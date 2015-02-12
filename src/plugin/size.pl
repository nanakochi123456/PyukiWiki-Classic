###############################################
# size plugin for YukiWiki & PyukiWiki
# size.pl
# Copyright(c) 2004 Nekyo.
# 1TAB=4Spaces
###############################################
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
