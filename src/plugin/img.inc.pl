############################################################
# img Plugin
# img.inc.pl
# Copyright(c) 2004 Nekyo.
# for PyukiWiki(http://nekyo.hp.infoseek.co.jp)
# v0.0.1 2004/04/23 Add Alt Option.
# v0.0.0 xxxx/xx/xx ProtType
# 1TAB=4Spaces

sub plugin_img_convert {
	my $argv = shift;
	my ($uri, $align, $alt) = split(/,/, $argv);
	$uri   = trim($uri);
	$align = trim($align);
	$alt   = trim($alt);

	if ($align =~ /^(r|right)/i) {
		$align = 'right';
	} elsif ($align =~ /^(l|left)/i) {
		$align = 'left';
	} else {
		return '<div style="clear:both"></div>';
	}
	if ($uri =~ /^(http|https|ftp):/) {
		if ($uri =~ /\.(gif|png|jpeg|jpg)$/i) {
			return <<"EOD";
<div style="float:$align;padding:.5em 1.5em .5em 1.5em">
 <img src="$uri" alt="$alt" />
</div>
EOD
		}
	}
	return '';
}
1;
