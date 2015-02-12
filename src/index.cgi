#!/usr/bin/perl
#!/usr/local/bin/perl --
#######################################
# index.cgi - This is PyukiWiki.
#
# PyukiWiki Classic Version see also $::version
# Copyright (C) 2004 by Nekyo. http://nekyo.hp.infoseek.co.jp/
# Copyright (C) 2005 PyukiWiki Developers Team. http://pyukiwiki.sourceforge.jp/
#
# Based on YukiWiki <hyuki@hyuki.com> http://www.hyuki.com/yukiwiki/
# Powerd by PukiWiki http://pukiwiki.sourceforge.jp/
# License: GPL2 and/or Artistic or each later version
#
# This program is free software; you can redistribute it and/or
# modify it under the same terms as Perl itself.
# Return:LF Code=EUC-JP 1TAB=4Spaces
#######################################
$::version = '0.1.8';

##
# �饤�֥��
BEGIN {
	push @INC, 'lib';
}

use strict;

##
# $::ini_file ����˻��ꤷ�Ƥ����ȡ����줬ɾ������롣
$::ini_file = 'pyukiwiki.ini.cgi' if ($::ini_file eq '');

use CGI qw(:standard);
#use CGI::Carp qw(fatalsToBrowser);
use Yuki::DiffText qw(difftext);
use Yuki::YukiWikiDB;

eval 'use Socket';
eval 'use FileHandle';

use Jcode;
#use Fcntl;
# Check if the server can use 'AnyDBM_File' or not.
# eval 'use AnyDBM_File';
# my $error_AnyDBM_File = $@;

##
# ����ե������ɹ���
require $::ini_file;

##
# �ƥ�ץ졼�ȥե������ɹ���
$::template_file = 'template.cgi' if ($::template_file eq '');

##############################
# �������
my $modifier_dbtype = 'Yuki::YukiWikiDB';
my $modifier_sendmail = '';
#my $modifier_sendmail = '/usr/sbin/sendmail -t -n';

# ��������
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

##############################
my $editchar = '?';
my $subject_delimiter = ' - ';
my $use_exists = 0; # If you can use 'exists' method for your DB.
##############################
my $interwikiName = 'InterWikiName';
my $AdminChangePassword = 'AdminChangePassword';
my $CompletedSuccessfully = 'CompletedSuccessfully';
my $ErrorPage = 'ErrorPage';

# Wiki������
my $wiki_name = '\b([A-Z][a-z]+[A-Z][a-z]+)\b';
my $bracket_name = '\[\[([^\]]+?)\]\]';
my $embedded_name = '(\#\S+?)';
my $interwiki_definition = '\[\[(\S+?)\ (\S+?)\]\]';	# ? \[\[(\S+) +(\S+)\]\]
my $interwiki_definition2 = '\[(\S+?)\ (\S+?)\]\ (utf8|euc|sjis|yw|asis|raw)';
my $interwiki_name = '([^:]+):([^:].*)';
my $interwiki_name2 = '([^:]+):([^:#].*?)(#.*)?';
#             ^$ascii     +@($domain              |$ip)
my $ismail = '[\x01-\x7F]+\@(([-a-z0-9]+\.)*[a-z]+|\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\])';

# �ץ饰��������
my $embed_plugin = '^\#([^\(]+)(\((.*)\))?';
my $embed_inline = '(&amp;[^;&]+;|&amp;[^)]+\))';

# �ѿ�����
$::info_ConflictChecker = 'ConflictChecker';
my $info_LastModified = 'LastModified';
my $info_IsFrozen = 'IsFrozen';
my $info_AdminPassword = 'AdminPassword';
my %fixedpage = (	# ����ڡ���
	$ErrorPage => 1,
	$::RecentChanges => 1,
	$AdminChangePassword => 1,
	$CompletedSuccessfully => 1,
);
my %fixedplugin = (	# ����
	'newpage' => 1,
	'search' => 1,
	'list' => 1,
);
my %command_do = (	# ���ޥ����̾
	read => \&do_read,
	write => \&do_write,
	createresult => \&do_createresult,
);
$::counter_ext = '.count';	# �����󥿥ե������ĥ��

# �����
$::upload_link = $::upload_dir if (!$::upload_link);
$::conv_start = (times)[0] if ($::enable_convtime != 0);	# ����С��ȥ���������
@::notes = ();												# �������

##
# �ѿ����
my %infobase;
%::diffbase;
%::interwiki;
my $lastmod;	# �ǽ�������
my %_plugined;	# �ץ饰������� 1:Pyuki/2:Yuki/0:None

&main;
exit(0);

