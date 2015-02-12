##
# 文字の大きさを指定する。
# :書式|
#  &size(ピクセル数値){文字列}
# ピクセル数値は文字の大きさを指定。
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
