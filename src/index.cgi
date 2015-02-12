#!/usr/bin/perl --
#!/usr/local/bin/perl --
#
# wiki.cgi - This is PyukiWiki, yet another Wiki clone.
#
# Copyright (C) 2004 by Nekyo.
# http://nekyo.hp.infoseek.co.jp/
#
# Based on YukiWiki
#
# 1TAB=4Spaces
#
# This program is free software; you can redistribute it and/or
# modify it under the same terms as Perl itself.
# Return Code:UNIX=LF/Windows=CR+LF/Mac=CR
##############################
# Libraries.
use strict;
# if you can use lib is ../lib then swap this comment
BEGIN {
	push @INC, 'lib';
}

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use Yuki::RSS;
use Yuki::DiffText qw(difftext);
use Yuki::YukiWikiDB;

# If You can use Jcode.pm then Swap the comment.
my $use_Jcodepm = 1;
use Jcode;
#my $use_Jcodepm = 0;
#require 'jcode.pl';

use Fcntl;
# Check if the server can use 'AnyDBM_File' or not.
# eval 'use AnyDBM_File';
# my $error_AnyDBM_File = $@;
$::version = '0.1.3';
##############################
# You MUST modify following initial file.

require 'pyukiwiki.ini.cgi';
require $::skin_file;

##############################
#
# You MAY modify following variables.
#
my $modifier_dbtype = 'YukiWikiDB';
my $modifier_sendmail = '';
#my $modifier_sendmail = '/usr/sbin/sendmail -t -n';
##############################
# You MAY modify following variables.

if ($::lang eq 'ja') {
	if ($::kanjicode eq 'euc') {
		$::charset = 'EUC-JP';
	} elsif ($::kanjicode eq 'utf8') {
		$::charset = 'UTF-8';
	} elsif ($::kanjicode eq 'sjis') {
		$::charset = 'Shift-JIS';
	}
} elsif ($::lang eq 'cn') {
	$::charset = 'gb2312';
}

my $file_resource = "$::data_home/resource.$::lang.txt";
my $file_conflict = "$::data_home/conflict.$::lang.txt";

##############################
my $editchar = '?';
my $subject_delimiter = ' - ';
my $use_autoimg = 1; # automatically convert image URL into <img> tag.
my $use_exists = 0; # If you can use 'exists' method for your DB.
#my $use_FixedFrontPage = 0;
##############################
my $interwikiName = 'InterWikiName';
my $AdminChangePassword = 'AdminChangePassword';
my $CompletedSuccessfully = 'CompletedSuccessfully';
my $ErrorPage = 'ErrorPage';

##############################
my $wiki_name = '\b([A-Z][a-z]+([A-Z][a-z]+)+)\b';
my $bracket_name = '\[\[([^\]]+?)\]\]';
my $embedded_name = '(\#\S+?)';
my $interwiki_definition = '\[\[(\S+?)\ (\S+?)\]\]';	# ? \[\[(\S+) +(\S+)\]\]
my $interwiki_definition2 = '\[(\S+?)\ (\S+?)\]\ (utf8|euc|sjis|yw|asis|raw)';
my $interwiki_name = '([^:]+):([^:].*)';
my $interwiki_name2 = '([^:]+):([^:#].*?)(#.*)?';
##############################
my $embed_plugin = '^#([^(]+)(\(([^)]+)\))?$';
my $embed_inline = '(&amp;[^;&]+;|&amp;[^)]+\))';
##############################
$::info_ConflictChecker = 'ConflictChecker';
my $info_LastModified = 'LastModified';
my $info_IsFrozen = 'IsFrozen';
my $info_AdminPassword = 'AdminPassword';
##############################
my %fixedpage = (
	$ErrorPage => 1,
	$::RecentChanges => 1,
	$AdminChangePassword => 1,
	$CompletedSuccessfully => 1,
);
my %fixedplugin = (
	'newpage' => 1,
	'search' => 1,
	'list' => 1,
);
my %infobase;
%::diffbase;
%::interwiki;
##############################
my %command_do = (
	read => \&do_read,
	write => \&do_write,
	createresult => \&do_createresult,
);

$::counter_ext = '.count';
my $lastmod;	# v0.0.9
my %_plugined;	# 1:Pyuki/2:Yuki/0:None

if (!$::upload_link) {
	$::upload_link = $::upload_dir;
}

##############################
my $_conv_start;
$_conv_start = (times)[0] if ($::enable_convtime != 0);

@::notes = ();

&main;
exit(0);
##############################

sub main {
	&init_resource;
	# &check_modifiers;
	&open_db;
	&init_form;
	&init_InterWikiName;
	if ($command_do{$::form{cmd}}) {
		&{$command_do{$::form{cmd}}};
	} else {
		my $exec = 1;
		if ($::form{cmd}) {
			if (&exist_plugin($::form{cmd}) == 1) {
				my $action = "\&plugin_" . $::form{cmd} . "_action";
				my %ret = eval $action;
				if (($ret{msg} ne '') && ($ret{body} ne '')) {
					$exec = 0;
					&skin($ret{msg}, $ret{body}, 0);
				}
			}
		}
		if ($exec == 1) {
			$::form{mypage} = $::FrontPage if (!$::form{mypage});
			&do_read;
		}
	}
	&close_db;
}

