##
# ページ一覧を表示。
# :書式|
#  ?cmd=list

# Copyright(c) 2004 Nekyo.
# for PyukiWiki(http://nekyo.hp.infoseek.co.jp)
# v0.2 non_list
# v0.1

sub plugin_list_action {
	my $navi = qq(<div id="body"><div id="top" style="text-align:center">);
	my $body = qq(</div>);
	my $prev = '';
	my $char = '';
	my $idx = 1;
	my $page_num = 0;

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
		$body .= qq(<li><a href="$::script?@{[&encode($page)]}">@{[&htmlspecialchars($page)]}</a>@{[&htmlspecialchars(&get_subjectline($page))]}</li>\n);
		$page_num++;
	}
	$body .= qq(</li></ul>Total:) . $page_num . qq( Pages);

	return ('msg' => $::IndexPage, 'body' => $navi . $body);
}
1;
