##
# ʸ�����礭������ꤹ�롣
# :��|
#  &size(�ԥ��������){ʸ����}
# �ԥ�������ͤ�ʸ�����礭������ꡣ
# @author Nekyo.
use strict;
package size;

sub plugin_inline {
	my ($size, $body) = split(/,/, shift);
	if ($size eq '' or $body eq '') {
		return "";
	}
	return "<span style=\"font-size:" . $size . "px;display:inline-block;line-height:130%;text-indent:0px\">$body</span>";
}
1;
