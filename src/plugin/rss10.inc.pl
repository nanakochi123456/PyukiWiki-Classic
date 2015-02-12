############################################################
# rss10 ƒvƒ‰ƒOƒCƒ“
# rss10.inc.pl
# Copyright(c) 2004 Nekyo.
# for PyukiWiki(http://nekyo.hp.infoseek.co.jp)
#
# 1TAB=4Spaces

sub plugin_rss10_action {
	my $rss = new Yuki::RSS(
		version => '1.0',
		encoding => $::charset,
	);
	$rss->channel(
		title => $::modifier_rss_title,
		link  => $::modifier_rss_link,
		description => $::modifier_rss_description,
	);
	my $recentchanges = $::database{$::RecentChanges};
	my $count = 0;
	foreach (split(/\n/, $recentchanges)) {
		last if ($count >= 15);
		/^\- \d\d\d\d\-\d\d\-\d\d \(...\) \d\d:\d\d:\d\d (\S+)/;    # date format.
		my $title = &unarmor_name($1);
		my $escaped_title = &escape($title);
		my $link = $modifier_rss_link . '?' . &encode($title);
		my $description = $escaped_title . &escape(&get_subjectline($title));
		$rss->add_item(
			title => $escaped_title,
			link  => $link,
			description => $description,
		);
		$count++;
	}
	# print RSS information (as XML).
	print <<"EOD";
Content-type: text/xml

@{[$rss->as_string]}
EOD
	&close_db;
	exit;
}
1;
