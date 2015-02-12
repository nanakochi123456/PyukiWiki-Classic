#################################
# Default skin for Classic v0.1.7
# Copyright(c) Nekyo
use strict;

##
# @param $page ページ名
# @param $is_page ページか？
sub skin {
	my ($page, $body, $is_page, $bodyclass, $editable, $admineditable, $basehref) = @_;

	my $cookedpage  = &encode($page);
	my $escapedpage = &htmlspecialchars($page);
	my $HelpPage    = &encode($::resource{help});

	# 更新日付
	my $lastmod1 = '';	# 前表示
	my $lastmod2 = '';	# 後表示
	if ($::last_modified != 0) {	# v0.0.9
		$lastmod1 = "<div id=\"lastmodified\">$::lastmod_prompt "
			. &date("Y-m-d H:i:s", (stat($::data_dir . "/" . &dbmname($page) . ".txt"))[9]) . "</div>";
		if ($::last_modified == 2) {
			$lastmod2 = $lastmod1;
			$lastmod1 = '';
		}
	}

	# ヘッダー、フッター
	my $header = (&is_exist_page($::Header))
		? '<div id="pageheader">' . &text_to_html($::database{$::Header}) . '</div>' : '';
	my $footer = (&is_exist_page($::Footer))
		? '<div id="pagefooter">' . &text_to_html($::database{$::Footer}) . '</div>' : '';

	# skinチェンジャー
	my $default_css  = "$::skin_dir/default.css";
	my $default_icon = "$::image_dir/pyukiwiki.png";
	my $default_menu = $::MenuBar;
	foreach my $key (keys %::skin_chg) {
		if ($page =~ /$key/i) {
			$default_css  = "$::skin_dir/"  . $::skin_chg{$key}{'css'};
			$default_icon = "$::image_dir/" . $::skin_chg{$key}{'icon'};
			$default_menu = $::skin_chg{$key}{'menu'};
			last;
		}
	}

	# 本体
	my $main_body = '';
	if ($is_page) {
		$main_body .=<<"EOD";
$header
$::prove_scr
<table border="0" style="width:100%">
  <tr>
    <td class="menubar">
    <div id="menubar">
EOD
		$::pushedpage = $::form{mypage};	# push;
		$::form{mypage} = $default_menu;
		$main_body .= &text_to_html($::database{$::form{mypage}});
		$::form{mypage} = $::pushedpage;	# pop
		$main_body .=<<"EOD";
    </div>
    </td>
    <td valign=top>
      <div id="body">$body</div>
    </td>
  </tr>
</table>
$footer
EOD
	} else {
		$main_body .= qq(<div id="body">$body</div>);
	}

	# ノート
	my $notes = '';
	if (@::notes) {
		$notes .=<< "EOD";
<div id="note">
<hr class="note_hr" />
EOD
		my $cnt = 1;
		foreach my $note (@::notes) {
			$notes .=<< "EOD";
<a id="notefoot_$cnt" href="#notetext_$cnt" class="note_super">*$cnt</a>
<span class="small">@{[&inline($note)]}</span>
<br />
EOD
			$cnt++;
		}
		$notes .= "</div>";
	}

	# RSS URL
	my $rssurl = $::rssurl ? $::rssurl : "$::script?cmd=rss10";

	# ナビゲーション作成
	my $navi = '';
	if ($editable) {
		$navi .= qq(<a title="$::resource{editthispage}" href="$::script?cmd=edit&amp;mypage=$cookedpage">$::resource{editbutton}</a> | );
	}
	if ($admineditable) {
		$navi .= qq(<a title="$::resource{admineditthispage}" href="$::script?cmd=adminedit&amp;mypage=$cookedpage">$::resource{admineditbutton}</a> | )
			. qq(<a href="$::script?cmd=diff&amp;mypage=$cookedpage">$::resource{diffbutton}</a> | );
	}
	if (-f "$::plugin_dir/attach.inc.pl") {
		$navi .= qq(<a href="$::script?cmd=attach&amp;mypage=$cookedpage">$::resource{attachbutton}</a> | );
	}

	print <<"EOD";
Content-type: text/html; charset=$::charset
$::gzip_header
EOD
	if ($::gzip_header ne '') {
		open(STDOUT,"| $::gzip_path");
	}
	print <<"EOD";
<!DOCTYPE html
    PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
    "http://www.w3.org/TR/html4/loose.dtd">
<html lang="$::lang">
<head>
  <meta http-equiv="Content-Language" content="$::lang">
  <meta http-equiv="Content-Type" content="text/html; charset=$::charset">
  <title>$escapedpage @{[&htmlspecialchars(&get_subjectline($page))]}</title>
  $basehref<link rel="index" href="$::script?cmd=list">
  <link rev="made" href="mailto:$::modifier_mail">
  <link rel="stylesheet" href="$default_css" type="text/css" media="screen" charset="Shift_JIS" />
  <link rel="alternate" type="application/rss+xml" title="RSS" href="$rssurl" />
EOD
	print &jscss_include();
	print <<"EOD";
</head>
<body class="$bodyclass"$::bodyattr>
<div id="header">
 <a href="$::modifierlink"><img id="logo" src="$default_icon" width="80" height="80" alt="[PyukiWiki]" title="[PyukiWiki]" /></a>
<h1 class="title"><a
    title="$::resource{searchthispage}"
    href="$::script?cmd=search&amp;mymsg=$cookedpage">@{[&htmlspecialchars($page)]}</a></h1>
<a href="$::script?$cookedpage">$::script?$cookedpage</a>
</div>
<div id="navigator">
[ <a href="$::script?$::FrontPage">$::resource{top}</a> ] &nbsp;
[ $navi <a href="$::script?$cookedpage">$::resource{reload}</a> ] &nbsp;
[ <a href="$::script?cmd=newpage">$::resource{createbutton}</a> |
  <a href="$::script?cmd=list">$::resource{indexbutton}</a> | 
  <a href="$::script?cmd=search">$::resource{searchpage}</a> |
  <a href="$::script?$::RecentChanges">$::resource{recentchangesbutton}</a> |
  <a href="$::script?$HelpPage">$::resource{help}</a> ]
</div>
<hr class="full_hr" />
$lastmod1
$main_body
$notes
<hr class="full_hr" />
<div id="toolbar"><a href="$rssurl"><img src="$::image_dir/feed-icon16x16.png" border="0" /></a></div>
$lastmod2
<div id="footer">
Modified by <a href="$::modifierlink">$::modifier</a><br /><br />
<b>PyukiWiki Classic $::version</b>
Copyright&copy; 2004-2006 by <a href="http://nekyo.hp.infoseek.co.jp/">Nekyo</a>,
<a href="http://pyukiwiki.sourceforge.jp/">PyukiWiki Developers Team</a>.
License is <a href="http://www.gnu.org/licenses/gpl.html">GPL</a><br />
Based on "YukiWiki" 2.1.0 by <a href="http://www.hyuki.com/yukiwiki/">yuki</a>
and <a href="http://pukiwiki.sourceforge.jp">"PukiWiki"</a>
EOD
	# 変換時間はなるべく最後に計算
	if ($::enable_convtime != 0) {
		printf('HTML convert time: %.3f', ((times)[0] - $::conv_start));
		print ' Compressed' if ($::gzip_header ne '');
		print "<br />\n";
	}
	print <<"EOD";
</div>
</body>
</html>
EOD
}

1;
