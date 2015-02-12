##
# �����ǻ��ꤷ������饤�����ǤΡ�ʸ�������طʿ�����ꤹ�롣
# :��|
#  &color([ʸ����][,�طʿ�]){ʸ��};

# @author nekyo.
# @version 1.00
use strict;
package color;

sub plugin_inline {
	my @args = split(/,/, shift);
	my $bgcolor = '';
	my ($color, $bgcolor, $body);

	if (@args == 3) {
		$color = $args[0];
		$bgcolor = $args[1];
		$body = $args[2];
		if ($body eq '') {
			$body = $bgcolor;
			$bgcolor = '';
		}
	} elsif (@args == 2) {
		$color = $args[0];
		$body = $args[1];
	} else {
		return '';
	}
	if ($color eq '' or $body eq '') {
		return '';
	}
	if ($bgcolor ne '') {
		$color .= ';background-color:'.$bgcolor;
	}
	return "<span style=\"color:$color\">$body</span>";
}
1;
