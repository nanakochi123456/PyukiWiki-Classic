# br plugin for YukiWiki & PyukiWiki
# Author Nekyo.(http://nekyo.hp.infoseek.co.jp/)
# v1.0 2004/05/26
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
		version => '1.0',
		author => 'Nekyo',
		syntax => '&br',
		description => 'line break.',
		example => '&br',
	};
}

1;
