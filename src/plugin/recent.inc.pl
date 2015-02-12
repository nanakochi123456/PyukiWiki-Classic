############################################################
# 最近更新されたページ一覧を表示。省略時件数は10件。
# :書式|
#  #recent([件数])

# @author Copyright(c) 2004 Nekyo.
# v 0.0.3 : + ページ名は一覧に表示しない。
# v 0.0.2 ダイナミック生成から RecentChanges を除外した。
# v 0.0.1 Actionによりダイナミック生成機能追加
# v 0.0.0
# for PyukiWiki(http://nekyo.hp.infoseek.co.jp)

##
# 時間を返す
# @param unix time
# @return yyyy-mm-dd 形式
sub get_date {
	my ($time) = @_;
	my ($sec, $min, $hour, $day, $mon, $year, $weekday) = localtime($time);
	$year += 1900;
	$mon++;
	$mon = "0$mon" if $mon < 10;
	$day = "0$day" if $day < 10;
	return "$year-$mon-$day";
}

##
# 最終更新の一覧を表示
# @return 最終更新の一覧
sub plugin_recent_action {
	my $update;
	my %rclist;
	my $atime;
	foreach my $page (sort keys %::database) {
		$atime = (stat($::data_dir . "/" . &::dbmname($page) . ".txt"))[9];	# statで最終更新日付を取得
		$rclist{$page} = $atime;
	}
	my @updates;
	foreach my $page (sort { $rclist{$b} <=> $rclist{$a} } keys %rclist) {
		next if ($page eq '');
		$atime = $rclist{$page};
		$update = "- @{[&get_date($atime)]} @{[&armor_name($page)]}";
		push(@updates, $update);
	}
	splice(@updates, $::maxrecent + 1);
	return ('msg' => $::resource{recentchangesbutton}, 'body' => &::text_to_html(join("\n", @updates)));
}

##
# 最終更新の一覧を表示
# @param 表示数(省略時:10)
# @return 最終更新の一覧
sub plugin_recent_convert {
	my $limit = shift;
	$limit = 10 if ($limit eq '');
	my $recentchanges = $::cache_dir . '/recent.dat';

	open(fp, "<$recentchanges");
	@lines = <fp>;
	close(fp);

	my $count = 0;
	my $date = "";
	my $_date;
	my $out = "";
	foreach (@lines) {
		last if ($count >= $limit);
		/(\d+)\t(\S+)/;	# date format.
		next if ($2 =~ /\[*:/); # 先頭が : の場合は表示しない。

		$_date = get_date($1);
		if ($2) {
			if ($date ne $_date) {
				$out .= "</ul>\n" if ($date ne '');
				$date = $_date;
				$out .= "<strong>$date</strong><ul class=\"recent_list\">\n";
			}
			$out .= "<li>" . &make_link($2) . "</li>\n";
			$count++;
		}
	}
	$out .= "</ul>\n" if ($date ne '');
	return $out;
}
1;
