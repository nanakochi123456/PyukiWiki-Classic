#!/usr/local/bin/perl --
#
# wiki.cgi - This is PyukiWiki, yet another Wiki clone.
#
# Copyright (C) 2004 by Nekyo.
# http://nekyo.hp.infoseek.co.jp/
#
# Based on YukiWiki <hyuki@hyuki.com> http://www.hyuki.com/yukiwiki/
# Powerd by PukiWiki http://pukiwiki.org/
#
# 1TAB=4Spaces
#
# This program is free software; you can redistribute it and/or
# modify it under the same terms as Perl itself.
# Return Code:UNIX=LF/Windows=CR+LF/Mac=CR
##############################
# Libraries.
use strict;
use lib qw(.);
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser);
use Yuki::RSS;
use Yuki::DiffText qw(difftext);
use Yuki::YukiWikiDB;

# If You can use Jcode.pm then Swap the comment.
#my $use_Jcodepm = 1;
#use Jcode;
my $use_Jcodepm = 0;
require 'jcode.pl';

use Fcntl;
# Check if the server can use 'AnyDBM_File' or not.
# eval 'use AnyDBM_File';
# my $error_AnyDBM_File = $@;
$::version = '0.0.9';
##############################
#
# You MUST modify following '$modifier_...' variables.
#
require 'pyukiwiki.ini.cgi';

##############################
#
# You MAY modify following variables.
#
my $modifier_dbtype = 'YukiWikiDB';
my $modifier_sendmail = '';
# my $modifier_sendmail = '/usr/sbin/sendmail -t -n';
##############################
#
# You MAY modify following variables.
#

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

my $file_touch = "$::modifier_dir_data/touched.txt";
my $file_resource = "$::modifier_dir_data/resource.$::lang.txt";
my $file_conflict = "$::modifier_dir_data/conflict.txt";
my $file_format = "$::modifier_dir_data/format.txt";

my $url_stylesheet = "$::modifierlink_data/default.ja.css"; # wiki.css -> default.ja.css
$::maxrecent = 50;
my $cols = 80;
my $rows = 20;
##############################
#
# You MAY modify following variables.
#
$::dataname = "$::modifier_dir_data/wiki";
my $infoname = "$::modifier_dir_data/info";
my $diffname = "$::modifier_dir_data/diff";
my $editchar = '?';
my $subject_delimiter = ' - ';
my $use_autoimg = 1; # automatically convert image URL into <img> tag.
my $use_exists = 0; # If you can use 'exists' method for your DB.
#my $use_FixedFrontPage = 0;
##############################
my $InterWikiName = 'InterWikiName';
my $AdminChangePassword = 'AdminChangePassword';
my $CompletedSuccessfully = 'CompletedSuccessfully';
my $ErrorPage = 'ErrorPage';
my $AdminSpecialPage = 'Admin Special Page'; # must include spaces.

##############################
my $wiki_name = '\b([A-Z][a-z]+([A-Z][a-z]+)+)\b';
my $bracket_name = '\[\[(\S+?)\]\]';
my $embedded_name = '(\#\S+?)';
my $interwiki_definition = '\[\[(\S+?)\ (\S+?)\]\]';
my $interwiki_name = '([^:]+):([^:].*)';
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
my %diffbase;
my %interwiki;
##############################
my %page_command = (
	$AdminChangePassword => 'adminchangepasswordform',
);
my %command_do = (
	read => \&do_read,
	edit => \&do_edit,
	adminedit => \&do_adminedit,
	adminchangepasswordform => \&do_adminchangepasswordform,
	adminchangepassword => \&do_adminchangepassword,
	write => \&do_write,
	createresult => \&do_createresult,
);

my $plugin_dir = "./plugin/";
$::counter_dir = "$::modifier_dir_data/counter/";
$::counter_ext = '.count';
my $lastmod;	# v0.0.9

