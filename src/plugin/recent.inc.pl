############################################################
# �Ƕṹ�����줿�ڡ���������ɽ������ά�������10�
# :��|
#  #recent([���])

# @author Copyright(c) 2004 Nekyo.
# v 0.0.3 : + �ڡ���̾�ϰ�����ɽ�����ʤ���
# v 0.0.2 �����ʥߥå��������� RecentChanges �����������
# v 0.0.1 Action�ˤ������ʥߥå�������ǽ�ɲ�
# v 0.0.0
# for PyukiWiki(http://nekyo.hp.infoseek.co.jp)

##
# ���֤��֤�
# @param unix time
# @return yyyy-mm-dd ����
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
# �ǽ������ΰ�����ɽ��
# @return �ǽ������ΰ���
sub plugin_recent_action {
	my $update;
	my %rclist;
	my $atime;
	foreach my $page (sort keys %::database) {
		$atime = (stat($::data_dir . "/" . &::dbmname($page) . ".txt"))[9];	# stat�Ǻǽ��������դ����
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
# �ǽ������ΰ�����ɽ��
# @param ɽ����(��ά��:10)
# @return �ǽ������ΰ���
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
		next if ($2 =~ /\[*:/); # ��Ƭ�� : �ξ���ɽ�����ʤ���

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
