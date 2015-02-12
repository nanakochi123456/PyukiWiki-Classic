##
# 他のプラグインで有効になったテキスト回り込み指定を解除する。
# :書式|
#  #clear
# @author: Nanami <nanami@daiba.cx>

use strict;
package clear;

sub plugin_inline {
	return '<div class="clear"></div>';
}
1;