##############################
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
			my $path = $plugin_dir . $::form{cmd} . '.inc.pl';
			if (-e $path) {
				my $action = "\&plugin_" . $::form{cmd} . "_action";
				require $path;
				my %ret = eval $action;
				if (($ret{msg} ne '') && ($ret{body} ne '')) {
					$exec = 0;
					&print_header($ret{msg});
					print $ret{body};
					&print_footer($ret{msg});
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
	&print_header($::form{mypage});
	print <<"EOD";
<table border="0" style="width:100%">
  <tr>
    <td class="menubar">
    <div id="menubar">
EOD
	my $mypage = $::form{mypage};	# push;
	$::form{mypage} = $::MenuBar;
	&print_content($::database{$::form{mypage}});
	$::form{mypage} = $mypage;		# pop

	print <<"EOD";
    </div>
    </td>
    <td valign=top>
EOD
	&print_content($::database{$::form{mypage}});
	print <<"EOD";
    </td>
  </tr>
</table>
EOD
	&print_footer($::form{mypage});
}

sub do_edit {
	my ($page) = &unarmor_name(&armor_name($::form{mypage}));
	&print_header($page);
	if (not &is_editable($page)) {
		&print_message($::resource{cantchange});
	} elsif (&is_frozen($page)) {
		&print_message($::resource{cantchange});
	} else {
		&print_editform($::database{$page}, &get_info($page, $::info_ConflictChecker), admin=>0);
	}
	&print_footer($page);
}

sub do_adminedit {
	my ($page) = &unarmor_name(&armor_name($::form{mypage}));
	&print_header($page);
	if (not &is_editable($page)) {
		&print_message($::resource{cantchange});
	} else {
		&print_message($::resource{passwordneeded});
		&print_editform($::database{$page}, &get_info($page, $::info_ConflictChecker), admin=>1);
	}
	&print_footer($page);
}

sub do_adminchangepasswordform {
	&print_header($AdminChangePassword);
	&print_passwordform;
	&print_footer($AdminChangePassword);
}

sub do_adminchangepassword {
	if ($::form{mynewpassword} ne $::form{mynewpassword2}) {
		&print_error($::resource{passwordmismatcherror});
	}
	my ($validpassword_crypt) = &get_info($AdminSpecialPage, $info_AdminPassword);
	if ($validpassword_crypt) {
		if (not &valid_password($::form{myoldpassword})) {
			&send_mail_to_admin(<<"EOD", "AdminChangePassword");
myoldpassword=$::form{myoldpassword}
mynewpassword=$::form{mynewpassword}
mynewpassword2=$::form{mynewpassword2}
EOD
			&print_error($::resource{passworderror});
		}
	}
	my ($sec, $min, $hour, $day, $mon, $year, $weekday) = localtime(time);
	my (@token) = ('0'..'9', 'A'..'Z', 'a'..'z');
	my $salt1 = $token[(time | $$) % scalar(@token)];
	my $salt2 = $token[($sec + $min*60 + $hour*60*60) % scalar(@token)];
	my $crypted = crypt($::form{mynewpassword}, "$salt1$salt2");
	&set_info($AdminSpecialPage, $info_AdminPassword, $crypted);

	&print_header($CompletedSuccessfully);
	&print_message($::resource{passwordchanged});
	&print_footer($CompletedSuccessfully);
}

sub do_write {
	if (&frozen_reject()) {
		return;
	}

	if (not &is_editable($::form{mypage})) {
		&print_header($::form{mypage});
		&print_message($::resource{cantchange});
		&print_footer($::form{mypage});
		return;
	}

	if (&conflict($::form{mypage}, $::form{mymsg})) {
		return;
	}

	$::form{mymsg} =~ s/&date;/&date($::date_format)/gex;
	$::form{mymsg} =~ s/&time;/&date($::time_format)/gex;
#	'&page;' => array_pop(explode('/',$vars['page'])),
#	'&fpage;' => $vars['page'],

	# Making diff
	if (1) {
		&open_diff;
		my @msg1 = split(/\n/, $::database{$::form{mypage}});
		my @msg2 = split(/\n/, $::form{mymsg});
		$diffbase{$::form{mypage}} = &difftext(\@msg1, \@msg2);
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
		if ($::form{mytouch}) {
			&update_recent_changes;
		}
		&print_header($::form{mypage});
		&print_message($::resource{deleted});
		&print_footer($::form{mypage});
	}
}

sub print_error {
	my ($msg) = @_;
	&print_header($ErrorPage);
	print qq(<p><strong class="error">$msg</strong></p>);
	&print_footer($ErrorPage);
	exit(0);
}

sub print_header {
	my ($page) = @_;
	my $bodyclass = "normal";
	my $editable = 0;
	my $admineditable = 0;
	if (&is_frozen($page) and $::form{cmd} =~ /^(read|write)$/) {
		$editable = 0;
		$admineditable = 1;
		$bodyclass = "frozen";
	} elsif (&is_editable($page) and $::form{cmd} =~ /^(read|write)$/) {
		$admineditable = 1;
		$editable = 1;
	} else {
		$editable = 0;
	}
	my $cookedpage = &encode($page);
	my $escapedpage = &htmlspecialchars($page);
	my $HelpPage = &encode($::resource{help});

	if ($::last_modified != 0) {	# v0.0.9
		$lastmod = &date("Y-m-d H:i:s", (stat($::dataname . "/" . &dbmname($page) . ".txt"))[9]);
	}
	print <<"EOD";
Content-type: text/html; charset=$::charset

<!DOCTYPE html
    PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
    "http://www.w3.org/TR/html4/loose.dtd">
<html lang="$::lang">
<head>
    <meta http-equiv="Content-Language" content="$::lang">
    <meta http-equiv="Content-Type" content="text/html; charset=$::charset">
    <title>$escapedpage @{[&htmlspecialchars(&get_subjectline($page))]}</title>
    <link rel="index" href="$::script?cmd=list">
    <link rev="made" href="mailto:$::modifier_mail">
    <link rel="stylesheet" href="$url_stylesheet" type="text/css" media="screen" charset="Shift_JIS" />
    <link rel="stylesheet" href="blosxom.css" type="text/css" media="screen" charset="Shift_JIS" />
    <link rel="stylesheet" href="print.ja.css" type="text/css" media="print" charset="Shift_JIS" />
</head>
<body class="$bodyclass">
<div id="header">
 <a href="$::modifierlink">$::icontag</a>
<h1 class="title"><a
    title="$::resource{searchthispage}"
    href="$::script?cmd=search&amp;mymsg=$cookedpage">@{[&htmlspecialchars($page)]}</a></h1>
<a href="$::script?$page">$::script?$page</a>
</div>
<div id="navigator">

 [ <a href="$::script?$cookedpage">$::resource{reload}</a> ]
 &nbsp;
 [ <a href="$::script?cmd=newpage">$::resource{createbutton}</a>
 @{[ $editable
   ? qq( | <a title="$::resource{editthispage}" href="$::script?cmd=edit&amp;mypage=$cookedpage">$::resource{editbutton}</a>)
   : qq()
 ]}
 @{[ $admineditable
   ? qq( | <a title="$::resource{admineditthispage}" href="$::script?cmd=adminedit&amp;mypage=$cookedpage">$::resource{admineditbutton}</a>)
   : qq()
 ]}
 @{[ $admineditable
   ? qq( | <a href="$::script?cmd=diff&amp;mypage=$cookedpage">$::resource{diffbutton}</a>)
   : qq()
 ]}
 @{[ (-f "$plugin_dir/attach.inc.pl")
   ? qq( | <a href="$::script?cmd=attach&amp;mode=form&frompage=$cookedpage">$::resource{attachbutton}</a>)
   : qq()
 ]}
 ]
 &nbsp;
 [ <a href="$::script?$::FrontPage">$::resource{top}</a> | 
   <a href="$::script?cmd=list">$::resource{indexbutton}</a> | 
   <a href="$::script?cmd=search">$::resource{searchpage}</a> |
   <a href="$::script?$::RecentChanges">$::resource{recentchangesbutton}</a> |
   <a href="$::script?$HelpPage">$::resource{help}</a> ]
</div>
<hr class="full_hr" />
@{[ $::last_modified == 1
  ? qq(<div id="lastmodified">$::lastmod_prompt $lastmod</div>)
  : q()
]}
EOD
}

my @notes = ();

sub print_footer {
	my ($page) = @_;

	if (@notes) {
		print << "EOD";
<div id="note">
<hr class="note_hr" />
EOD
		my $cnt = 1;
		foreach my $note (@notes) {
			print << "EOD";
<a id="notefoot_$cnt" href="#notetext_$cnt" class="note_super">*$cnt</a>
<span class="small">@{[&inline($note)]}</span>
<br />
EOD
			$cnt++;
		}
		print("</div>\n");
	}
	print <<"EOD";
<hr class="full_hr" />
<div id="toolbar"><a href="$::script?cmd=rss10"><img src="$::modifierlink_data/image/rss.png" border="0" /></a></div>
@{[ $::last_modified == 2
 ? qq(<div id="lastmodified">$::lastmod_prompt $lastmod</div>)
 : qq()
]}
<div id="footer">
Modified by <a href="$::modifierlink">$::modifier</a><br /><br />
<b>"PyukiWiki" $::version</b>
Copyright&copy; 2004 by <a href="http://nekyo.hp.infoseek.co.jp/">Nekyo</a>.<br />
Based on "YukiWiki" 2.1.0 by <a href="http://www.hyuki.com/yukiwiki/">yuki</a>
and <a href="http://pukiwiki.org">"PukiWiki"</a><br />
</div>
</body>
</html>
EOD
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
	print &text_to_html($rawcontent, toc=>1);
}

sub text_to_html {
	my ($txt, %option) = @_;
	my (@txt) = split(/\r?\n/, $txt);
	my (@toc);
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
			# $hn = 'h2', 'h3' or 'h4'
			my $hn = "h" . (length($1) + 1);
			push(@toc, '-' x length($1) . qq( <a href="#i$tocnum">@{[&htmlspecialchars($2)]}</a>\n));
			if ($tocnum == 0) {
				push(@result, splice(@saved), qq(<$hn><a name="i$tocnum"> </a>) . &inline($2) . qq(</$hn>));
			} else {
				push(@result, splice(@saved), qq(<div class="jumpmenu"><a href="#navigator">&uarr;</a></div><$hn><a name="i$tocnum"> </a>) . &inline($2) . qq(</$hn>));
			}
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
		} elsif (/^:([^:]+):(.+)/) {
			&back_push('dl', 1, \@saved, \@result);
			push(@result, '<dt>' . &inline($1) . '</dt>', '<dd>' . &inline($2) . '</dd>');
		} elsif (/^:([^\|]+)\|(.*)/) {
			&back_push('dl', 1, \@saved, \@result);
			push(@result, '<dt>' . &inline($1) . '</dt>', '<dd>' . &inline($2) . '</dd>');
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
		} elsif (/^\,(.*?)[\x0D\x0A]*$/) {
			&back_push('table', 1, \@saved, \@result, ' class="style_table" cellspacing="1" border="0"');
			#######
			# This part is taken from Mr. Ohzaki's Perl Memo and Makio Tsukamoto's WalWiki.
			# XXXXX
			my $tmp = "$1,";
			my @value = map {/^"(.*)"$/ ? scalar($_ = $1, s/""/"/g, $_) : $_} ($tmp =~ /("[^"]*(?:""[^"]*)*"|[^,]*),/g);
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
		} else {
			push(@result, &inline($_));
		#	push(@result, "<br />");	# Thanks wadldw.
		}
	}
	push(@result, splice(@saved));

	if (0) { # $option{toc}) {
		# Convert @toc (table of contents) to HTML.
		# This part is taken from Makio Tsukamoto's WalWiki.
		my (@tocsaved, @tocresult);
		foreach (@toc) {
			if (/^(-{1,3})(.*)/) {
				&back_push('ul', length($1), \@tocsaved, \@tocresult);
				push(@tocresult, '<li>' . $2 . '</li>');
			}
		}
		push(@tocresult, splice(@tocsaved));

		# Insert "table of contents".
		if (@tocresult) {
			unshift(@tocresult, qq(<h2>$::resource{table_of_contents}</h2>));
		}

		return join("\n", @tocresult, @result);
	} else {
		return join("\n", @result);
	}
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
		$line =~ s|\s(\:\))| <img src="$::modifierlink_data/face/smile.png" alt="$1" />|g;
		$line =~ s|\s(\:D)| <img src="$::modifierlink_data/face/bigsmile.png" alt="$1" />|g;
		$line =~ s|\s(\:p)| <img src="$::modifierlink_data/face/huh.png" alt="$1" />|g;
		$line =~ s|\s(\:d)| <img src="$::modifierlink_data/face/huh.png" alt="$1" />|g;
		$line =~ s|\s(XD)| <img src="$::modifierlink_data/face/oh.png" alt="$1" />|g;
		$line =~ s|\s(X\()| <img src="$::modifierlink_data/face/oh.png" alt="$1" />|g;
		$line =~ s|\s(;\))| <img src="$::modifierlink_data/face/wink.png" alt="$1" />|g;
		$line =~ s|\s(;\()| <img src="$::modifierlink_data/face/sad.png" alt="$1" />|g;
		$line =~ s|\s(\:\()| <img src="$::modifierlink_data/face/sad.png" alt="$1" />|g;
		$line =~ s|&heart;|<img src="$::modifierlink_data/face/heart.png" alt="$1" />|g;
	}

	return $line;
}