sub do_read {
	&skin($::form{mypage}, &text_to_html($::database{$::form{mypage}}), 1);
}

sub do_write {
	return if (&frozen_reject());

	if (not &is_editable($::form{mypage})) {
		&skin($::form{mypage}, &message($::resource{cantchange}), 0);
		return;
	}
	return if (&conflict($::form{mypage}, $::form{mymsg}));

	$::form{mymsg} =~ s/&date;/&date($::date_format)/gex;
	$::form{mymsg} =~ s/&time;/&date($::time_format)/gex;
#	'&page;' => array_pop(explode('/',$vars['page'])),
#	'&fpage;' => $vars['page'],

	# Making diff
	if (1) {
		&open_diff;
		my @msg1 = split(/\n/, $::database{$::form{mypage}});
		my @msg2 = split(/\n/, $::form{mymsg});
		$::diffbase{$::form{mypage}} = &difftext(\@msg1, \@msg2);
		&close_diff;
	}

	if ($::form{mymsg}) {
		$::database{$::form{mypage}} = $::form{mymsg};
		&send_mail_to_admin($::form{mypage}, "Modify");
		&set_info($::form{mypage}, $::info_ConflictChecker, '' . localtime);
		if ($::form{mytouch}) {
			&set_info($::form{mypage}, $info_LastModified, '' . localtime);
			&update_recent_changes;
		}
		&set_info($::form{mypage}, $info_IsFrozen, 0 + $::form{myfrozen});
		&do_read;
	} else {
		&send_mail_to_admin($::form{mypage}, "Delete");
		delete $::database{$::form{mypage}};
		delete $infobase{$::form{mypage}};
		&update_recent_changes if ($::form{mytouch});

		&skin($::form{mypage}, &message($::resource{deleted}), 0);
	}
}

sub print_error {
	my ($msg) = @_;
	&skin($ErrorPage, qq(<p><strong class="error">$msg</strong></p>), 0);
	exit(0);
}

sub escape {
	return &htmlspecialchars(shift);
}

sub unescape {
	my $s = shift;
	# $s =~ s|\n|\r\n|g;
	$s =~ s|\&amp;|\&|g;
	$s =~ s|\&lt;|\<|g;
	$s =~ s|\&gt;|\>|g;
	$s =~ s|\&quot;|\"|g;
	return $s;
}

sub print_content {
	my ($rawcontent) = @_;
	print &text_to_html($rawcontent);
}

