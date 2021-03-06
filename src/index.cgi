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
$::version = '0.1.9';

##
# ライブラリ
BEGIN {
	push @INC, 'lib';
}

use strict;

##
# $::ini_file を先に指定しておくと、それが評価される。
$::ini_file = 'pyukiwiki.ini.cgi' if ($::ini_file eq '');

use CGI qw(:standard);
#use CGI::Carp qw(fatalsToBrowser);
use Yuki::DiffText qw(difftext);
use Yuki::YukiWikiDB;

eval 'use Socket';
eval 'use FileHandle';

use Jcode;

##
# 設定ファイル読込み
require $::ini_file;

##
# テンプレートファイル読込み
$::template_file = 'template.cgi' if ($::template_file eq '');

##############################
# 初期設定
my $modifier_dbtype = 'Yuki::YukiWikiDB';
my $modifier_sendmail = '';
#my $modifier_sendmail = '/usr/sbin/sendmail -t -n';

# 言語設定
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

# Wikiの設定
my $wiki_name = '\b([A-Z][a-z]+[A-Z][a-z]+)\b';
my $bracket_name = '\[\[([^\]]+?)\]\]';
my $embedded_name = '(\#\S+?)';
my $interwiki_definition = '\[\[(\S+?)\ (\S+?)\]\]';	# ? \[\[(\S+) +(\S+)\]\]
my $interwiki_definition2 = '\[(\S+?)\ (\S+?)\]\ (utf8|euc|sjis|yw|asis|raw)';
my $interwiki_name = '([^:]+):([^:].*)';
my $interwiki_name2 = '([^:]+):([^:#].*?)(#.*)?';
#             ^$ascii     +@($domain              |$ip)
my $ismail = '[\x01-\x7F]+\@(([-a-z0-9]+\.)*[a-z]+|\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\])';

# プラグイン設定
my $embed_plugin = '^\#([^\(]+)(\((.*)\))?';
my $embed_inline = '(&amp;[^;&]+;|&amp;[^)]+\))';

# 変数設定
$::info_ConflictChecker = 'ConflictChecker';
my $info_LastModified = 'LastModified';
my $info_IsFrozen = 'IsFrozen';
my $info_AdminPassword = 'AdminPassword';
my %fixedpage = (	# 固定ページ
	$ErrorPage => 1,
	$AdminChangePassword => 1,
	$CompletedSuccessfully => 1,
);
my %fixedplugin = (	# 固定
	'newpage' => 1,
	'search' => 1,
	'list' => 1,
);
my %command_do = (	# コマンド別名
	read => \&do_read,
	write => \&do_write,
	createresult => \&do_createresult,
);
$::counter_ext = '.count';	# カウンタファイル拡張子

# 初期化
$::upload_link = $::upload_dir if (!$::upload_link);
$::conv_start = (times)[0] if ($::enable_convtime != 0);	# コンバートタイム初期化
@::notes = ();												# 注釈初期化

##
# 変数定義
%::diffbase;
%::interwiki;
my $lastmod;	# 最終更新日
my %_plugined;	# プラグイン種別 1:Pyuki/2:Yuki/0:None

&main;
exit(0);

