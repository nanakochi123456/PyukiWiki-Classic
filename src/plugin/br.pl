##
# 文章中で改行を行う。
# :書式|
#  #br
#  &br;
# @author Nekyo.(http://nekyo.hp.infoseek.co.jp/)
# @version 1.00

use strict;
package br;

sub plugin_block {
	return &plugin_inline;
}

sub plugin_inline {
	return qq(<br />);
}

sub plugin_usage {
	return {
		name => 'br',
		version => '1.00',
		author => 'Nekyo',
		syntax => '&br',
		description => 'line break.',
		example => '&br',
	};
}
1;