sub text_to_html {
	my ($txt) = @_;
	my (@txt) = split(/\r?\n/, $txt);
	my $verbatim;
	my $tocnum = 0;
	my (@saved, @result);
	unshift(@saved, "</p>");
	push(@result, "<p>");

	foreach (@txt) {
		chomp;

		# verbatim.
		if ($verbatim->{func}) {
			if (/^\Q$verbatim->{done}\E$/) {
				undef $verbatim;
				push(@result, splice(@saved));
			} else {
				push(@result, $verbatim->{func}->($_));
			}
			next;
		}

		# non-verbatim follows.
		push(@result, shift(@saved)) if (@saved and $saved[0] eq '</pre>' and /^[^ \t]/);
		if (/^(\*{1,3})(.+)/) {
			my $hn = "h" . (length($1) + 1);	# $hn = 'h2', 'h3' or 'h4'
			my $hedding = ($tocnum != 0)
				? qq(<div class="jumpmenu"><a href="#navigator">&uarr;</a></div>)
				: '';

			my $nametag = ($::IsMenu == 1) ? "m" : "i";
			push(@result, splice(@saved),
				$hedding . qq(<$hn><a name="$nametag$tocnum"> </a>) . &inline($2) . qq(</$hn>)
			);
			$tocnum++;
		} elsif (/^(-{2,3})\($/) {
			if ($& eq '--(') {
				$verbatim = { func => \&inline, done => '--)', class => 'verbatim-soft' };
			} else {
				$verbatim = { func => \&escape, done => '---)', class => 'verbatim-hard' };
			}
			&back_push('pre', 1, \@saved, \@result, " class='$verbatim->{class}'");
		} elsif (/^{{{/) {	# OpenWiki like. Thanks wadldw.
			$verbatim = { func => \&inline, done => '}}}', class => 'verbatim-soft' };
			&back_push('pre', 1, \@saved, \@result, " class='$verbatim->{class}'");
		} elsif (/^----/) {
			push(@result, splice(@saved), '<hr>');
		} elsif (/^(-{1,3})(.+)/) {
			&back_push('ul', length($1), \@saved, \@result,
				" class=\"list" . length($1) . "\" style=\"padding-left:16px;margin-left:16px;\"");
			push(@result, '<li>' . &inline($2) . '</li>');
		} elsif (/^(\+{1,3})(.+)/) {
			&back_push('ol', length($1), \@saved, \@result,
				" class=\"list" . length($1) . "\" style=\"padding-left:16px;margin-left:16px;\"");
			push(@result, '<li>' . &inline($2) . '</li>');
		} elsif ((/^:([^:]+):(.*)/) || (/^:([^\|]+)\|(.*)/)) {
			push(@saved, '<dl><dt>', &inline($1) . "</dt>\n<dd>");
			push(@saved, &inline($2));
			$verbatim = { func => \&inline, done => '' };
			&back_push('', 0, \@saved, \@result);
			push(@saved, "</dd>\n</dl>");
		#	&back_push('dl', 1, \@saved, \@result);
		#	push(@result, '<dt>' . &inline($1) . '</dt>', '<dd>' . &inline($2) . '</dd>');
		} elsif (/^(>{1,3})(.+)/) {
			&back_push('blockquote', length($1), \@saved, \@result);
			push(@result, &inline($2));
		} elsif (/^$/) {
			push(@result, splice(@saved));
			unshift(@saved, "</p>");
			push(@result, "<p>");
		} elsif (/^(\s+.*)$/) {
			&back_push('pre', 1, \@saved, \@result);
			push(@result, &htmlspecialchars($1)); # Not &inline, but &escape
		} elsif (/^([\,|\|])(.*?)[\x0D\x0A]*$/) {
			&back_push('table', 1, \@saved, \@result,
				' class="style_table" cellspacing="1" border="0"');
			#######
			# This part is taken from Mr. Ohzaki's Perl Memo and Makio Tsukamoto's WalWiki.
			# XXXXX
			my $delm = "\\$1";
			my $tmp = ($1 eq ',') ? "$2$1" : "$2";
			my @value = map {/^"(.*)"$/ ? scalar($_ = $2, s/""/"/g, $_) : $_}
				($tmp =~ /("[^"]*(?:""[^"]*)*"|[^$delm]*)$delm/g);
			my @align = map {(s/^\s+//) ? ((s/\s+$//) ? ' align="center"' : ' align="right"') : ''} @value;
			my @colspan = map {($_ eq '==') ? 0 : 1} @value;
			for (my $i = 0; $i < @value; $i++) {
				if ($colspan[$i]) {
					while ($i + $colspan[$i] < @value and $value[$i + $colspan[$i]] eq '==') {
						$colspan[$i]++;
					}
					$colspan[$i] = ($colspan[$i] > 1) ? sprintf(' colspan="%d"', $colspan[$i]) : '';
					$value[$i] = sprintf('<td%s%s class="style_td">%s</td>', $align[$i], $colspan[$i], &inline($value[$i]));
				} else {
					$value[$i] = '';
				}
			}
			push(@result, join('', '<tr>', @value, '</tr>'));
			# XXXXX
			#######
		} elsif (/^====/) {
			if ($::form{show} ne 'all') {
				push(@result, splice(@saved), "<a href=\"$::script?cmd=read&mypage="
					. &encode($::form{mypage}) . "&show=all\">$::resource{continue_msg}</a>");
				last;
			}
		} else {
			push(@result, &inline($_));
		#	push(@result, "<br />");	# Thanks wadldw.
		}
	}
	push(@result, splice(@saved));
	return join("\n", @result);
}

sub back_push {
	my ($tag, $level, $savedref, $resultref, $attr) = @_;
	while (@$savedref > $level) {
		push(@$resultref, shift(@$savedref));
	}
	if ($savedref->[0] ne "</$tag>") {
		push(@$resultref, splice(@$savedref));
	}
	while (@$savedref < $level) {
		unshift(@$savedref, "</$tag>");
		push(@$resultref, "<$tag$attr>");
	}
}

sub inline {
	my ($line) = @_;
	$line = &htmlspecialchars($line);
	$line =~ s|'''([^']+?)'''|<em>$1</em>|g;		# Italic
	$line =~ s|''([^']+?)''|<strong>$1</strong>|g;	# Bold
	$line =~ s|%%%([^%]*)%%%|<ins>$1</ins>|g;		# Insert Line
	$line =~ s|%%([^%]*)%%|<del>$1</del>|g;			# Delete Line
	$line =~ s|\^\^([^\^]*)\^\^|<sup>$1</sup>|g;	# sup
	$line =~ s|__([^_]*)__|<sub>$1</sub>|g;			# sub
	$line =~ s|(\d\d\d\d-\d\d-\d\d \(\w\w\w\) \d\d:\d\d:\d\d)|<span class="date">$1</span>|g;	# Date
	$line =~ s|~$|<br />|g;							# ~\n -> <br />
	$line =~ s|^//.*$||g;							# Comment
	$line =~ s!^(LEFT|CENTER|RIGHT):(.*)$!<div style="text-align:$1">$2</div>!g;
	$line =~ s!^(RED|BLUE|GREEN):(.*)$!<font color="$1">$2</font>!g;	# v0.0.9 Tnx hash.
	$line =~ s|\(\((.*)\)\)|&note($1)|gex;

	$line =~ s|\[\#(.*)\]|<a class="anchor_super" id="$1" href="#$1" title="$1">$::_symbol_anchor</a>|g;

	if ($line =~ /^$embedded_name$/) {
		$line =~ s!^$embedded_name$!&embedded_to_html($1)!gex;	# #command
	} else {
		$line =~ s!
			(
				($bracket_name)			# [[likethis]], [[Friend:remotelink]]
					|
				($interwiki_definition)	# [[Friend http://somewhere/?q=sjis($1)]]
					|
				((mailto|http|https|ftp):([^\x00-\x20()<>\x7F-\xFF\]])*)	# Direct http://...
					|
				($wiki_name)			# LocalLinkLikeThis
					|
				($embed_inline)			# &user_defined_plugin(123,hello)
			)
			!
				&make_link($1)
			!gex;
	}

	if ($::usefacemark == 1) {
		$line =~ s!\s(\:\)|\(\^\^\))! <img src="$::image_dir/face/smile.png" alt="$1" />!g;
		$line =~ s!\s(\:D|\(\^-\^\))! <img src="$::image_dir/face/bigsmile.png" alt="$1" />!g;
		$line =~ s!\s(\:p|\:d)! <img src="$::image_dir/face/huh.png" alt="$1" />!g;
		$line =~ s!\s(XD|X\(|\(\.\.;)! <img src="$::image_dir/face/oh.png" alt="$1" />!g;
		$line =~ s!\s(;\)|\(\^_-\))! <img src="$::image_dir/face/wink.png" alt="$1" />!g;
		$line =~ s!\s(;\(|\:\(|\(--;\))! <img src="$::image_dir/face/sad.png" alt="$1" />!g;
		$line =~ s!&(heart);!<img src="$::image_dir/face/heart.png" alt="$1" />!g;
		$line =~ s!\s\(\^\^;\)?! <img src="$::image_dir/face/worried.png" alt="$1" />!g;
	}
	return $line;
}

sub note {
	my ($msg) = @_;

	push(@::notes, $msg);
	return "<a id=\"notetext_" . @::notes . "\" "
		. "href=\"#notefoot_" . @::notes . "\" class=\"note_super\">*"
		. @::notes . "</a>";
}

sub make_link {
	my $chunk = shift;
	if ($chunk =~ /^(http|https|ftp):/) {
		if ($use_autoimg and $chunk =~ /\.(gif|png|jpeg|jpg)$/) {
			return qq(<a href="$chunk"><img src="$chunk"></a>);
		} else {
			# v0.0.9
			return qq(<a href="$chunk" target="_blank" >$chunk</a>) if ($::use_popup != 0);
			return qq(<a href="$chunk">$chunk</a>);
		}
	} elsif ($chunk =~ /^(mailto):(.*)/) {
		return qq(<a href="$chunk">$2</a>);
	} elsif ($chunk =~ /^$interwiki_definition2$/) {
		return qq(<span class="InterWiki"><a href="$1">$2</a> $3</span>);
	} elsif ($chunk =~ /$embed_inline/) {
		return &embedded_inline($1)
	} else {
		$chunk = &unarmor_name($chunk);
		$chunk = &unescape($chunk); # To treat '&' or '>' or '<' correctly.
		my $cookedchunk = &encode($chunk);
		my $escapedchunk = &htmlspecialchars($chunk);
		if (0 < index($chunk, '>')) {			# Nekyo Add Start alias ymu=
			my @alias = split(/>/, $chunk);		# [[alias>URL]]
			$cookedchunk = &encode($alias[1]);
			$escapedchunk = &htmlspecialchars($alias[0]);
			$chunk = $alias[1];
		} elsif (($chunk =~ /(.+?):((http|https|ftp):.*)/)
			or ($chunk =~ /(.+?):(.+)/ && !$::interwiki{$1})) {
			$escapedchunk = &htmlspecialchars($1);
			$chunk = $2;
			$cookedchunk = &encode($chunk);
		}
		if ($chunk =~ /^(http|https|ftp):/) {
			if ($use_autoimg and $escapedchunk =~ /\.(gif|png|jpeg|jpg)$/) {
				return qq(<a href="$chunk"><img src="$escapedchunk"></a>);
			} else {
				# v0.0.9
				return qq(<a href="$chunk" target="_blank" >$escapedchunk</a>)
					if ($::use_popup != 0);
				return qq(<a href="$chunk">$escapedchunk</a>);
			}
		} elsif ($chunk =~ /^$interwiki_name2$/) {
			my ($intername, $keyword, $anchor) = ($1, $2, $3);
			if (exists $::interwiki2{$intername}) {
				my ($code, $url) = %{$::interwiki2{$intername}};
				$url =~ s/\$1/&interwiki_convert($code, $keyword)/e;
				$url = &htmlspecialchars($url.$anchor);
				# v0.0.9
				return qq(<a href="$url" target="_blank">$escapedchunk</a>)
					if ($::use_popup != 0);
				return qq(<a href="$url">$escapedchunk</a>);
			} else {
				return $escapedchunk;
			}
		} elsif ($chunk =~ /^$interwiki_name$/) {
			my ($intername, $localname) = ($1, $2);
			my $remoteurl = $::interwiki{$intername};
			if ($remoteurl) {
				$remoteurl =~
				 s/\b(utf8|euc|sjis|ykwk|asis)\(\$1\)/&interwiki_convert($1, $localname)/e;
				return qq(<a href="$remoteurl">$escapedchunk</a>);
			} else {
				return $escapedchunk;
			}
		}

		$chunk = get_fullname($chunk, $::form{mypage});
		$cookedchunk  = &encode($chunk);
		if ($::database{$chunk}) {
			return qq(<a title="$chunk" href="$::script?$cookedchunk">$escapedchunk</a>);
		} elsif (($chunk =~ /^([^#]*)#/) && $::database{$1}) {
			return qq(<a title="$chunk" href="$::script?$chunk">$escapedchunk</a>);
		} elsif (&is_editable($chunk)) {
			return qq($escapedchunk<a title="$::resource{editthispage}" class="editlink" href="$::script?cmd=edit&amp;mypage=$cookedchunk">$editchar</a>);
		}
		return $escapedchunk;
	}
}

sub get_fullname {
	my ($name, $refer) = @_;

	return $refer if ($name eq '');
	if ($name eq '/') {
		$name = substr($name,1);
		return ($name eq '') ? $::FrontPage : $name;
	}
	return $refer if ($name eq './');
	if (substr($name,0,2) eq './') {
		return ($1) ? $refer . '/' . $1 : $refer;
	}
	if (substr($name,0,3) eq '../') {
		my @arrn = split('/', $name);
		my @arrp = split('/', $refer);

		while (@arrn > 0 and $arrn[0] eq '..') {
			shift(@arrn);
			pop(@arrp);
		}
		$name = @arrp ? join('/',(@arrp,@arrn)) :
			(@arrn ? "$::FrontPage/".join('/',@arrn) : $::FrontPage);
	}
	return $name;
}

sub message {
	my ($msg) = @_;
	return qq(<p><strong>$msg</strong></p>);
}

sub init_form {
	if (param()) {
		foreach my $var (param()) {
			$::form{$var} = param($var);
		}
	} else {
		$ENV{QUERY_STRING} = $::FrontPage;
	}

	my $query = &decode($ENV{QUERY_STRING});
	if ($query =~ /&/) {
		my @querys = split(/&/, $query);
		foreach (@querys) {
			$::form{$1} = $2 if (/([^=]*)=(.*)$/);
		}
	}

	if ($query =~ /^($wiki_name)$/) {
		$::form{cmd} = 'read';
		$::form{mypage} = $1;
	} elsif ($::database{$query}) {
		$::form{cmd} = 'read';
		$::form{mypage} = $query;
	}

	# mypreview_edit        -> do_edit, with preview.
	# mypreview_adminedit   -> do_adminedit, with preview.
	# mypreview_write       -> do_write, without preview.
	foreach (keys %::form) {
		if (/^mypreview_(.*)$/) {
			$::form{cmd} = $1;
			$::form{mypreview} = 1;
		}
	}

	# $::form{cmd} is frozen here.

	$::form{mymsg} = &code_convert(\$::form{mymsg},   $::kanjicode);
	$::form{myname} = &code_convert(\$::form{myname}, $::kanjicode);
}

sub update_recent_changes {
	my $update = "- @{[&get_now]} @{[&armor_name($::form{mypage})]} @{[&get_subjectline($::form{mypage})]}";
	my @oldupdates = split(/\r?\n/, $::database{$::RecentChanges});
	my @updates;
	foreach (@oldupdates) {
		/^\- \d\d\d\d\-\d\d\-\d\d \(...\) \d\d:\d\d:\d\d (\S+)/;	# date format.
		my $name = &unarmor_name($1);
		if (&is_exist_page($name) and ($name ne $::form{mypage})) {
			push(@updates, $_);
		}
	}
	unshift(@updates, $update) if (&is_exist_page($::form{mypage}));
	splice(@updates, $::maxrecent + 1);
	$::database{$::RecentChanges} = join("\n", @updates);
}

sub get_subjectline {
	my ($page, %option) = @_;
	if (not &is_editable($page)) {
		return "";
	} else {
		# Delimiter check.
		my $delim = $subject_delimiter;
		$delim = $option{delimiter} if (defined($option{delimiter}));
		# Get the subject of the page.
		my $subject = $::database{$page};
		$subject =~ s/\r?\n.*//s;
		return "$delim$subject";
	}
}

sub send_mail_to_admin {
	my ($page, $mode) = @_;
	return unless $modifier_sendmail;
	my $message = <<"EOD";
To: $::modifier_mail
From: $::modifier_mail
Subject: [Wiki]
MIME-Version: 1.0
Content-Type: text/plain; charset=ISO-2022-JP
Content-Transfer-Encoding: 7bit

--------
MODE = $mode
REMOTE_ADDR = $ENV{REMOTE_ADDR}
REMOTE_HOST = $ENV{REMOTE_HOST}
--------
$page
--------
$::database{$page}
--------
EOD
	&code_convert(\$message, 'jis');
	open(MAIL, "| $modifier_sendmail");
	print MAIL $message;
	close(MAIL);
}

sub open_db {
	if ($modifier_dbtype eq 'dbmopen') {
		dbmopen(%::database, $::data_dir, 0666) or &print_error("(dbmopen) $::data_dir");
		dbmopen(%infobase, $::info_dir, 0666) or &print_error("(dbmopen) $::info_dir");
	} elsif ($modifier_dbtype eq 'AnyDBM_File') {
		tie(%::database, "AnyDBM_File", $::data_dir, O_RDWR|O_CREAT, 0666) or &print_error("(tie AnyDBM_File) $::data_dir");
		tie(%infobase, "AnyDBM_File", $::info_dir, O_RDWR|O_CREAT, 0666) or &print_error("(tie AnyDBM_File) $::info_dir");
	} else {
		tie(%::database, "Yuki::YukiWikiDB", $::data_dir) or &print_error("(tie Yuki::YukiWikiDB) $::data_dir");
		tie(%infobase, "Yuki::YukiWikiDB", $::info_dir) or &print_error("(tie Yuki::YukiWikiDB) $::info_dir");
	}
}

sub close_db {
	if ($modifier_dbtype eq 'dbmopen') {
		dbmclose(%::database);
		dbmclose(%infobase);
#	} elsif ($modifier_dbtype eq 'AnyDBM_File') {
#		untie(%::database);
#		untie(%infobase);
	} else {
		untie(%::database);
		untie(%infobase);
	}
}

sub open_diff {
	if ($modifier_dbtype eq 'dbmopen') {
		dbmopen(%::diffbase, $::diff_dir, 0666) or &print_error("(dbmopen) $::diff_dir");
	} elsif ($modifier_dbtype eq 'AnyDBM_File') {
		tie(%::diffbase, "AnyDBM_File", $::diff_dir, O_RDWR|O_CREAT, 0666) or &print_error("(tie AnyDBM_File) $::diff_dir");
	} else {
		tie(%::diffbase, "Yuki::YukiWikiDB", $::diff_dir) or &print_error("(tie Yuki::YukiWikiDB) $::diff_dir");
	}
}

sub close_diff {
	if ($modifier_dbtype eq 'dbmopen') {
		dbmclose(%::diffbase);
#	} elsif ($modifier_dbtype eq 'AnyDBM_File') {
#		untie(%::diffbase);
	} else {
		untie(%::diffbase);
	}
}

sub is_editable {
	my ($page) = @_;
	if (&is_bracket_name($page)) {
		return 0;
	} elsif ($fixedpage{$page}) {
		return 0;
	} elsif ($fixedplugin{$::form{cmd}}) {
		return 0;
	} elsif ($page =~ /\s/) {
		return 0;
	} elsif ($page =~ /^\#/) {
		return 0;
	} elsif ($page =~ /^$interwiki_name$/) {
		return 0;
	} elsif ($page =~ /(^|\/)\.{1,2}(\/|$)/) { # ./ ../ is ng
		return 0;
	} elsif (not $page) {
		return 0;
	} else {
		return 1;
	}
}

# armor_name:
#   WikiName -> WikiName
#   not_wiki_name -> [[not_wiki_name]]
sub armor_name {
	my ($name) = @_;
	return ($name =~ /^$wiki_name$/) ? $name : "[[$name]]";
}

# unarmor_name:
#   [[bracket_name]] -> bracket_name
#   WikiName -> WikiName
sub unarmor_name {
	my ($name) = @_;
	return ($name =~ /^$bracket_name$/) ? $1 : $name;
}

sub is_bracket_name {
	my ($name) = @_;
	return ($name =~ /^$bracket_name$/) ? 1 : 0;
}

sub dbmname {
	my ($name) = @_;
	$name =~ s/(.)/uc unpack('H2', $1)/eg;
	return $name;
}

sub decode {
	my ($s) = @_;
	$s =~ tr/+/ /;
	$s =~ s/%([A-Fa-f0-9][A-Fa-f0-9])/pack("C", hex($1))/eg;
	return $s;
}

# Thanks to WalWiki for [better encode].
sub encode {
	my ($encoded) = @_;
	$encoded =~ s/(\W)/'%' . unpack('H2', $1)/eg;
	return $encoded;
}

sub init_resource {
	open(FILE, $file_resource) or &print_error("(resource)");
	while (<FILE>) {
		s/\r\n/\n/;
		chomp;
		next if /^#/;
		my ($key, $value) = split(/=/, $_, 2);
		$::resource{$key} = &code_convert(\$value, $::kanjicode);
	}
	close(FILE);
}

sub conflict {
	my ($page, $rawmsg) = @_;
	if ($::form{myConflictChecker} eq &get_info($page, $::info_ConflictChecker)) {
		return 0;
	}
	open(FILE, $file_conflict) or &print_error("(conflict)");
	my $content = join('', <FILE>);
	&code_convert(\$content, $::kanjicode);
	close(FILE);

	my $body = &text_to_html($content);
	if (&exist_plugin('edit') == 1) {
		$body .= &editform($rawmsg, $::form{myConflictChecker}, frozen=>0, conflict=>1);
	}

	&skin($page, $body, 0);
	return 1;
}

sub get_now {
	my (@week) = qw(Sun Mon Tue Wed Thu Fri Sat);
	my ($sec, $min, $hour, $day, $mon, $year, $weekday) = localtime(time);
	$weekday = $week[$weekday];
	return sprintf("%d-%02d-%02d ($weekday) %02d:%02d:%02d",
		$year + 1900, $mon + 1, $day, $hour, $min, $sec);
}

# [[YukiWiki http://www.hyuki.com/yukiwiki/wiki.cgi?euc($1)]]
# [http://www.hyuki.com/yukiwiki/wiki.cgi?$1 YukiWiki] euc
sub init_InterWikiName {
	my $content = $::database{$interwikiName};
	while ($content =~ /$interwiki_definition/g) {
		my ($name, $url) = ($1, $2);
		$::interwiki{$name} = $url;
	}
	while ($content =~ /$interwiki_definition2/g) {
		$::interwiki2{$2}{$3} = $1;
	}
}

sub interwiki_convert {
	my ($type, $localname) = @_;
	if ($type eq 'sjis' or $type eq 'euc' or $type eq 'utf8') {
		&code_convert(\$localname, $type);
		return &encode($localname);
	} elsif (($type eq 'ykwk') || ($type eq 'yw')) {
		# for YukiWiki1
		if ($localname =~ /^$wiki_name$/) {
			return $localname;
		} else {
			&code_convert(\$localname, 'sjis');
			return &encode("[[" . $localname . "]]");
		}
#	} elsif (($type eq 'asis') || ($type eq 'raw')) {
#		return $localname;
	} else {
		return $localname;
	}
}

sub get_info {
	my ($page, $key) = @_;
	my %info = map { split(/=/, $_, 2) } split(/\n/, $infobase{$page});
	return $info{$key};
}

sub set_info {
	my ($page, $key, $value) = @_;
	my %info = map { split(/=/, $_, 2) } split(/\n/, $infobase{$page});
	$info{$key} = $value;
	my $s = '';
	for (keys %info) {
		$s .= "$_=$info{$_}\n";
	}
	$infobase{$page} = $s;
}

sub frozen_reject {
	my ($isfrozen) = &get_info($::form{mypage}, $info_IsFrozen);
	my ($willbefrozen) = $::form{myfrozen};
	if (not $isfrozen and not $willbefrozen) {
		# You need no check.
		return 0;
	} elsif (valid_password($::form{mypassword})) {
		# You are admin.
		return 0;
	} else {
		&print_error($::resource{passworderror});
		return 1;
	}
}

sub valid_password {
	my ($givenpassword) = @_;
	return (crypt($givenpassword, "AA") eq $::adminpass) ? 1 : 0;
}

sub is_frozen {
	my ($page) = @_;
	return (&get_info($page, $info_IsFrozen)) ? 1 : 0;
}

# require plugin with flag control;
sub exist_plugin {
	my ($plugin) = @_;

	if (!$_plugined{$plugin}) {
		my $path = "$::plugin_dir/$plugin" . '.inc.pl';
		if (-e $path) {
			require $path;
			$_plugined{$1} = 1;	# Pyuki
			return 1;
		} else {
			$path = "$::plugin_dir/$plugin" . '.pl';
			if (-e $path) {
				require $path;
				$_plugined{$1} = 2;	# Yuki
				return 2;
			}
		}
		return 0;
	}
	return $_plugined{$plugin};
}

sub embedded_to_html {
	my $embedded = shift;

	if ($embedded =~ /$embed_plugin/) {
		my $exist = &exist_plugin($1);
		my $action = '';
		if ($exist == 1) {
			$action = "\&plugin_" . $1 . "_convert('$3')";
		} elsif ($exist == 2) {
			$action = "\&$1::plugin_block('$3');";
		}
		if ($action ne '') {
			$_ = eval $action;
			return ($_) ? $_ : &htmlspecialchars($embedded);
		}
	}
	return $embedded;
}

sub embedded_inline {
	my $embedded = shift;

	if ($embedded =~ /&amp;([^;({]+)(\(([^)]*)\))?({([^}]*)})?;?/) {
		my $arg = ($3) ? $3 : '';
		if ($5) {
			if ($arg ne '') { $arg .= "," }
			$arg .= $5;
		}

		my $exist = &exist_plugin($1);
		my $action = '';
		if ($exist == 1) {
			$action = "\&plugin_" . $1 . "_inline('$arg')";
		} elsif ($exist == 2) {
			$action = "\&$1::plugin_inline('$arg');";
		}
		if ($action ne '') {
			$_ = eval $action;
			return $_ if ($_);
		}
	}
	return &unescape($embedded);
}

sub code_convert {
	my ($contentref, $kanjicode) = @_;
	if ($::lang eq 'ja') {
		if ($use_Jcodepm == 1) {
			&Jcode::convert($contentref, $kanjicode);	# for Jcode.pm
		} elsif ($kanjicode eq 'euc' or $kanjicode eq 'sjis') {
			&jcode::convert($contentref, $kanjicode);	# for jcode.pl
		}
	}
	return $$contentref;
}

sub is_exist_page {
	my ($name) = @_;
	return ($use_exists) ? exists($::database{$name}) : $::database{$name};
}

# Like a PHP.
sub trim {
	my ($s) = @_;
	$s =~ s/^\s*(\S+)\s*$/$1/o; # trim
	return $s;
}

sub mktime {
	my ($hour, $min, $sec, $month, $day, $year) = @_;
	my $days = 0;

	if    ($year <  70) { $year += 2000; } #  0-69 -> 2000-2069
	elsif ($year < 100) { $year += 1900; } # 70-99 -> 1970-1999

	my $i;
	for ($i = 1970; $i < $year; $i++) {
		$days += ($i % 4 == 0 && ($i % 400 == 0 || $i % 100 != 0)) ? 366 : 365;
	}
	# Nishi Muku Samurai!
	my @samurai = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);
	for ($i = 1; $i < $month; $i++) {
		$days += ($i == 2 && $year % 4 == 0 && ($year % 400 == 0 || $year % 100 != 0)) ? 29 : $samurai[$i - 1];
	}
	$days += $day;
	return (((($days * 24) + $hour) * 60) + $min) * 60 + $sec;
}

sub htmlspecialchars {
	my ($s) = @_;
	$s =~ s|\r\n|\n|g;
	$s =~ s|\&|&amp;|g;
	$s =~ s|<|&lt;|g;
	$s =~ s|>|&gt;|g;
	$s =~ s|"|&quot;|g;
	return $s;
}

sub date
{
	my ($format, $tm) = @_;

	# yday:0-365 $isdst Summertime:1/not:0
	my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = ((@_ > 1) ? localtime($tm) : localtime);
	$year += 1900;	# 
	my ($hr12, $ampm) = $hour >= 12 ? ($hour - 12,'pm') : ($hour, 'am');

	# year
	$format =~ s/Y/$year/ge;	# Y:4char ex)1999 or 2003
	$year = $year % 100;
	$year = "0" . $year if ($year < 10);
	$format =~ s/y/$year/ge;	# y:2char ex)99 or 03

	# month
	my $month = ('January','February','March','April','May','June','July','August','September','October','November','December')[$mon];
	$mon++;									# mon is 0 to 11 add 1
	$format =~ s/n/$mon/ge;					# n:1-12
	$mon = "0" . $mon if ($mon < 10);
	$format =~ s/m/$mon/ge;					# m:01-12
	$format =~ s/M/substr($month,0,3)/ge;	# M:Jan-Dec
	$format =~ s/F/$month/ge;				# F:January-December

	# day
	$format =~ s/j/$mday/ge;				# j:1-31
	$mday = "0" . $mday if ($mday < 10);
	$format =~ s/d/$mday/ge;				# d:01-31

	# hour
	$format =~ s/g/$hr12/ge;				# g:1-12
	$format =~ s/G/$hour/ge;				# G:0-23
	$hr12 = "0" . $hr12 if ($hr12 < 10);
	$hour = "0" . $hour if ($hour < 10);
	$format =~ s/h/$hr12/ge;				# h:01-12
	$format =~ s/H/$hour/ge;				# H:00-23

	# minutes
	$min = "0" . $min if ($min < 10);
	$format =~ s/i/$min/ge;					# i:00-59

	# second
	$sec = "0" . $sec if ($sec < 10);
	$format =~ s/s/$sec/ge;					# s:00-59

	$format =~ s/a/$ampm/ge;	# a:am or pm
	$format =~ s/A/uc $ampm/ge;	# A:AM or PM

	$format =~ s/w/$wday/ge;	# w:0(Sunday)-6(Saturday)

	my $weekday = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')[$wday];
	$format =~ s/l/$weekday/ge;				# l(lower L):Sunday-Saturday
	$format =~ s/D/substr($weekday,0,3)/ge;	# D:Mon-Sun

	$format =~ s/I/$isdst/ge;	# I(Upper i):1 Summertime/0:Not

	# Not Allowed
	# L 閏年であるかどうかを表す論理値。 1なら閏年。0なら閏年ではない。 
	# O グリニッジ標準時(GMT)との時間差 Example: +0200 
	# r RFC 822 フォーマットされた日付 Example: Thu, 21 Dec 2000 16:01:07 +0200 
	# S 英語形式の序数を表すサフィックス。2 文字。 st, nd, rd or th. Works well with j  
	# T このマシーンのタイムゾーンの設定。 Examples: EST, MDT ... 
	# U Unix 時(1970年1月1日0時0分0秒)からの秒数 See also time() 
	# W ISO-8601 月曜日に始まる年単位の週番号 (PHP 4.1.0で追加) Example: 42 (the 42nd week in the year) 
	$format =~ s/z/$yday/ge;	# z:days/year 0-366
	return $format;
}

1;
__END__
=head1 NAME

wiki.cgi - This is PyukiWiki, yet another Wiki clone.

=head1 DESCRIPTION

PyukiWiki is yet another Wiki clone. Based on YukiWiki

YukiWiki can treat Japanese WikiNames (enclosed with [[ and ]]).
YukiWiki provides 'InterWiki' feature, RDF Site Summary (RSS),
and some embedded commands (such as [[#comment]] to add comments).

=head1 AUTHOR

Nekyo http://nekyo.hp.infoseek.co.jp/

=head1 LICENSE

Copyright (C) 2004 by Nekyo.

This program is free software; you can redistribute it and/or
modify it under the same terms as Perl itself.

=cut
