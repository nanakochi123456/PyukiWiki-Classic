# 本体
my $main_body = '';
if ($skin::is_page) {
	$main_body .=<<"EOD";
$skin::header
$::prove_scr
<table border="0" style="width:100%">
  <tr>
    <td class="menubar">
    <div id="menubar">
EOD

	$::pushedpage = $::form{mypage};	# push;
	$::form{mypage} = $skin::default_menu;
	$main_body .= &::text_to_html($::database{$::form{mypage}});
	$::form{mypage} = $::pushedpage;	# pop

	$main_body .=<<"EOD";
    </div>
    </td>
    <td valign=top>
      <div id="body">$skin::body</div>
    </td>
  </tr>
</table>
$skin::footer
EOD

} else {
	$main_body .= qq(<div id="body">$skin::body</div>);
}

print <<"EOD";
<!DOCTYPE html
    PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
    "http://www.w3.org/TR/html4/loose.dtd">
<html lang="$::lang">
<head>
  <meta http-equiv="Content-Language" content="$::lang">
  <meta http-equiv="Content-Type" content="text/html; charset=$::charset">
  <title>$skin::escapedpage @{[&::htmlspecialchars(&::get_subjectline($page))]}</title>
  $skin::basehref<link rel="index" href="$::script?cmd=list">
  <link rev="made" href="mailto:$::modifier_mail">
  <link rel="stylesheet" href="$skin::default_css" type="text/css" media="screen" charset="Shift_JIS" />
  <link rel="alternate" type="application/rss+xml" title="RSS" href="$skin::rssurl" />
  @{[&::jscss_include]}
</head>
<body class="$skin::bodyclass"$::bodyattr>
<div id="header">
 <a href="$::modifierlink"><img id="logo" src="$skin::default_icon" width="80" height="80" alt="[PyukiWiki]" title="[PyukiWiki]" /></a>
<h1 class="title"><a
    title="$::resource{searchthispage}"
    href="$::script?cmd=search&amp;mymsg=$skin::cookedpage">@{[&::htmlspecialchars($skin::page)]}</a></h1>
<a href="$::script?$cookedpage">$::script?$skin::cookedpage</a>
</div>
<div id="navigator">
[ <a href="$::script?$::FrontPage">$::resource{top}</a> ] &nbsp;
[ $skin::navi <a href="$::script?$skin::cookedpage">$::resource{reload}</a> ] &nbsp;
[ <a href="$::script?cmd=newpage">$::resource{createbutton}</a> |
  <a href="$::script?cmd=list">$::resource{indexbutton}</a> | 
  <a href="$::script?cmd=search">$::resource{searchpage}</a> |
  <a href="$::script?$::RecentChanges">$::resource{recentchangesbutton}</a> |
  <a href="$::script?$::HelpPage">$::resource{help}</a> ]
</div>
<hr class="full_hr" />
$skin::lastmod1
$main_body
$skin::notes
<hr class="full_hr" />
<div id="toolbar"><a href="$skin::rssurl"><img src="$::image_dir/feed-icon16x16.png" border="0" /></a></div>
$skin::lastmod2
<div id="footer">
Modified by <a href="$::modifierlink">$::modifier</a><br /><br />
<b>PyukiWiki Classic $::version</b>
Copyright&copy; since 2004 by <a href="http://nekyo.hp.infoseek.co.jp/">Nekyo</a>,
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
