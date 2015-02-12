######################################################################
# calendar2.inc.pl - This is PyukiWiki, yet another Wiki clone.
# $Id: calendar2.inc.pl,v 1.45 2006/05/20 02:04:33 papu Exp $
#
# 使用方法
# #calendar2([{[ページ名|*], [yyyymm], [off]}])
# 概要
#   指定した位置にカレンダーを設置します。
#   表示月のとなりに表示されたリンク(<< および >>)を選択することで先月／次月分のカレンダーを表示できます。
#   カレンダー上でyyyy/mm/ddという日付を選択すると、ページ名/yyyy-mm-ddというページを表示できます。
#   当日分のページが作成されていた場合、カレンダーの右隣に当日分のページ内容を表示します。
######################################################################
use strict;

######################################################################
#
sub plugin_calendar2_convert {
	my ($page, $dt, $flg) = split(/,/, shift);
	my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst);
	my ($disp_wday,$today,$start,$end,$i,$label,$cookedpage,$d);
	my ($prefix,$splitter);
	my $date_format;
	my $empty = '';
	my $calendar = "";
	my ($_year, $_mon);
	($sec, $min, $hour, $mday, $mon, $year) = localtime();	# 現在日時の取得

	if ($dt eq '') {
		$_year = &date("Y");
		$_mon  = &date("m");
	} else {
		$_year = substr($dt, 0, 4);
		$_mon  = substr($dt, 4, 2);
	}
	$date_format = ($::date_format eq '') ? 'Y-m-d' : $::date_format;

	if ($page eq '') {
		$prefix = $::form{mypage};
		$splitter = '/';
	} elsif ($page eq '*') {
		$prefix = '';
		$splitter = '';
	} else {
		$prefix = $page;
		$splitter = '/';
	}
	$page = &htmlspecialchars($prefix);

	my $prev_year = $_mon eq  1 ? $_year - 1 : $_year;
	my $prev_mon  = $_mon eq  1 ? 12 : $_mon - 1;
	my $next_year = $_mon eq 12 ? $_year + 1 : $_year;
	my $next_mon  = $_mon eq 12 ?  1 : $_mon + 1;
	my $cookedpage = &encode($page eq '' ? $::FrontPage : $page);

	my $query;
	$query="cmd=calendar2&amp;mymsg=$cookedpage&amp;format=@{[&encode($date_format)]}";
	$calendar =<<"END";
<table class="style_calendar" summary="calendar body">
  <tr>
    <td class="style_td_caltop" colspan="7">
      <a href="$::script?$query&amp;date=@{[sprintf("%04d%02d", $prev_year, $prev_mon)]}">&lt;&lt;</a>
      <strong>$_year.$_mon</strong>
      <a href="$::script?$query&amp;date=@{[sprintf("%04d%02d", $next_year, $next_mon)]}">&gt;&gt;</a><br />
      [<a href="$::script?$page">$page</a>]
    </td>
  </tr>
  <tr>
    <td class="style_td_week">S</td>
    <td class="style_td_week">M</td>
    <td class="style_td_week">T</td>
    <td class="style_td_week">W</td>
    <td class="style_td_week">T</td>
    <td class="style_td_week">F</td>
    <td class="style_td_week">S</td>
  </tr>
  <tr>
END
	my $tm = &mktime(0, 0, 0, $_mon, 1, $_year);
	my $j  = &date("w", $tm);

	# 月初 先月分セル描画
	for ($i = 0; $i < $j; $i++) {
		$calendar .= "    <td class=\"style_td_blank\">&nbsp;</td>\n";
	}

	my $lm  = &mktime(0, 0, 0, $_mon + 1, 0, $_year);
	# 月末取得
	my $ld = &date("d", $lm);

	for ($j = 1; $j <= $ld; $j++) {
		$i++;
		$calendar .= qq(<tr>) if ($i % 7 == 1); # 日曜日
		if ($i % 7 == 1) {
			$calendar .= qq(<td class="style_td_sun">);
		} elsif ($i % 7 == 0) {
			$calendar .= qq(<td class="style_td_sat">);
		} else {
			$calendar .= qq(<td class="style_td_day">);
		}
		$calendar .= qq($j</td>);
		$calendar .= qq(</tr>) if ($i % 7 == 0); # 土曜日
	}
	if ($i % 7 != 0) { #月末がぴったりじゃなかｔった。
		for ($j = $i % 7; $j < 7; $j++) {
			$calendar .= "<td class=\"style_td_blank\">&nbsp;</td>";
		}
		$calendar.="</tr>";
	}
	$calendar .= "</table>\n";

	return $calendar;
}

sub plugin_calendar2_action {
	my $page = &htmlspecialchars($::form{mymsg});
	my $date = &htmlspecialchars($::form{date});
	my $format=&htmlspecialchars($::form{format});
	my $body = &plugin_calendar2_convert(qq($page,$date,$format));

	my $yy = sprintf("%04d.%02d",substr($date,0,4),substr($date,4,2));
	my $s_page = &htmlspecialchars($page);
	return ('msg'=>qq(calendar $s_page/$yy), 'body'=>$body);
}
1;
__END__