##
# �ᥤ�����
sub main {
	%::resource = &read_resource("$::res_dir/resource.$::lang.txt");
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
					&skinex($ret{msg}, $ret{body}, 0);
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

##
# ����ɽ����������
sub skinex {
	my ($page, $body, $is_page) = @_;
	$skin::page    = $page;
	$skin::body    = $body;
	$skin::is_page = $is_page;
	$skin::bodyclass  = "normal";
	$skin::editable      = 0;
	$skin::admineditable = 0;

	if (lc $::form{cmd} eq 'read' || lc $::form{cmd} eq 'write') {
		if (&is_frozen($page)) {
			$skin::admineditable = 1;
			$skin::bodyclass = "frozen";
		} elsif (&is_editable($page)) {
			$skin::admineditable = 1;
			$skin::editable = 1;
		}
	}

	# Thanks moriyoshi koizumi.
	$skin::basehref = "$ENV{'HTTP_HOST'}";
	if (($ENV{'https'} =~ /on/i) || ($ENV{'SERVER_PORT'} eq '443')) {
		$skin::basehref = 'https://' . $skin::basehref;
	} else {
		$skin::basehref = 'http://' . $skin::basehref;
		$skin::basehref .= ":$ENV{'SERVER_PORT'}" if ($ENV{'SERVER_PORT'} ne '80');
	}
	$skin::basehref .= $ENV{'SCRIPT_NAME'};
	if ($skin::basehref ne '') {
		$skin::basehref = '<base href="' . $skin::basehref . '?' . &rawurlencode($page) . "\" />\n";
	}

	# add by nanami. Custom by Nekyo.
	$::gzip_header = '';
	if ($::gzip_path ne '') {
		if (($ENV{'HTTP_ACCEPT_ENCODING'} =~ /gzip/)) {
			$::gzip_header .= "Content-Encoding: " . ($ENV{'HTTP_ACCEPT_ENCODING'} =~ /x-gzip/) ? "x-gzip\n" : "gzip\n";
		}
	}

	$skin::cookedpage  = &::encode($page);
	$skin::escapedpage = &::htmlspecialchars($page);
	$::HelpPage        = &::encode($::resource{help});

	# ��������
	$skin::lastmod1 = '';	# ��ɽ��
	$skin::lastmod2 = '';	# ��ɽ��
	if ($::last_modified != 0) {	# v0.0.9
		$skin::lastmod1 = "<div id=\"lastmodified\">$::lastmod_prompt "
			. &::date("Y-m-d H:i:s", (stat($::data_dir . "/" . &::dbmname($page) . ".txt"))[9]) . "</div>";
		if ($::last_modified == 2) {
			$skin::lastmod2 = $skin::lastmod1;
			$skin::lastmod1 = '';
		}
	}

	# �إå������եå���
	$skin::header = (&::is_exist_page($::Header))
		? '<div id="pageheader">' . &::text_to_html($::database{$::Header}) . '</div>' : '';
	$skin::footer = (&::is_exist_page($::Footer))
		? '<div id="pagefooter">' . &::text_to_html($::database{$::Footer}) . '</div>' : '';

	# skin�����󥸥㡼
	$skin::default_css  = "$::skin_uri/default.css";
	$skin::default_icon = "$::image_dir/pyukiwiki.png";
	$skin::default_menu = $::MenuBar;
	my $tmpl_file       = "$::skin_dir/$::template_file";
	foreach my $key (keys %::skin_chg) {
		if ($page =~ /$key/i) {
			$skin::default_css  = "$::skin_uri/"  . $::skin_chg{$key}{'css'}  if ($::skin_chg{$key}{'css'});
			$skin::default_icon = "$::image_dir/" . $::skin_chg{$key}{'icon'} if ($::skin_chg{$key}{'icon'});
			$skin::default_menu = $::skin_chg{$key}{'menu'}                   if ($::skin_chg{$key}{'menu'});
			$::FrontPage = $::skin_chg{$key}{'FrontPage'} if ($::skin_chg{$key}{'FrontPage'});
			$tmpl_file = $::skin_chg{$key}{'template'} if ($::skin_chg{$key}{'template'});
			last;
		}
	}

	# �Ρ���
	$skin::notes = '';
	if (@::notes) {
		$skin::notes .=<< "EOD";
<div id="note">
<hr class="note_hr" />
EOD
		my $cnt = 1;
		foreach my $note (@::notes) {
			$skin::notes .=<< "EOD";
<a id="notefoot_$cnt" href="#notetext_$cnt" class="note_super">*$cnt</a>
<span class="small">@{[&::inline($note)]}</span>
<br />
EOD
			$cnt++;
		}
		$skin::notes .= "</div>";
	}

	# RSS URL
	$skin::rssurl = $::rssurl ? $::rssurl : "$::script?cmd=rss10";

	# �ʥӥ�����������
	$skin::navi = '';
	$skin::navi .= qq(<a title="$::resource{editthispage}" href="$::script?cmd=edit&amp;mypage=$skin::cookedpage" rel="nofollow">)
		. qq($::resource{editbutton}</a> | ) if ($skin::editable);
	$skin::navi .= qq(<a title="$::resource{admineditthispage}" href="$::script?cmd=adminedit&amp;mypage=$skin::cookedpage">)
		. qq($::resource{admineditbutton}</a> | )
		. qq(<a href="$::script?cmd=diff&amp;mypage=$skin::cookedpage">$::resource{diffbutton}</a> | )
		if ($skin::admineditable);
	$skin::navi .= qq(<a href="$::script?cmd=attach&amp;mypage=$skin::cookedpage">$::resource{attachbutton}</a> | )
		if (-f "$::plugin_dir/attach.inc.pl" || -f "$::secondary_plugin_dir/attach.inc.pl");

	print <<"EOD";
Content-type: text/html; charset=$::charset
$::gzip_header
EOD
	open(STDOUT, "| $::gzip_path") if ($::gzip_header ne '');
	require($tmpl_file);
}

##
# �ڡ���ɽ��
sub do_read {
	&skinex($::form{mypage}, &text_to_html($::database{$::form{mypage}}), 1);
}

##
# ����
sub snapshot {
	my $title = shift;
	my $fp;

	if ($::deny_log) {
		open $fp, ">>$::deny_log";
		print $fp "<<" . $title . ' ' . date("Y-m-d H:i:s") . ">>\n";
		print $fp "HTTP_USER_AGENT:"      . $::ENV{'HTTP_USER_AGENT'}      . "\n";
		print $fp "HTTP_REFERER:"         . $::ENV{'HTTP_REFERER'}         . "\n"; # �ƤӽФ���URL
		print $fp "REMOTE_ADDR:"          . $::ENV{'REMOTE_ADDR'}          . "\n";  # ��⡼��
		print $fp "REMOTE_HOST:"          . $::ENV{'REMOTE_HOST'}          . "\n";
		print $fp "REMOTE_IDENT:"         . $::ENV{'REMOTE_IDENT'}         . "\n";
		print $fp "HTTP_ACCEPT_LANGUAGE:" . $::ENV{'HTTP_ACCEPT_LANGUAGE'} . "\n";
		print $fp "HTTP_ACCEPT:"          . $::ENV{'HTTP_ACCEPT'}          . "\n";
		print $fp "HTTP_HOST:"            . $::ENV{'HTTP_HOST'}            . "\n";
		close $fp;
	}
	if ($::filter_flg == 1) {
		open($fp, "$::cache_dir/black.lst");
		while (<$fp>) {
			tr/\r\n//d;
			s/\./\\\./g;
			if ($_ ne '' && $::ENV{'REMOTE_ADDR'} =~ /$_/i) {
				close($fp);
				return 0;
			}
		}
		close($fp);
		open($fp, ">>$::cache_dir/black.lst");
		print $fp $::ENV{'REMOTE_ADDR'} . "\n";  # ��⡼��
		close $fp;
	}
}

##
# ������ǤΥ��ѥ�ե��륿��
sub spam_filter {
	my ($chk_str, $level) = @_;
	return if ($::filter_flg != 1);	# �ե��륿�����դʤ鲿�⤷�ʤ���
	return if ($chk_str eq '');		# ʸ����̵����в��⤷�ʤ���
	# ����٥�ǽ���ߥ����å���Ԥ���
	if (($::chk_uri_count > 0) && (($chk_str =~ s/https?:\/\///g) > $::chk_uri_count)) {
		&snapshot('Over http');
	# ��٥뤬 1 �λ��Τ� ���ܸ�����å���Ԥ���
	} elsif (($level == 1) && ($::chk_jp_only == 1) && ($chk_str !~ /[��-��-��]/)) {
		&snapshot('No Japanese');
	} else {
		return;
	}
	&skinex($::form{mypage}, &message($::resource{auth_writefobidden}), 0);
	&close_db;
	exit;
}

##
# �ڡ�����¸
sub do_write {
	my ($FrozenWrite, $viewpage) = @_;
	if (not &is_editable($::form{mypage})) {
		&skinex($::form{mypage}, &message($::resource{cantchange}), 0);
		return;
	}
	if ($FrozenWrite ne 'FrozenWrite') {
		return if (&frozen_reject());
	} else {
		# ����°��������Ѥ�
		$::form{myfrozen} = &get_info($::form{mypage}, $info_IsFrozen) ? 1 : 0;
	}
	return if (&conflict($::form{mypage}, $::form{mymsg}));

	# IP�ե��륿���
	if ($::filter_flg == 1) {
		open(FILE, "$::cache_dir/black.lst");
		while (<FILE>) {
			tr/\r\n//d;
			s/\./\\\./g;
			if ($_ ne '' && $::ENV{'REMOTE_ADDR'} =~ /$_/i) {
				&skinex($::form{mypage}, &message($::resource{auth_readfobidden}), 0);
				return 0;
			}
		}
		close(FILE);
	}
	# ��Ͽ����ʸ���� ini �ե������ $disablewords �ǻ��ꡣ���ڤ�ϲ���
	foreach(split(/\n/, $::disablewords)) {
		s/\./\\\./g;
		s/\//\\\//g;
		if ($::form{mymsg} =~ /$_/i) {
			&snapshot('Deny Word');
			&skinex($::form{mypage}, &message($::resource{auth_writefobidden}), 0);
			return 0;
		}
	}

	$::form{mymsg} =~ s/&date;/&date($::date_format)/gex;
	$::form{mymsg} =~ s/&time;/&date($::time_format)/gex;

	# ��ʬ����
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
		&skinex($::form{mypage}, &message($::resource{deleted}), 0);
	}
	return 0;
}

##
# ���顼����ɽ��
sub print_error {
	my ($msg) = @_;
	&skinex($ErrorPage, qq(<p><strong class="error">$msg</strong></p>), 0);
	exit(0);
}

##
# �ü�ʸ���򸵤��᤹��
sub unescape {
	my $s = shift;
	$s =~ s|\&amp;|\&|g;
	$s =~ s|\&lt;|\<|g;
	$s =~ s|\&gt;|\>|g;
	$s =~ s|\&quot;|\"|g;
	return $s;
}

##
# ����ƥ��ɽ��
sub print_content {
	my ($rawcontent) = @_;
	print &text_to_html($rawcontent);
}

##
# �ƥ�����HTML�Ѵ�
sub text_to_html {
	my ($txt) = @_;
	my (@txt) = split(/\r?\n/, $txt);
	my $verbatim;
	my $tocnum = 0;
	my (@saved, @result);
	unshift(@saved, "</p>");
	push(@result, "<p>");

	foreach (@txt) {
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

		my $c = ord($_);	# �ǽ��ʸ���Υ���������
		if ($c == 42) {		# ���ͤˤ�����(ʸ�������ᤤ) ord('*')
			if (/^(\*{1,3})(.+)/) {
				my $hn = "h" . (length($1) + 1);	# $hn = 'h2', 'h3' or 'h4'
				my $hedding = ($tocnum != 0)
					? qq(<div class="jumpmenu"><a href="#navigator">&uarr;</a></div>)
					: '';
				push(@result, splice(@saved),
					$hedding . qq(<$hn><a name="i$tocnum"> </a>) . &inline($2) . qq(</$hn>)
				);
				$tocnum++;
				next;
			}
		} elsif ($c == 45) {	# ord('-')
			if (/^(-{2,3})\($/) {
				if ($& eq '--(') {
					$verbatim = { func => \&inline, done => '--)', class => 'verbatim-soft' };
				} else {
					$verbatim = { func => \&escape, done => '---)', class => 'verbatim-hard' };
				}
				&back_push('pre', 1, \@saved, \@result, " class='$verbatim->{class}'");
				next;
			} elsif (/^----/) {
				push(@result, splice(@saved), '<hr>');
				next;
			} elsif (/^(-{1,3})(.+)/) {
				my $class = "";
				if ($::form{mypage} ne $::MenuBar) {
					$class = " class=\"list" . length($1) . "\" style=\"padding-left:16px;margin-left:16px;\"";
				}
				&back_push('ul', length($1), \@saved, \@result, $class);
				push(@result, '<li>' . &inline($2) . '</li>');
				next;
			}
		} elsif ($c == 123) { # ord('{');
			if (/^{{{/) {	# OpenWiki like.
				$verbatim = { func => \&inline, done => '}}}', class => 'verbatim-soft' };
				&back_push('pre', 1, \@saved, \@result, " class='$verbatim->{class}'");
				next;
			}
		} elsif ($c == 43) {	# ord('+');
			if (/^(\+{1,3})(.+)/) {
				my $class = "";
				if ($::form{mypage} ne $::MenuBar) {
					$class = " class=\"list" . length($1) . "\" style=\"padding-left:16px;margin-left:16px;\"";
				}
				&back_push('ol', length($1), \@saved, \@result, $class);
				push(@result, '<li>' . &inline($2) . '</li>');
				next;
			}
		} elsif ($c == 58) {	# ord(':');
			if (/^:([^:]+):(.+)/) {
				&back_push('dl', 1, \@saved, \@result);
				push(@result, '<dt>' . &inline($1) . '</dt>', '<dd>' . &inline($2) . '</dd>');
				next;
			} elsif (/^:([^\|]+)\|(.*)/) {
				&back_push('dl', 1, \@saved, \@result);
				push(@result, '<dt>' . &inline($1) . '</dt>', '<dd>' . &inline($2) . '</dd>');
				next;
			}
		} elsif ($c == 62) {	# ord('>');
			if (/^(>{1,3})(.+)/) {
				&back_push('blockquote', length($1), \@saved, \@result);
				push(@result, &inline($2));
				next;
			}
		} elsif ($c == 0) {	# (/^$/) {
			push(@result, splice(@saved));
			unshift(@saved, "</p>");
			push(@result, "<p>");
			next;
		} elsif ($c == 32) {	# ord(' ');
			if (/^(\s+.*)$/) {
				&back_push('pre', 1, \@saved, \@result);
				push(@result, &htmlspecialchars($1)); # Not &inline, but &escape
				next;
			}
		} elsif ($c ==  44		# ord(',');
			 ||  $c == 124) {	# ord('|');
			if (/^([\,|\|])(.*?)[\x0D\x0A]*$/) {
				&back_push('table', 1, \@saved, \@result,
					' class="style_table" cellspacing="1" border="0"');
				#######
				# This part is taken from Mr. Ohzaki's Perl Memo and Makio Tsukamoto's WalWiki.
				# XXXXX
				my $delm = "\\$1";	# �ǥ�ߥ��� | �� ,
				my $tmp = ($1 eq ',') ? "$2$1" : "$2";
				# �ǥ�ߥ���ʬ�䤷������˥��å�
				my @value = map {/^"(.*)"$/ ? scalar($_ = $2, s/""/"/g, $_) : $_}
					($tmp =~ /("[^"]*(?:""[^"]*)*"|[^$delm]*)$delm/g);
				my @align = map {(s/^\s+//) ? ((s/\s+$//) ? ' align="center"' : ' align="right"') : ''} @value;
				my @colspan = map {($_ eq '==') ? 0 : 1} @value;
				my $pukicolspan = 1;
				my $thflag = 'td';
				my $value_style = '';
				my @col_style;

				for (my $i = 0; $i < @value; $i++) {
					if ($colspan[$i]) {
						if ($value[$i] eq '~') {		# �ͤ� ~ �����ʤ鲼��Ϣ��
							$value[$i] = '';
						} elsif ($value[$i] =~ /^\~/) {	# ��Ƭ�� ~ �ʤ� th
							$value[$i] =~ s/^\~//g;
							$thflag = 'th';
						} elsif ($value[$i] eq '>') {	# �ͤ� > �����ʤ鱦��Ϣ��
							$value[$i] = '';
							$pukicolspan++;
							next;
						}
						while ($i + $colspan[$i] < @value and $value[$i + $colspan[$i]] eq '==') {
							$colspan[$i]++;
						}
						if ($pukicolspan > 1) {
							$colspan[$i] = $pukicolspan;
							$pukicolspan = 1;
						}
						$colspan[$i] = ($colspan[$i] > 1) ? sprintf(' colspan="%d"', $colspan[$i]) : '';
						$value[$i] =~ s!LEFT\:!\ftext-align:left;\t!g;
						$value[$i] =~ s!CENTER\:!\ftext-align:center;\t!g;
						$value[$i] =~ s!RIGHT\:!\ftext-align:right;\t!g;
						$value[$i] =~ s!BGCOLOR\((.*?)\):(.*)!\fbackground-color:$1;\t$2!g;
						$value[$i] =~ s!COLOR\((.*?)\):(.*)!\fcolor:$1;\t$2!g;
						$value[$i] =~ s!SIZE\((.*?)\):(.*)!\ffont-size:$1px;\t$2!g;

						if ($value[$i] =~ /\f/) {
							$value_style = $value[$i];
							$value_style =~ s!\t\f!!g;
							$value_style =~ s!\t(.*)$!!g;
							$value_style =~ s!\f!!g;
							$value[$i] =~ s/\f(.*?)\t//g;
						}
						if ($tmp =~ /[\,\|]c$/) {
							$col_style[$i] = $value_style;
						} else {
							$value[$i] = sprintf('<%s%s%s class="style_%s" style="%s%s">%s</%s>',
								$thflag, $align[$i], $colspan[$i], $thflag, $col_style[$i], $value_style,
								&inline($value[$i]), $thflag);
							$value_style = '';
						}
					} else {
						$value[$i] = '';
					}
				}
				# ��Ȥ� result �˥ץå��夹�롣
				if ($tmp =~ /[\,\|]h$/) {
					push(@result, join('', '<thead><tr>',@value,'</tr></thead>'));
				} elsif ($tmp =~ /[\,\|]f$/) {
					push(@result, join('', '<tfoot><tr>',@value,'</tr></tfoot>'));
				} elsif ($tmp !~ /[\,\|]c$/) {
					push(@result, join('', '<tr>', @value, '</tr>'));
				}
				next;
			}
		} elsif ($c == 61) {	# ord('=');
			if (/^====/) {
				if ($::form{show} ne 'all') {
					push(@result, splice(@saved), "<a href=\"$::script?cmd=read&mypage="
						. &rawurlencode($::form{mypage}) . "&show=all\">$::resource{continue_msg}</a>");
					last;
				}
				next;
			}
		} elsif ($c == 47) {	# ord('/');
			next if (/^\/\//);	# comment
		} elsif ($c == 76	# ord('L')
			 ||  $c == 67	# ord('C')
			 ||  $c == 82	# ord('R')
			 ||  $c == 66	# ord('B')
			 ||  $c == 71	# ord('G')
		) {
			if (/^(LEFT|CENTER|RIGHT):(.*)$/) {
				push(@result, splice(@saved), "<div style=\"text-align:$1\">$2</div>");
				next;
			} elsif (/^(RED|BLUE|GREEN):(.*)$/) {
				push(@result, splice(@saved), "<font color=\"$1\">$2</font>");
				next;
			}
		}
		push(@result, &inline($_));
	}
	push(@result, splice(@saved));
	return join("\n", @result);
}

sub back_push {
	my ($tag, $level, $savedref, $resultref, $attr) = @_;
	while (@$savedref > $level) {
		push(@$resultref, shift(@$savedref));
	}
	push(@$resultref, splice(@$savedref)) if ($savedref->[0] ne "</$tag>");
	while (@$savedref < $level) {
		unshift(@$savedref, "</$tag>");
		push(@$resultref, "<$tag$attr>");
	}
}

##
# ����饤��Ÿ��
sub inline {
	my ($line) = @_;
	$line = &htmlspecialchars($line);
	$line =~ s|'''([^']+?)'''|<em>$1</em>|g;		# Italic
	$line =~ s|''([^']+?)''|<strong>$1</strong>|g;	# Bold
	$line =~ s|%%%([^%]*)%%%|<ins>$1</ins>|g;		# Insert Line
	$line =~ s|%%([^%]*)%%|<del>$1</del>|g;			# Delete Line
	$line =~ s|\^\^([^\^]*)\^\^|<sup>$1</sup>|g;	# sup
	$line =~ s|__([^_]*)__|<sub>$1</sub>|g;			# sub
	$line =~ s|~$|<br />|g;							# ~\n -> <br />
	$line =~ s|\(\((.*)\)\)|&note($1)|gex;
	$line =~ s|\[\#(.*)\]|<a class="anchor_super" id="$1" href="#$1" title="$1">$::_symbol_anchor</a>|g;
	$line =~ s|(\d\d\d\d-\d\d-\d\d \(\w\w\w\) \d\d:\d\d:\d\d)|<span class="date">$1</span>|g;	# Date

	if ($line =~ /^$embedded_name$/) {
		$line =~ s!^$embedded_name$!&embedded_to_html($1)!gex;	# #command
	} else {
		$line =~ s!
			(($bracket_name)			# [[likethis]], [[Friend:remotelink]]
			|($interwiki_definition)	# [[Friend http://somewhere/?q=sjis($1)]]
			|((https?|ftp):([^\x00-\x20()<>\x7F-\xFF\]])*)	# Direct http://...
			|($wiki_name)				# LocalLinkLikeThis
			|($embed_inline)			# &user_defined_plugin(123,hello)
			|($ismail)
			)!&make_link($1)!gex;
	}
	$line = &plugin_facemark_convert($line) if (&exist_plugin('facemark') == 1);
	return $line;
}

##
# ���ɽ��
sub note {
	my ($msg) = @_;

	push(@::notes, $msg);
	return "<a id=\"notetext_" . @::notes . "\" "
		. "href=\"#notefoot_" . @::notes . "\" class=\"note_super\">*"
		. @::notes . "</a>";
}

##
# ��󥯺���
sub make_link {
	my $chunk = shift;
	my $res;
	my $target = $::use_popup != 0 ? qq( target="_blank") : '';

	if ($chunk =~ /^(https?|ftp):/) {
		if (&exist_plugin('img') == 1) {
			$res = &plugin_img_convert("$chunk,module");
			return $res if ($res ne '');
		}
		return qq(<a href="$chunk"$target>$chunk</a>);
	} elsif ($chunk =~ /^$interwiki_definition2$/) {
		return qq(<span class="InterWiki"><a href="$1">$2</a> $3</span>);
	} elsif ($chunk =~ /$embed_inline/) {
		return &embedded_inline($1)
	} else {
		$chunk = &unarmor_name($chunk);
		$chunk = &unescape($chunk); # To treat '&' or '>' or '<' correctly.
		my $cookedchunk = &rawurlencode($chunk);
		my $escapedchunk = &htmlspecialchars($chunk);
		if ($chunk =~ /(.+?)>(.+)/ or $chunk =~ /(.+?):(.+)/) {	# v0.1.4
			$escapedchunk = &htmlspecialchars($1);
			if ($escapedchunk =~ /\.(gif|png|jpe?g)$/) {
				$escapedchunk = "<img src=\"$escapedchunk\">";
			}
			$chunk = $2;
			if ($2 =~ /$ismail/) {
				$escapedchunk = $chunk   if ($escapedchunk =~ /^mailto/);
				$chunk = "mailto:$chunk" if ($chunk !~ /^mailto:/);
				return qq(<a href="$chunk">$escapedchunk</a>);
			} elsif (($chunk =~ /(https?|ftp):.*/) or !$::interwiki{$1}) {
				$cookedchunk = &rawurlencode($chunk);
			}
		} elsif ($chunk =~ /^($ismail)/) {
			return qq(<a href="mailto:$chunk">$chunk</a>);
		}
		if ($chunk =~ /^(https?|ftp):/) {
			if (&exist_plugin('img') == 1) {
				$res = &plugin_img_convert("$chunk,module");
				return $res if ($res ne '');
			}
			return qq(<a href="$chunk">$escapedchunk</a>);
		} elsif ($chunk =~ /^$interwiki_name2$/) {
			my ($intername, $keyword, $anchor) = ($1, $2, $3);
			if (exists $::interwiki2{$intername}) {
				my ($code, $url) = %{$::interwiki2{$intername}};
				$url =~ s/\$1/&interwiki_convert($code, $keyword)/e;
				$url = &htmlspecialchars($url.$anchor);
				return qq(<a href="$url"$target>$escapedchunk</a>);
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
		$cookedchunk = &rawurlencode($chunk);
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

##
# �����������
sub init_form {
	my @params = param();
	if (@params) {
		foreach my $var (@params) {
			$::form{$var} = param($var);
		}
	} else {
		$ENV{QUERY_STRING} = $::FrontPage;
	}

	# Thanks Mr.koizumi. v0.1.4
	my $query = $ENV{QUERY_STRING};
	if (0 <= index($query, '&')) {
		my @querys = split(/&/, $query);
		foreach (@querys) {
			$_ = &rawurldecode($_);
			$::form{$1} = $2 if (/([^=]*)=(.*)$/);
		}
	} else {
		$query = &rawurldecode($query);
	}

	if ($query =~ /^($wiki_name)$/ || $::database{$query}) {
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
	$::form{mymsg}  = &code_convert(\$::form{mymsg},  $::kanjicode);
	$::form{myname} = &code_convert(\$::form{myname}, $::kanjicode);
}

##
# �ǽ�����������
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
	return "" if (not &is_editable($page));
	# Delimiter check.
	my $delim = $subject_delimiter;
	$delim = $option{delimiter} if (defined($option{delimiter}));
	# Get the subject of the page.
	my $subject = $::database{$page};
	$subject =~ s/\r?\n.*//s;
	return "$delim$subject";
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

##
# DB�Υ����ץ� ���⥸�塼�벽������٤��ʤ롣
sub open_db {
	if ($modifier_dbtype eq 'dbmopen') {
		dbmopen(%::database, $::data_dir, 0666) or &print_error("(dbmopen) $::data_dir");
		dbmopen(%infobase,   $::info_dir, 0666) or &print_error("(dbmopen) $::info_dir");
#	} elsif ($modifier_dbtype eq 'AnyDBM_File') {
#		tie(%::database, "AnyDBM_File", $::data_dir, O_RDWR|O_CREAT, 0666) or &print_error("(tie AnyDBM_File) $::data_dir");
#		tie(%infobase,   "AnyDBM_File", $::info_dir, O_RDWR|O_CREAT, 0666) or &print_error("(tie AnyDBM_File) $::info_dir");
	} else {
		tie(%::database, $modifier_dbtype, $::data_dir) or &print_error("(tie $modifier_dbtype) $::data_dir");
		tie(%infobase,   $modifier_dbtype, $::info_dir) or &print_error("(tie $modifier_dbtype) $::info_dir");
	}
}

##
# DB�Υ�����
sub close_db {
	if ($modifier_dbtype eq 'dbmopen') {
		dbmclose(%::database);
		dbmclose(%infobase);
	} else {
		untie(%::database);
		untie(%infobase);
	}
}

sub open_diff {
	if ($modifier_dbtype eq 'dbmopen') {
		dbmopen(%::diffbase, $::diff_dir, 0666) or &print_error("(dbmopen) $::diff_dir");
#	} elsif ($modifier_dbtype eq 'AnyDBM_File') {
#		tie(%::diffbase, "AnyDBM_File", $::diff_dir, O_RDWR|O_CREAT, 0666) or &print_error("(tie AnyDBM_File) $::diff_dir");
	} else {
		tie(%::diffbase, $modifier_dbtype, $::diff_dir) or &print_error("(tie $modifier_dbtype) $::diff_dir");
	}
}

sub close_diff {
	if ($modifier_dbtype eq 'dbmopen') {
		dbmclose(%::diffbase);
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
	} elsif ($page =~ /[\n\r\f\t]/) {
		return 0;
	} elsif ($page =~ /^\s/) {
		return 0;
	} elsif ($page =~ /\s$/) {
		return 0;
	} elsif ($page =~ /^\#/) {
		return 0;
	} elsif ($page =~ /(^|\/)\.{1,2}(\/|$)/) { # ./ ../ is ng
		return 0;
	} elsif (not $page) {
		return 0;
	} else {
		return 1;
	}
}

##
# WikiName �� �֥�󥱥å�([[]])�ɲ�
sub armor_name {
	my ($name) = @_;
	return ($name =~ /^$wiki_name$/) ? $name : "[[$name]]";
}

##
# �֥�󥱥å�([[]])�����
sub unarmor_name {
	my ($name) = @_;
	return ($name =~ /^$bracket_name$/) ? $1 : $name;
}

##
# �֥�󥱥å��դ�����ǧ
sub is_bracket_name {
	my ($name) = @_;
	return ($name =~ /^$bracket_name$/) ? 1 : 0;
}

##
# �ڡ���̾��DB�ե�����̾���Ѵ�
sub dbmname {
	my ($name) = @_;
	$name =~ s/(.)/uc unpack('H2', $1)/eg;
	return $name;
}

##
# �꥽�������ɹ������ѥ롼����
sub read_resource {
	my ($file, %buf) = @_;
	open(FILE, $file) or &print_error("(resource:$file)");
	while (<FILE>) {
		next if /^#/;
		tr/\r\n//d;
		my ($key, $value) = split(/=/, $_, 2);
		$buf{$key} = &code_convert(\$value, $::kanjicode);
	}
	close(FILE);
	return %buf;
}

##
# ����
sub conflict {
	my ($page, $rawmsg) = @_;
	return 0 if ($::form{myConflictChecker} eq &get_info($page, $::info_ConflictChecker));
	open(FILE, "$::res_dir/conflict.$::lang.txt") or &print_error("(conflict)");
	my $content = join('', <FILE>);
	&code_convert(\$content, $::kanjicode);
	close(FILE);

	my $body = &text_to_html($content);
	if (&exist_plugin('edit') == 1) {
		$body .= &editform($rawmsg, $::form{myConflictChecker}, frozen=>0, conflict=>1);
	}
	&skinex($page, $body, 0);
	return 1;
}

##
# ���߻������
sub get_now {
	return date("Y-m-d (D) H:i:s");
}

##
# InterWikiName �����
# YukiWiki���� [[YukiWiki http://www.hyuki.com/yukiwiki/wiki.cgi?euc($1)]]
# PukiWiki���� [http://www.hyuki.com/yukiwiki/wiki.cgi?$1 YukiWiki] euc
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
		return &rawurlencode($localname);
	} elsif (($type eq 'ykwk') || ($type eq 'yw')) {
		# for YukiWiki1
		if ($localname =~ /^$wiki_name$/) {
			return $localname;
		} else {
			&code_convert(\$localname, 'sjis');
			return &rawurlencode("[[" . $localname . "]]");
		}
	} else {
		return $localname;
	}
}

##
# �ղþ������
sub get_info {
	my ($page, $key) = @_;
	my %info = map { split(/=/, $_, 2) } split(/\n/, $infobase{$page});
	return $info{$key};
}

##
# �ղþ�������
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

##
# �������å�
sub frozen_reject {
	my ($isfrozen) = &get_info($::form{mypage}, $info_IsFrozen);
	my ($willbefrozen) = $::form{myfrozen};
	if (not $isfrozen and not $willbefrozen) {		# You need no check.
		return 0;
	} elsif (valid_password($::form{mypassword})) {	# You are admin.
		return 0;
	} else {
		&print_error($::resource{passworderror});
		return 1;
	}
}

##
# �ѥ���ɳ�ǧ
sub valid_password {
	my ($givenpassword) = @_;
	return (crypt($givenpassword, "AA") eq $::adminpass) ? 1 : 0;
}

##
# ����ǧ
sub is_frozen {
	my ($page) = @_;
	return (&get_info($page, $info_IsFrozen)) ? 1 : 0;
}

##
# �ץ饰����Ÿ��
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

##
# ����饤��Ÿ��
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

##
# ʸ���������Ѵ�
sub code_convert {
	my ($contentref, $kanjicode) = @_;
	if ($::lang eq 'ja') {
		&Jcode::convert($contentref, $kanjicode);	# for Jcode.pm
	}
	return $$contentref;
}

##
# �ڡ���¸�߳�ǧ
sub is_exist_page {
	my ($name) = @_;
	return ($use_exists) ? exists($::database{$name}) : $::database{$name};
}


##############################
# ���̸ߴ���

##
# �ü�ʸ���� HTML ����ƥ��ƥ����Ѵ����롣'&' �� '&amp;' ��
sub escape {
	return &htmlspecialchars(shift);
}

##
# RFC1738�˴�Ť�URL���󥳡��ɤ�Ԥ���foo bar@baz �� foo%20bar%40baz
sub decode {
	return &rawurldecode(@_);
}

##
# URL���󥳡��ɤ��줿ʸ�����ǥ����ɤ��롣foo%20bar%40baz �� foo bar@baz
sub encode {
	return &rawurlencode(@_);
}

##
# Plugin���б�����JavaScript�ɹ���ʸ�����������롣
sub jscss_include {
	my ($res, $rel, $js, $css, $onload, $onunload);
	foreach (keys %_plugined) {
		$js = $_ . '.js';
		if (-e "$::js_dir/$js") {
			$res .= '<script type="text/javascript" src="' . $::js_uri . '/' . $js . '"></script>' . "\n";
		}
		if ($::extend_js{$_}{'js'} ne '') {
			$res .= '<script type="text/javascript" src="' . $::extend_js{$_}{'js'} . '"';
			if ($::extend_js{$_}{'charset'} ne '') {
				$res .= ' charset="' . $::extend_js{$_}{'charset'} . '"';
			}
			$res .= '></script>' . "\n";
		}
		if ($::extend_js{$_}{'onload'} ne '') {
			$onload .= $::extend_js{$_}{'onload'};
		}
		if ($::extend_js{$_}{'onunload'} ne '') {
			$onunload .= $::extend_js{$_}{'onunload'};
		}
		$css = $_ . '.css';
		if (-e "$::css_dir/$css") {
			$rel .= '<link rel="stylesheet" href="' . $::css_uri . '/' . $css
				. '" type="text/css" media="screen" charset="Shift_JIS" />' . "\n";
		}
	}
	if ($onload ne '') {
		$::bodyattr .= ' onload="' . $onload . '"';
	}
	if ($onunload ne '') {
		$::bodyattr .= ' onunload="' . $onunload . '"';
	}
	return $res . $rel;
}

##############################
# PukiWiki���ؿ�

##
# �ץ饰�����¸�߳�ǧ
sub exist_plugin {
	my ($plugin) = @_;

	if (!$_plugined{$plugin}) {
		my $path = "$::plugin_dir/$plugin" . '.inc.pl';
		if (-e $path) {
			require $path;
			$_plugined{$plugin} = 1;	# Pyuki
			$path = "$::res_dir/$plugin.$::lang.txt";
			%::resource = &read_resource($path, %::resource) if (-r $path);
			return 1;
		} else {
			$path = "$::plugin_dir/$plugin" . '.pl';
			if (-e $path) {
				require $path;
				$_plugined{$plugin} = 2;	# Yuki
				$path = "$::res_dir/$plugin.$::lang.txt";
				%::resource = &read_resource($path, %::resource) if (-r $path);
				return 2;

			# �������������
			} elsif ($::secondary_plugin_dir) {
				$path = "$::secondary_plugin_dir/$plugin" . '.inc.pl';
				if (-e $path) {
					require $path;
					$_plugined{$plugin} = 1;	# Pyuki
					$path = "$::res_dir/$plugin.$::lang.txt";
					%::resource = &read_resource($path, %::resource) if (-r $path);
					return 1;
				} else {
					$path = "$::secondary_plugin_dir/$plugin" . '.pl';
					if (-e $path) {
						require $path;
						$_plugined{$plugin} = 2;	# Yuki
						$path = "$::res_dir/$plugin.$::lang.txt";
						%::resource = &read_resource($path, %::resource) if (-r $path);
						return 2;
					}
				}
			}
		}
		return 0;
	}
	return $_plugined{$plugin};
}

##
# �ץ饰�������Ÿ����ɬ�������� shift �Ȥ��롣
sub func_get_args {
	my @args = split(/,/, shift);
	for (my $i = 0; $i < @args; $i++) {
		$args[$i] = trim($args[$i]);
	}
	return @args;
}

##############################
# PHP�ߴ��ؿ�

##
# fopen hosts �б����ѿ�
my $hosts_exist = 0;
my %hosts;

##
# �ե�����ޤ���URL�򥪡��ץ󤹤�
sub fopen {
	my ($fname, $fmode) = @_;
	my $_fname;
	my $fp;

	# HTTP: ���ä���
	if (substr($fname, 0, 7) eq 'http://') {
		$fname =~ m!(http:)?(//)?([^:/]*)?(:([0-9]+)?)?(/.*)?!;
		my $host = ($3 ne "") ? $3 : "localhost";
		my $port = ($5 ne "") ? $5 : 80;
		my $path = ($6 ne "") ? $6 : "/";
		my $useproxy = 0;
		if ($::proxy_host) {
			$useproxy = 1;

			# �㳰(�ץ������̤��ʤ����ɥ쥹)
			foreach(split(/\n/, $::noproxy)) {
				s/\./\\\./g;
				s/\//\\\//g;
				if ($host =~ /$_/i) {
					$useproxy = 0;
					last;
				}
			}
		}
		if ($useproxy) {
			$host = $::proxy_host;
			$port = $::proxy_port;
			$path = $fname;
		}
		my ($sockaddr, $ip);
		$fp = new FileHandle;

		# hosts ��ǽ(infoseek �� DNSŸ������ʤ����� hosts �����Ѥ��롣)
		if ($hosts_exist == 0) {	# hosts ���ɤ�Ǥ��ʤ���
			# hosts �� �꥽�����ǥ��쥯�ȥ�� hosts.cgi ���ꡣ
			my $hosts_path = $::res_dir . '/hosts.cgi';
			$hosts_exist = 2;	# �ե����롦�ǡ�����¸�ߤ��ʤ��ä���
			if (-f $hosts_path) {
				if (open(FILE, $hosts_path)) {
					while (<FILE>) {
						next if /^#/; # ��Ƭ # �ʤ饳����
						tr/\r\n//d;
						# IP URL alias ��̵��
						if (/(\d+\.\d+\.\d+\.\d+)\s+([^\s]+)/) {
							$hosts{$2} = $1;
							$hosts_exist = 1;	# �ǡ�����¸�ߤ�����
						}
					}
					close(FILE);
				}
			}
		}
		if (($hosts_exist == 1) && ($hosts{$host})) { # �����������
			$host = $hosts{$host}; # hosts ͥ����֤�����
		}

		if ($host =~ /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/) {
			$ip = pack('C4', split(/\./, $host));
		} else {
			#HOST̾��IP��ľ��
		#	$ip = (gethostbyname($host))[4] || return (1, "Host Not Found.");
			$ip = inet_aton($host) || return 0;	# Host Not Found.
		}
		$sockaddr = pack_sockaddr_in($port, $ip) || return 0; # Can't Create Socket address.
		eval 'socket($fp, PF_INET, SOCK_STREAM, 0)';
		connect($fp, $sockaddr) || return 0;	# Can't connect Server.
		autoflush $fp(1);
		print $fp "GET $path HTTP/1.1\r\nHost: $host\r\n\r\n";
		return $fp;
	} else {
		$fmode = lc($fmode);
		if ($fmode eq 'w') {
			$_fname = ">$fname";
		} elsif ($fmode eq 'w+') {
			$_fname = "+>$fname";
		} elsif ($fmode eq 'a') {
			$_fname = ">>$fname";
		} elsif ($fmode eq 'r') {
			$_fname = $fname;
		} else {
			return 0;
		}
		if (open($fp, $_fname)) {
			return $fp;
		}
	}
	return 0;
}

##
# ʸ�������Ƭ����������ˤ���ۥ磻�ȥ��ڡ������������
sub trim {
	my ($s) = @_;
	$s =~ s/^\s*(\S+)\s*$/$1/o; # trim
	return $s;
}

##
# ���դ� Unix �Υ����ॹ����פȤ��Ƽ�������
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
	$days += $day - 1;
	return (((($days * 24) + $hour) * 60) + $min) * 60 + $sec;
}

##
# RFC1738�˴�Ť�URL���󥳡��ɤ�Ԥ���foo bar@baz �� foo%20bar%40baz
sub rawurlencode {
	my ($encoded) = @_;
	$encoded =~ s/(\W)/'%' . unpack('H2', $1)/eg;
	return $encoded;
}

##
# URL���󥳡��ɤ��줿ʸ�����ǥ����ɤ��롣foo%20bar%40baz �� foo bar@baz
sub rawurldecode {
	my ($s) = @_;
	$s =~ tr/+/ /;
	$s =~ s/%([A-Fa-f0-9][A-Fa-f0-9])/pack("C", hex($1))/eg;
	return $s;
}

##
# �ü�ʸ���� HTML ����ƥ��ƥ����Ѵ����롣'&' �� '&amp;' ��
sub htmlspecialchars {
	my ($s) = @_;
	$s =~ tr|\r||d;
	$s =~ s|\&|&amp;|g;
	$s =~ s|<|&lt;|g;
	$s =~ s|>|&gt;|g if($s=~/</);	# nanami add
	$s =~ s|"|&quot;|g;
	return $s;
}

##
# �����������/�����񼰲�����
sub date
{
	my ($format, $tm) = @_;

	# yday:0-365 $isdst Summertime:1/not:0
	my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = ((@_ > 1) ? localtime($tm) : localtime);
	$year += 1900;	#
	my ($hr12, $ampm) = $hour >= 12 ? ($hour - 12, 'pm') : ($hour, 'am');
	my $month = ('January','February','March','April','May','June','July','August','September','October','November','December')[$mon];
	my $weekday = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')[$wday];
													# year
	$format =~ s/Y/$year/ge;						# Y:4char ex)1999 or 2003
	$format =~ s/y/sprintf("%02d", $year % 100)/ge;	# y:2char ex)99 or 03
													# month
	$mon++;											# mon is 0 to 11 add 1
	$format =~ s/n/$mon/ge;							# n:1-12
	$format =~ s/m/sprintf("%02d", $mon)/ge;		# m:01-12
	$format =~ s/M/substr($month, 0, 3)/ge;			# M:Jan-Dec
	$format =~ s/F/$month/ge;						# F:January-December
													# day
	$format =~ s/j/$mday/ge;						# j:1-31
	$format =~ s/d/sprintf("%02d", $mday)/ge;		# d:01-31
													# hour
	$format =~ s/g/$hr12/ge;						# g:1-12
	$format =~ s/G/$hour/ge;						# G:0-23
	$format =~ s/h/sprintf("%02d", $hr12)/ge;		# h:01-12
	$format =~ s/H/sprintf("%02d", $hour)/ge;		# H:00-23
													# minutes
	$format =~ s/i/sprintf("%02d", $min)/ge;		# i:00-59
													# second
	$format =~ s/s/sprintf("%02d", $sec)/ge;		# s:00-59
	$format =~ s/a/$ampm/ge;						# a:am or pm
	$format =~ s/A/uc $ampm/ge;						# A:AM or PM
	$format =~ s/w/$wday/ge;						# w:0(Sunday)-6(Saturday)
	$format =~ s/l/$weekday/ge;						# l(lower L):Sunday-Saturday
	$format =~ s/D/substr($weekday, 0, 3)/ge;		# D:Mon-Sun
	$format =~ s/I/$isdst/ge;						# I(Upper i):1 Summertime/0:Not

	# Not Allowed
	# L ��ǯ�Ǥ��뤫�ɤ�����ɽ�������͡� 1�ʤ鱼ǯ��0�ʤ鱼ǯ�ǤϤʤ��� 
	# O ����˥å�ɸ���(GMT)�Ȥλ��ֺ� Example: +0200 
	# r RFC 822 �ե����ޥåȤ��줿���� Example: Thu, 21 Dec 2000 16:01:07 +0200 
	# S �Ѹ�����ν�����ɽ�����ե��å�����2 ʸ���� st, nd, rd or th. Works well with j  
	# T ���Υޥ�����Υ����ॾ��������ꡣ Examples: EST, MDT ... 
	# U Unix ��(1970ǯ1��1��0��0ʬ0��)������ÿ� See also time() 
	# W ISO-8601 �������˻Ϥޤ�ǯñ�̤ν��ֹ� (PHP 4.1.0���ɲ�) Example: 42 (the 42nd week in the year) 
	$format =~ s/z/$yday/ge;	# z:days/year 0-366
	return $format;
}

1;
__END__
