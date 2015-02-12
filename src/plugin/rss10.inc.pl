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
	my $recentchanges = $::database{$::RecentChanges};
	my $count = 0;

	print <<"EOD";
Content-type: text/xml

<?xml version="1.0" encoding="$::charset"?>
  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns="http://purl.org/rss/1.0/" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <channel rdf:about="$::modifier_rss_link">
  <title>$::modifier_rss_title</title> 
  <link>$::modifier_rss_link</link> 
  <discription>$::modifier_rss_description</discription>
  <items>
  <rdf:Seq>
EOD

	my $items;

	foreach (split(/\n/, $recentchanges)) {
		last if ($count >= 15);
		/^\- (\d\d\d\d\-\d\d\-\d\d) \(...\) (\d\d:\d\d:\d\d) (\S+)/;    # data format.
		my $title = &unarmor_name($3);
		my $escaped_title = &htmlspecialchars($title);
		my $link = $modifier_rss_link . '?' . &rawurlencode($title);
		my $description = $escaped_title . &htmlspecialchars(&get_subjectline($title));

		print <<"EOD";
  <rdf:li rdf:resource="$link" />
EOD

		$gmt = ((localtime(time))[2] + (localtime(time))[3] * 24)
			- ((gmtime(time))[2] + (gmtime(time))[3] * 24);
		my $date = $1 . "T" . $2 . sprintf("%+02d:00", $gmt);

		$items .=<<"EOD";
  <item rdf:about="$link">
  <title>$escaped_title</title> 
  <link>$link</link> 
  <discription>$description</discription> 
  <dc:date>$date</dc:date> 
  </item>
EOD
		$count++;
	}
	print <<"EOD";
  </rdf:Seq>
  </items>
  </channel>
  $items
</rdf:RDF>
EOD
	&close_db;
	exit;
}
1;
