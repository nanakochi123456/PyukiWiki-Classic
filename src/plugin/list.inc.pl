############################################################
# list プラグイン
# list.inc.pl
# Copyright(c) 2004 Nekyo.
# for PyukiWiki(http://nekyo.hp.infoseek.co.jp)
# v0.2 non_list
# v0.1
# 1TAB=4Spaces

#<div id="body"><div id="top" style="text-align:center">
#<a id="top_1" href="#head_1"><strong>B</strong></a> | 
#<a id="top_2" href="#head_2"><strong>F</strong></a> | 
#</div>
#<ul>
# <li><a id="head_1" href="#top_1"><strong>B</strong></a>
#  <ul>
#   <li><a href="http://nekyo.mydns.jp/index.php?cmd=read&amp;page=BracketName">BracketName</a><small>(114d)</small></li>
#  </ul>
# </li>
#</ul>

sub plugin_list_action {
	my $navi = qq(<div id="body"><div id="top" style="text-align:center">);
	my $body = qq(</div>);
	my $prev = '';
	my $char = '';
	my $idx = 1;

	foreach my $page (sort keys %::database) {
		next if ($page =~ $::non_list);
		$char = substr($page, 0, 1);
		if (!($char =~ /[a-zA-Z0-9]/)) {
			$char = "日本語";
		}
		if ($prev ne $char) {
			if ($prev ne '') {
				$navi .= " |\n";
				$body .= "  </ul>\n </li>\n</ul>\n";
			}
			$prev = $char;
			$navi .= qq(<a id="top_$idx" href="#head_$idx"><strong>$prev</strong></a>);
			$body .= <<"EOD";
<ul>
 <li><a id="head_$idx" href="#top_$idx"><strong>$prev</strong></a>
  <ul>
EOD
			$idx++;
		}
		$body .= qq(<li><a href="$::script?@{[&encode($page)]}">@{[&escape($page)]}</a>@{[&escape(&get_subjectline($page))]}</li>\n);
	}
	$body .= qq(</li></ul>);

	return ('msg' => $::IndexPage, 'body' => $navi . $body);
}
1;
