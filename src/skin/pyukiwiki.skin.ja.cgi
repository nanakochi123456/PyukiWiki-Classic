# skin

sub skin {
	my ($page, $body, $is_page) = @_;

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
  <link rel="stylesheet" href="$::skin_dir/default.$::lang.css" type="text/css" media="screen" charset="Shift_JIS" />
  <link rel="stylesheet" href="$::skin_dir/blosxom.css" type="text/css" media="screen" charset="Shift_JIS" />
  <link rel="stylesheet" href="$::skin_dir/print.$::lang.css" type="text/css" media="print" charset="Shift_JIS" />
EOD
	if ($::extend_edit) {
		print '<script type="text/javascript" src="' . $::skin_dir . '/instag.js"></script>' . "\n";
	}
	print <<"EOD";
</head>
<body class="$bodyclass">
<div id="header">
 <a href="$::modifierlink"><img id="logo" src="$::image_dir/pyukiwiki.png" width="80" height="80" alt="[PyukiWiki]" title="[PyukiWiki]" /></a>
<h1 class="title"><a
    title="$::resource{searchthispage}"
    href="$::script?cmd=search&amp;mymsg=$cookedpage">@{[&htmlspecialchars($page)]}</a></h1>
<a href="$::script?$cookedpage">$::script?$cookedpage</a>
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
 @{[ (-f "$::plugin_dir/attach.inc.pl")
   ? qq( | <a href="$::script?cmd=attach&amp;mypage=$cookedpage">$::resource{attachbutton}</a>)
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

	if ($is_page) {
		if (&is_exist_page($::Header)) {
			print "<div id=\"pageheader\">";
			&print_content($::database{$::Header});
			print "</div>";
		}

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
      <div id="body">$body</div>
    </td>
  </tr>
</table>
EOD
		if (&is_exist_page($::Footer)) {
			print "<div id=\"pagefooter\">";
			&print_content($::database{$::Footer});
			print "</div>";
		}
	} else {
		print <<"EOD";
<div id="body">$body</div>
EOD
	}

	if (@::notes) {
		print << "EOD";
<div id="note">
<hr class="note_hr" />
EOD
		my $cnt = 1;
		foreach my $note (@::notes) {
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
<div id="toolbar"><a href="$::script?cmd=rss10"><img src="$::image_dir/rss.png" border="0" /></a></div>
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
EOD
	if ($::enable_convtime != 0) {
		printf('<br />HTML convert time to %.3f sec.<br />', (times)[0] - $_conv_start);
	}
	print <<"EOD";
</div>
</body>
</html>
EOD
}

1;
