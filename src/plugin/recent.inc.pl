############################################################
# recent プラグイン
# recent.inc.pl
# Copyright(c) 2004 Nekyo.
# v 0.0.1 Action機能追加
# v 0.0.0
# for PyukiWiki(http://nekyo.hp.infoseek.co.jp)
#

sub dbmname {
	my ($name) = @_;
	$name =~ s/(.)/uc unpack('H2', $1)/eg;
	return $name;
}

sub get_date {
	my ($time) = @_;

	my (@week) = qw(Sun Mon Tue Wed Thu Fri Sat);
	my ($sec, $min, $hour, $day, $mon, $year, $weekday) = localtime($time);
	$year += 1900;
	$mon++;
	$mon = "0$mon" if $mon < 10;
	$day = "0$day" if $day < 10;
	$hour = "0$hour" if $hour < 10;
	$min = "0$min" if $min < 10;
	$sec = "0$sec" if $sec < 10;
	$weekday = $week[$weekday];
	return "$year-$mon-$day ($weekday) $hour:$min:$sec";
}

sub plugin_recent_action {
	my $update;
	my %rclist;
	my $atime;
	foreach my $page (sort keys %::database) {
		$atime = (stat($::dataname . "/" . &dbmname($page) . ".txt"))[9];	# statでファイル更新日時取得
		$update = "- @{[&get_date($atime)]} @{[&armor_name($page)]} @{[&get_subjectline($page)]}";
		$rclist{$atime} = $update;
	}
	my @updates;
	foreach my $time (sort { $b <=> $a } keys %rclist) {
		push(@updates, $rclist{$time});
	}
	splice(@updates, $::maxrecent + 1);
	$::database{$::RecentChanges} = join("\n", @updates);
	if ($file_touch) {
		open(FILE, "> $file_touch");
		print FILE localtime() . "\n";
		close(FILE);
	}
	return;
}

sub plugin_recent_convert {
	my $limit = shift;
	if ($limit eq '') { $limit = 10; }
	my $recentchanges = $::database{$::RecentChanges};
	my $count = 0;
	my $date = "";
	my $out = "";
	foreach (split(/\n/, $recentchanges)) {
		last if ($count >= $limit);
		/^\- (\d\d\d\d\-\d\d\-\d\d) \(...\) \d\d:\d\d:\d\d (\S+)/;	# date format.
		if ($2) {
			if ($date ne $1) {
				if ($date ne '') { $out .= "</ul>\n"; }
				$date = $1;
				$out .= "<strong>$date</strong><ul class=\"recent_list\">\n";
			}
			$out .= "<li>" . &make_link($2) . "</li>\n";
		}
		$count++;
	}
	if ($date ne '') { $out .= "</ul>\n"; }
	return $out;
}
1;