##
# メイン処理
sub main {
	%::resource = &read_resource("$::res_dir/resource.$::lang.txt");

	# ディレクトリ検査
	my $err = '';
	$err .= "Directory is not found or not writable ($::data_dir)<br />\n" if (!-w $::data_dir);
	$err .= "Directory is not found or not writable ($::diff_dir)<br />\n" if (!-w $::diff_dir);
	$err .= "Directory is not found or not writable ($::cache_dir)<br />\n" if (!-w $::cache_dir);
	$err .= "Directory is not found or not writable ($::counter_dir)<br />\n" if (!-w $::counter_dir);
	$err .= "Directory is not found or not writable ($::upload_dir)<br />\n" if (!-w $::upload_dir);
	&print_error($err) if ($err ne '');

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
# 画面表示の前処理
sub skinex {
	my ($page, $body, $is_page) = @_;
	$skin::page    = $page;
	$skin::body    = $body;
	$skin::is_page = $is_page;
	$skin::bodyclass  = "normal";
	$skin::editable      = 0;
	$skin::admineditable = 0;

#	$skin::body =~ s/\n?#freeze\r?\n//g;

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
		if ($::IndexPage eq $page) {
			$skin::basehref = '<base href="' . $skin::basehref . "?cmd=list\" />\n";
		} else {
			$skin::basehref = '<base href="' . $skin::basehref . '?' . &rawurlencode($page) . "\" />\n";
		}
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

	# 更新日付
	$skin::lastmod1 = '';	# 前表示
	$skin::lastmod2 = '';	# 後表示
	if ($::last_modified != 0) {	# v0.0.9
		$skin::lastmod1 = "<div id=\"lastmodified\">$::lastmod_prompt "
			. &::date("Y-m-d H:i:s", (stat($::data_dir . "/" . &::dbmname($page) . ".txt"))[9]) . "</div>";
		if ($::last_modified == 2) {
			$skin::lastmod2 = $skin::lastmod1;
			$skin::lastmod1 = '';
		}
	}

	# ヘッダー、フッター
	$skin::header = (&::is_exist_page($::Header))
		? '<div id="pageheader">' . &::text_to_html($::database{$::Header}) . '</div>' : '';
	$skin::footer = (&::is_exist_page($::Footer))
		? '<div id="pagefooter">' . &::text_to_html($::database{$::Footer}) . '</div>' : '';

	# skinチェンジャー
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

	# ノート
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

	# ナビゲーション作成
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
# ページ表示
sub do_read {
	&skinex($::form{mypage}, &text_to_html($::database{$::form{mypage}}), 1);
}

##
# ロギング
sub snapshot {
	my $title = shift;
	my $fp;

	if ($::deny_log) {
		open $fp, ">>$::deny_log";
		print $fp "<<" . $title . ' ' . date("Y-m-d H:i:s") . ">>\n";
		print $fp "HTTP_USER_AGENT:"      . $::ENV{'HTTP_USER_AGENT'}      . "\n";
		print $fp "HTTP_REFERER:"         . $::ENV{'HTTP_REFERER'}         . "\n"; # 呼び出し元URL
		print $fp "REMOTE_ADDR:"          . $::ENV{'REMOTE_ADDR'}          . "\n";  # リモート
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
		print $fp $::ENV{'REMOTE_ADDR'} . "\n";  # リモート
		close $fp;
	}
}

##
# 投稿等でのスパムフィルター
sub spam_filter {
	my ($chk_str, $level) = @_;
	return if ($::filter_flg != 1);	# フィルターオフなら何もしない。
	return if ($chk_str eq '');		# 文字列が無ければ何もしない。
	# 全レベルで書込みチェックを行う。
	if (($::chk_uri_count > 0) && (($chk_str =~ s/https?:\/\///g) > $::chk_uri_count)) {
		&snapshot('Over http');
	# レベルが 1 の時のみ 日本語チェックを行う。
	} elsif (($level == 1) && ($::chk_jp_only == 1) && ($chk_str !~ /[あ-んア-ン]/)) {
		&snapshot('No Japanese');
	} else {
		return;
	}
	&skinex($::form{mypage}, &message($::resource{auth_writefobidden}), 0);
	&close_db;
	exit;
}

##
# ページ保存
sub do_write {
	my ($FrozenWrite, $viewpage) = @_;
	if (not &is_editable($::form{mypage})) {
		&skinex($::form{mypage}, &message($::resource{cantchange}), 0);
		return;
	}
	if ($FrozenWrite ne 'FrozenWrite') {
		return if (&frozen_reject());
	} else {
		# 凍結の属性を引き継ぐ
		$::form{myfrozen} = &get_info($::form{mypage}, $info_IsFrozen) ? 1 : 0;
	}
	return if (&conflict($::form{mypage}, $::form{mymsg}));

	# IPフィルタリング
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
	# 登録拒否文字列 ini ファイルに $disablewords で指定。区切りは改行
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

	# 差分作成
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
		&update_recent_changes if ($::form{mytouch});
		&skinex($::form{mypage}, &message($::resource{deleted}), 0);
	}
	return 0;
}

##
# エラー画面表示
sub print_error {
	my ($msg) = @_;
	&skinex($ErrorPage, qq(<p><strong class="error">$msg</strong></p>), 0);
	exit(0);
}

##
# 特殊文字を元に戻す。
sub unescape {
	my $s = shift;
	$s =~ s|\&amp;|\&|g;
	$s =~ s|\&lt;|\<|g;
	$s =~ s|\&gt;|\>|g;
	$s =~ s|\&quot;|\"|g;
	return $s;
}

##
# コンテンツ表示
sub print_content {
	my ($rawcontent) = @_;
	print &text_to_html($rawcontent);
}

##
# テキストHTML変換
sub text_to_html {
	my ($txt) = @_;
	my (@txt) = split(/\r?\n/, $txt);
	my $verbatim;
	my $tocnum = 0;
	my (@saved, @result);
	my $skip;
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

		$skip = 0;
		my $c = ord($_);	# 最初の文字のアスキー値
		if ($c == 42) {		# 数値による比較(文字列より早い) ord('*')
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
				my $delm = "\\$1";	# デリミタは | か ,
				my $tmp = ($1 eq ',') ? "$2$1" : "$2";
				# デリミタで分割して配列にセット
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
						if ($value[$i] eq '~') {		# 値が ~ だけなら下と連結
							$value[$i] = '';
						} elsif ($value[$i] =~ /^\~/) {	# 先頭が ~ なら th
							$value[$i] =~ s/^\~//g;
							$thflag = 'th';
						} elsif ($value[$i] eq '>') {	# 値が > だけなら右と連結
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
				# 中身は result にプッシュする。
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
		} elsif ($c == ord('#')) {
			if ($_ eq '#freeze') {	# スキップするプラグイン
				$skip = 1;
			}
		}
		push(@result, &inline($_)) if ($skip == 0);
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
# インライン展開
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
# 注釈表示
sub note {
	my ($msg) = @_;

	push(@::notes, $msg);
	return "<a id=\"notetext_" . @::notes . "\" "
		. "href=\"#notefoot_" . @::notes . "\" class=\"note_super\">*"
		. @::notes . "</a>";
}

##
# リンク作成
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
# 引数初期化。
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
# 最終更新日更新
sub update_recent_changes {
	my $update = time . "\t$::form{mypage}\n";
	my $recentchanges = $::cache_dir . '/recent.dat';

	open(fp, "<$recentchanges");
	my @oldupdates = <fp>;
	close(fp);

	my @updates;
	foreach (@oldupdates) {
		/(\d+)\t(\S+)/;	# date format.
		my $name = &unarmor_name($2);
		if (&is_exist_page($name) and ($name ne $::form{mypage})) {
			push(@updates, $_);
		}
	}
	unshift(@updates, $update) if (&is_exist_page($::form{mypage}));
	splice(@updates, $::maxrecent + 1);
	open(fp, ">$recentchanges");
	print(fp join('', @updates));
	close(fp);
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
# DBオープン ※モジュール化すると遅くなる。
sub open_db {
	if ($modifier_dbtype eq 'dbmopen') {
		dbmopen(%::database, $::data_dir, 0666);
	} else {
		tie(%::database, $modifier_dbtype, $::data_dir);
	}
}

##
# DBクローズ
sub close_db {
	if ($modifier_dbtype eq 'dbmopen') {
		dbmclose(%::database);
	} else {
		untie(%::database);
	}
}

sub open_diff {
	if ($modifier_dbtype eq 'dbmopen') {
		dbmopen(%::diffbase, $::diff_dir, 0666);
	} else {
		tie(%::diffbase, $modifier_dbtype, $::diff_dir);
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
# WikiName に ブランケット([[]])追加
sub armor_name {
	my ($name) = @_;
	return ($name =~ /^$wiki_name$/) ? $name : "[[$name]]";
}

##
# ブランケット([[]])削除。
sub unarmor_name {
	my ($name) = @_;
	return ($name =~ /^$bracket_name$/) ? $1 : $name;
}

##
# ブランケット付きか確認
sub is_bracket_name {
	my ($name) = @_;
	return ($name =~ /^$bracket_name$/) ? 1 : 0;
}

##
# ページ名をDBファイル名に変換
# @param $name ページ名
# @return DBファイル名
sub dbmname {
	my ($name) = @_;
	$name =~ s/(.)/uc unpack('H2', $1)/eg;
	return $name;
}

##
# リソースを読込む汎用ルーチン
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
# 衝突
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
# 現在時刻取得
# @return Y-m-d (D) H:i:s
sub get_now {
	return date("Y-m-d (D) H:i:s");
}

##
# InterWikiName 初期化
# YukiWiki形式 [[YukiWiki http://www.hyuki.com/yukiwiki/wiki.cgi?euc($1)]]
# PukiWiki形式 [http://www.hyuki.com/yukiwiki/wiki.cgi?$1 YukiWiki] euc
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
# 付加情報取得
# @param $page ページ
# @param $key キー
# @return 付加情報値
sub get_info {
	my ($page, $key) = @_;
	if ($key eq $info_IsFrozen) {
		return ($::database{$page} =~ /\n?#freeze\r?\n/) ? 1 : 0;
	}
	if (&is_exist_page($page)) {
		return &::date("Y-m-d H:i:s", (stat($::data_dir . "/" . &::dbmname($page) . ".txt"))[9]);
	}
	return '';

}

##
# 付加情報設定
# @param $page ページ
# @param $key キー
# @param $value 設定値
sub set_info {
	my ($page, $key, $value) = @_;
	if ($key eq $info_IsFrozen) {	# 凍結
		if ($::database{$page} =~ /\n?#freeze\r?\n/) {	# 凍結済み
			if ($value == 0) {	# 凍結解除
				$::database{$page} =~ s/\n?#freeze\r?\n//g;
			}
		} elsif ($value == 1) {	# 凍結
			$::database{$page} = "#freeze\n" . $::database{$page};
		}
	}
}

##
# 凍結チェック
# @return 1:凍結 / 0:未凍結
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
# パスワード確認
sub valid_password {
	my ($givenpassword) = @_;
	return (crypt($givenpassword, "AA") eq $::adminpass) ? 1 : 0;
}

##
# 凍結確認
# @return 1:凍結 / 0:未凍結
sub is_frozen {
	my ($page) = @_;
	return (&get_info($page, $info_IsFrozen)) ? 1 : 0;
}

##
# プラグイン展開
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
# インライン展開
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
# 文字コード変換
sub code_convert {
	my ($contentref, $kanjicode) = @_;
	if ($::lang eq 'ja') {
		&Jcode::convert($contentref, $kanjicode);	# for Jcode.pm
	}
	return $$contentref;
}

##
# ページ存在確認
sub is_exist_page {
	my ($name) = @_;
	return ($use_exists) ? exists($::database{$name}) : $::database{$name};
}


##############################
# 下位互換用

##
# 特殊文字を HTML エンティティに変換する。'&' → '&amp;' 等
sub escape {
	return &htmlspecialchars(shift);
}

##
# URLエンコードされた文字列をデコードする。foo%20bar%40baz → foo bar@baz
sub encode {
	return &rawurlencode(@_);
}

##
# Pluginに対応するJavaScript読込み文字列を作成する。
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
# PukiWiki風関数

##
# プラグインの存在確認
# @param プラグイン名
# @return 1:存在する。/ 0:存在しない。
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

			# セカンダリ設定
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
# プラグイン引数展開。必ず引数は shift とする。
sub func_get_args {
	my @args = split(/,/, shift);
	for (my $i = 0; $i < @args; $i++) {
		$args[$i] = trim($args[$i]);
	}
	return @args;
}

##############################
# PHP互換関数

##
# fopen hosts 対応用変数
my $hosts_exist = 0;
my %hosts;

##
# ファイルまたはURLをオープンする
sub fopen {
	my ($fname, $fmode) = @_;
	my $_fname;
	my $fp;

	# HTTP: だったら
	if (substr($fname, 0, 7) eq 'http://') {
		$fname =~ m!(http:)?(//)?([^:/]*)?(:([0-9]+)?)?(/.*)?!;
		my $host = ($3 ne "") ? $3 : "localhost";
		my $port = ($5 ne "") ? $5 : 80;
		my $path = ($6 ne "") ? $6 : "/";
		my $useproxy = 0;
		if ($::proxy_host) {
			$useproxy = 1;

			# 例外(プロキシを通さないアドレス)
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

		# hosts 機能(infoseek が DNS展開出来ないため hosts を利用する。)
		if ($hosts_exist == 0) {	# hosts を読んでいない。
			# hosts は リソースディレクトリの hosts.cgi 固定。
			my $hosts_path = $::res_dir . '/hosts.cgi';
			$hosts_exist = 2;	# ファイル・データが存在しなかった。
			if (-f $hosts_path) {
				if (open(FILE, $hosts_path)) {
					while (<FILE>) {
						next if /^#/; # 先頭 # ならコメント
						tr/\r\n//d;
						# IP URL alias は無視
						if (/(\d+\.\d+\.\d+\.\d+)\s+([^\s]+)/) {
							$hosts{$2} = $1;
							$hosts_exist = 1;	# データが存在した。
						}
					}
					close(FILE);
				}
			}
		}
		if (($hosts_exist == 1) && ($hosts{$host})) { # 該当があれば
			$host = $hosts{$host}; # hosts 優先で置き換え
		}

		if ($host =~ /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/) {
			$ip = pack('C4', split(/\./, $host));
		} else {
			#HOST名をIPに直す
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
# 文字列の先頭および末尾にあるホワイトスペースを取り除く。
# @param 変換前文字列
# @return 変換後の文字列
sub trim {
	my ($s) = @_;
	$s =~ s/^\s*(\S+)\s*$/$1/o; # trim
	return $s;
}

##
# 日付を Unix のタイムスタンプとして取得する
# @param 時
# @param 分
# @param 秒
# @param 月
# @param 日
# @param 年
# @return Unixタイム
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
# RFC1738に基づきURLエンコードを行う。foo bar@baz → foo%20bar%40baz
# @param 変換前文字列
# @return 変換後の文字列
sub rawurlencode {
	my ($encoded) = @_;
	$encoded =~ s/(\W)/'%' . unpack('H2', $1)/eg;
	return $encoded;
}

##
# URLエンコードされた文字列をデコードする。foo%20bar%40baz → foo bar@baz
# @param 変換前文字列
# @return 変換後の文字列
sub rawurldecode {
	my ($s) = @_;
	$s =~ tr/+/ /;
	$s =~ s/%([A-Fa-f0-9][A-Fa-f0-9])/pack("C", hex($1))/eg;
	return $s;
}

##
# 特殊文字を HTML エンティティに変換する。'&' → '&amp;' 等
# @param 変換前文字列
# @return 変換後の文字列
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
# ローカルの日付/時刻を書式化する
# @param $format 書式
# @param $tm Unixタイム
# @return 書式化した文字列
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
