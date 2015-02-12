############################################################
# rss10 plugin
# rss10.inc.pl
# Copyright(c) 2004 Nekyo.
# for PyukiWiki(http://nekyo.hp.infoseek.co.jp)
#
# v0.0.2 2005/03/11 Add dc:date
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
		/^\- (\d\d\d\d\-\d\d\-\d\d) \(...\) (\d\d:\d\d:\d\d) (\S+)/;    # data format.
		my $title = &unarmor_name($3);
		my $escaped_title = &escape($title);
		my $link = $modifier_rss_link . '?' . &encode($title);
		my $description = $escaped_title . &escape(&get_subjectline($title));

		$gmt = ((localtime(time))[2] + (localtime(time))[3] * 24)
			- ((gmtime(time))[2] + (gmtime(time))[3] * 24);
		my $date = $1 . "T" . $2 . sprintf("%+02d:00", $gmt);

		$rss->add_item(
			title => $escaped_title,
			link  => $link,
			description => $description,
			dc_date => $date
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