sub note {
	my ($msg) = @_;

	push(@notes, $msg);
	return "<a id=\"notetext_" . @notes . "\" "
		. "href=\"#notefoot_" . @notes . "\" class=\"note_super\">*"
		. @notes . "</a>";
}

sub make_link {
	my $chunk = shift;
	if ($chunk =~ /^(http|https|ftp):/) {
		if ($use_autoimg and $chunk =~ /\.(gif|png|jpeg|jpg)$/) {
			return qq(<a href="$chunk"><img src="$chunk"></a>);
		} else {
			if ($::use_popup != 0) {	# v0.0.9
				return qq(<a href="$chunk" target="_blank" >$chunk</a>);
			}
			return qq(<a href="$chunk">$chunk</a>);
		}
	} elsif ($chunk =~ /^(mailto):(.*)/) {
		return qq(<a href="$chunk">$2</a>);
	} elsif ($chunk =~ /^$interwiki_definition$/) {
		return qq(<span class="InterWiki">$chunk</span>);
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
		}
		if ($chunk =~ /:(http|https|ftp):/) {
			my @alias = split(/:/, $chunk);		# [[alias>URL]]
			$cookedchunk = &encode($alias[1]);
			$escapedchunk = &htmlspecialchars($alias[0]);
			$chunk = $alias[1];
		}
		if ($chunk =~ /^(http|https|ftp):/) {
			if ($use_autoimg and $chunk =~ /\.(gif|png|jpeg|jpg)$/) {
				return qq(<a href="$chunk"><img src="$escapedchunk"></a>);
			} else {
				return qq(<a href="$chunk">$escapedchunk</a>);
			}
		} elsif ($chunk =~ /^$interwiki_name$/) {
			my ($intername, $localname) = ($1, $2);
			my $remoteurl = $interwiki{$intername};
			if ($remoteurl) {
				$remoteurl =~ s/\b(utf8|euc|sjis|ykwk|asis)\(\$1\)/&interwiki_convert($1, $localname)/e;
				return qq(<a href="$remoteurl">$escapedchunk</a>);
			} else {
				return $escapedchunk;
			}
		} elsif ($::database{$chunk}) {
			my $subject = &htmlspecialchars(&get_subjectline($chunk, delimiter => ''));
			return qq(<a title="$subject" href="$::script?$cookedchunk">$escapedchunk</a>);
		} elsif ($page_command{$chunk}) {
			return qq(<a title="$escapedchunk" href="$::script?$cookedchunk">$escapedchunk</a>);
		} elsif (($chunk =~ /^([^#]*)#/) && $::database{$1}) {
			my $subject = &htmlspecialchars(&get_subjectline($1, delimiter => ''));
			return qq(<a title="$subject" href="$::script?$chunk">$escapedchunk</a>);
		} else {
			return qq($escapedchunk<a title="$::resource{editthispage}" class="editlink" href="$::script?cmd=edit&amp;mypage=$cookedchunk">$editchar</a>);
		}
	}
}

sub print_message {
	my ($msg) = @_;
	print qq(<p><strong>$msg</strong></p>);
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

	if ($page_command{$query}) {
		$::form{cmd} = $page_command{$query};
		$::form{mypage} = $query;
	} elsif ($query =~ /^($wiki_name)$/) {
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

	#
	# $::form{cmd} is frozen here.
	#

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
	if (&is_exist_page($::form{mypage})) {
		unshift(@updates, $update);
	}
	splice(@updates, $::maxrecent + 1);
	$::database{$::RecentChanges} = join("\n", @updates);
	if ($file_touch) {
		open(FILE, "> $file_touch");
		print FILE localtime() . "\n";
		close(FILE);
	}
}

sub get_subjectline {
	my ($page, %option) = @_;
	if (not &is_editable($page)) {
		return "";
	} else {
		# Delimiter check.
		my $delim = $subject_delimiter;
		if (defined($option{delimiter})) {
			$delim = $option{delimiter};
		}

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
		dbmopen(%::database, $::dataname, 0666) or &print_error("(dbmopen) $::dataname");
		dbmopen(%infobase, $infoname, 0666) or &print_error("(dbmopen) $infoname");
	} elsif ($modifier_dbtype eq 'AnyDBM_File') {
		tie(%::database, "AnyDBM_File", $::dataname, O_RDWR|O_CREAT, 0666) or &print_error("(tie AnyDBM_File) $::dataname");
		tie(%infobase, "AnyDBM_File", $infoname, O_RDWR|O_CREAT, 0666) or &print_error("(tie AnyDBM_File) $infoname");
	} else {
		tie(%::database, "Yuki::YukiWikiDB", $::dataname) or &print_error("(tie Yuki::YukiWikiDB) $::dataname");
		tie(%infobase, "Yuki::YukiWikiDB", $infoname) or &print_error("(tie Yuki::YukiWikiDB) $infoname");
	}
}

sub close_db {
	if ($modifier_dbtype eq 'dbmopen') {
		dbmclose(%::database);
		dbmclose(%infobase);
	} elsif ($modifier_dbtype eq 'AnyDBM_File') {
		untie(%::database);
		untie(%infobase);
	} else {
		untie(%::database);
		untie(%infobase);
	}
}

sub open_diff {
	if ($modifier_dbtype eq 'dbmopen') {
		dbmopen(%diffbase, $diffname, 0666) or &print_error("(dbmopen) $diffname");
	} elsif ($modifier_dbtype eq 'AnyDBM_File') {
		tie(%diffbase, "AnyDBM_File", $diffname, O_RDWR|O_CREAT, 0666) or &print_error("(tie AnyDBM_File) $diffname");
	} else {
		tie(%diffbase, "Yuki::YukiWikiDB", $diffname) or &print_error("(tie Yuki::YukiWikiDB) $diffname");
	}
}

sub close_diff {
	if ($modifier_dbtype eq 'dbmopen') {
		dbmclose(%diffbase);
	} elsif ($modifier_dbtype eq 'AnyDBM_File') {
		untie(%diffbase);
	} else {
		untie(%diffbase);
	}
}

sub print_editform {
	my ($mymsg, $conflictchecker, %mode) = @_;
	my $frozen = &is_frozen($::form{mypage});

	if ($::form{mypreview}) {
		if ($::form{mymsg}) {
			unless ($mode{conflict}) {
				print qq(<h3>$::resource{previewtitle}</h3>\n);
				print qq($::resource{previewnotice}\n);
				print qq(<div class="preview">\n);
				&print_content($::form{mymsg});
				print qq(</div>\n);
			}
		} else {
			print qq($::resource{previewempty});
		}
		$mymsg = &htmlspecialchars($::form{mymsg});
	} else {
		$mymsg = &htmlspecialchars($mymsg);
	}

	my $edit = $mode{admin} ? 'adminedit' : 'edit';
	my $escapedmypage = &htmlspecialchars($::form{mypage});
	my $escapedmypassword = &htmlspecialchars($::form{mypassword});

	print <<"EOD";
<form action="$::script" method="post">
  @{[ $mode{admin} ? qq($::resource{frozenpassword} <input type="password" name="mypassword" value="$escapedmypassword" size="10"><br>) : "" ]}
  <input type="hidden" name="myConflictChecker" value="$conflictchecker">
  <input type="hidden" name="mypage" value="$escapedmypage">
  <textarea cols="$cols" rows="$rows" name="mymsg">$mymsg</textarea><br />
@{[
  $mode{admin} ?
  qq(
  <input type="radio" name="myfrozen" value="1" @{[$frozen ? qq(checked="checked") : ""]}>$::resource{frozenbutton}
  <input type="radio" name="myfrozen" value="0" @{[$frozen ? "" : qq(checked="checked")]}>$::resource{notfrozenbutton}<br>)
  : ""
]}
@{[
  $mode{conflict} ? "" :
  qq(
    <input type="checkbox" name="mytouch" value="on" checked="checked">$::resource{touch}<br>
    <input type="submit" name="mypreview_$edit" value="$::resource{previewbutton}">
    <input type="submit" name="mypreview_write" value="$::resource{savebutton}"><br>
  )
]}
</form>
EOD
	unless ($mode{conflict}) {
		# Show the format rule.
		open(FILE, $file_format) or &print_error("($file_format)");
		my $content = join('', <FILE>);
		&code_convert(\$content, $::kanjicode);
		close(FILE);
		print &text_to_html($content, toc=>0);
	}
}

sub print_passwordform {
	print <<"EOD";
<form action="$::script" method="post">
  <input type="hidden" name="cmd" value="adminchangepassword">
  $::resource{oldpassword} <input type="password" name="myoldpassword" size="10"><br>
  $::resource{newpassword} <input type="password" name="mynewpassword" size="10"><br>
  $::resource{newpassword2} <input type="password" name="mynewpassword2" size="10"><br>
  <input type="submit" value="$::resource{changepasswordbutton}"><br>
</form>
EOD
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
	if ($name =~ /^$wiki_name$/) {
		return $name;
	} else {
		return "[[$name]]";
	}
}

# unarmor_name:
#   [[bracket_name]] -> bracket_name
#   WikiName -> WikiName
sub unarmor_name {
	my ($name) = @_;
	if ($name =~ /^$bracket_name$/) {
		return $1;
	} else {
		return $name;
	}
}

sub is_bracket_name {
	my ($name) = @_;
	if ($name =~ /^$bracket_name$/) {
		return 1;
	} else {
		return 0;
	}
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
	&print_header($page);
	&print_content($content);
	&print_editform($rawmsg, $::form{myConflictChecker}, frozen=>0, conflict=>1);
	&print_footer($page);
	return 1;
}

sub get_now {
	my (@week) = qw(Sun Mon Tue Wed Thu Fri Sat);
	my ($sec, $min, $hour, $day, $mon, $year, $weekday) = localtime(time);
	$year += 1900;
	$mon++;
	$mon = "0$mon" if $mon < 10;
	$day = "0$day" if $day < 10;
	$hour = "0$hour" if $hour < 10;
	$min = "0$min" if $min < 10;
	$sec = "0$sec" if $sec < 10;
	$weekday = $week[$weekday];
	return "$year-$mon-$day ($weekday) $hour:$min:$sec";
}

# [[YukiWiki http://www.hyuki.com/yukiwiki/wiki.cgi?euc($1)]]
sub init_InterWikiName {
	my $content = $::database{$InterWikiName};
	while ($content =~ /\[\[(\S+) +(\S+)\]\]/g) {
		my ($name, $url) = ($1, $2);
		$interwiki{$name} = $url;
	}
}

sub interwiki_convert {
	my ($type, $localname) = @_;
	if ($type eq 'sjis' or $type eq 'euc' or $type eq 'utf8') {
		&code_convert(\$localname, $type);
		return &encode($localname);
	} elsif ($type eq 'ykwk') {
		# for YukiWiki1
		if ($localname =~ /^$wiki_name$/) {
			return $localname;
		} else {
			&code_convert(\$localname, 'sjis');
			return &encode("[[" . $localname . "]]");
		}
	} elsif ($type eq 'asis') {
		return $localname;
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
	my ($validpassword_crypt) = &get_info($AdminSpecialPage, $info_AdminPassword);
	return (crypt($givenpassword, $validpassword_crypt) eq $validpassword_crypt) ? 1 : 0;
}

sub is_frozen {
	my ($page) = @_;
	return (&get_info($page, $info_IsFrozen)) ? 1 : 0;
}

sub embedded_to_html {
	my $embedded = shift;

	if ($embedded =~ /$embed_plugin/) {
		my $path = $plugin_dir . $1 . '.inc.pl';
		my $action = '';
		if (-e $path) {
			$action = "\&plugin_" . $1 . "_convert('$3')";
		} else {
			$path = $plugin_dir . $1 . '.pl';
			if (-e $path) {
				$action = "\&$1::plugin_block('$3');";
			}
		}
		if ($action ne '') {
			require $path;
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
		my $path = $plugin_dir . $1 . '.inc.pl';
		my $action = '';
		if (-e $path) {
			$action = "\&plugin_" . $1 . "_inline('$arg')";
		} else {
			$path = $plugin_dir . $1 . '.pl';
			if (-e $path) {
				$action = "\&$1::plugin_inline('$arg');";
			}
		}
		if ($action ne '') {
			require $path;
			$_ = eval $action;
			if ($_) { return $_; }
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
	if ($use_exists) {
		return exists($::database{$name});
	} else {
		return $::database{$name};
	}
}

# Like a PHP.
sub trim {
	my $s = shift;

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
	my $s = shift;
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
