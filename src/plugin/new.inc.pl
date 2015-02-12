##
# ��������������հ���ξ���New��ɽ�����롣
# :��|
#  &new(����);
# 5������ξ��� New��1������ξ��� New! ��ɽ�����롣
# @author Nekyo. for PyukiWiki(http://nekyo.hp.infoseek.co.jp)

sub plugin_new_inline {
	my $date = shift;
	return '' if ($date eq '');

	my $retval = $date;
	my ($mday, $mon, $year) = (localtime())[3..5];

	my $now = &mktime(0, 0, 0, $mon + 1, $mday, $year + 1900);
	$date =~ /(\d+)-(\d+)-(\d+)/;
	my $past = &mktime(0, 0, 0, $2, $3, $1);

	if (($now - $past) <= 1*60*60*24) {
		$retval .= ' <span class="new1">New!</span>';
	} elsif (($now - $past) <= 5*60*60*24) {
		$retval .= ' <span class="new5">New</span>';
	}
	return '<span class="comment_date">' . $retval . '</span>';
}
1;
