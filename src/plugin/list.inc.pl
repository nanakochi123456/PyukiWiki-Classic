############################################################
# list ƒvƒ‰ƒOƒCƒ“
# list.inc.pl
# Copyright(c) 2004 Nekyo.
# for PyukiWiki(http://nekyo.hp.infoseek.co.jp)
#
# 1TAB=4Spaces

sub plugin_list_action {
	my $body = qq(<ul>);
	foreach my $page (sort keys %::database) {
		$body .= qq(<li><a href="$::script?@{[&encode($page)]}">@{[&escape($page)]}</a>@{[&escape(&get_subjectline($page))]}</li>);
		# print qq(<li>@{[&get_info($page, $info_IsFrozen)]}</li>);
		# print qq(<li>@{[0 + &is_frozen($page)]}</li>);
	}
	$body .= qq(</ul>);
	return ('msg' => $::IndexPage, 'body' => $body);
}
1;
