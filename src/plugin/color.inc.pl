###############################################
# colorƒvƒ‰ƒOƒCƒ“
# color.inc.pl
# Copyright(c) 2004 Nekyo.
# for PyukiWiki(http://nekyo.hp.infoseek.co.jp)
# 1TAB=4Spaces

sub plugin_color_inline {
	my @args = split(/,/, shift);
	my $bgcolor = '';

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
		return FALSE;
	}
	if ($color eq '' or $body eq '') {
		return FALSE;
	}
	if ($bgcolor ne '') {
		$color .= ';background-color:'.$bgcolor;
	}
	return "<span style=\"color:$color\">$body</span>";
}
1;
