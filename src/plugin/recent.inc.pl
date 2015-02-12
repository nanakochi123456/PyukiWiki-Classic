############################################################
# recent プラグイン
# recent.inc.pl
# Copyright(c) 2004 Nekyo.
# v 0.0.2 ダイナミック生成から RecentChanges を除外した。
# v 0.0.1 Actionによりダイナミック生成機能追加
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
		next if ($page eq $::RecentChanges);	# RecentChanges を除外
		$atime = (stat($::data_dir . "/" . &dbmname($page) . ".txt"))[9];	# statで最終更新日付を取得
		$rclist{$page} = $atime;
	}
	my @updates;
	foreach my $page (sort { $rclist{$b} <=> $rclist{$a} } keys %rclist) {
		$atime = $rclist{$page};
		$update = "- @{[&get_date($atime)]} @{[&armor_name($page)]} @{[&get_subjectline($page)]}";
		push(@updates, $update);
	}
	splice(@updates, $::maxrecent + 1);
	$::database{$::RecentChanges} = join("\n", @updates);
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
