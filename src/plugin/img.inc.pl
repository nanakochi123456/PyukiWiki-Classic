##
# ������ɽ�����롣
# :��|
#  #img(������URI[[,��],alt������])
# �񼰡�r,right(����) or l,left(����) or module(index.cgi ����θƤӽФ�)
# or ����ʳ�(���ꥢ)~
# v0.1.6b ��ꤳ�δؿ��� index.cgi �� img �Ѵ��Ǥ�ƤӽФ��褦������(ɬ��)

######################################################################
# img.inc.pl
# PyukiClassic v 0.1.6b or laiter
# Author: Nekyo
# Copyright (C) 2004-2006 by Nekyo.
# http://nekyo.hp.infoseek.co.jp/
# License: GPL2
######################################################################
use strict;

sub plugin_img_convert {
	my ($uri, $align, $alt) = split(/,/, shift);
	$uri   = &trim($uri);
	$align = &trim($align);
	$alt   = &trim($alt);
	my $module = 0;
	my $res = '';

	if ($align =~ /^(r|right)/i) {
		$align = 'right';
	} elsif ($align =~ /^(l|left)/i) {
		$align = 'left';
	} elsif ($align =~ /^module$/i) {
		$module = 1;
	} else {
		return '<div style="clear:both"></div>';
	}
#	if ($uri =~ /^(https?|ftp):/) {
		if ($uri =~ /\.(gif|png|jpe?g)$/i) {
			if ($module == 1) {
				# ɬ�פǤ���С�������ʬ���ĥ���롣
				$res .= "<a href=\"$uri\"><img src=\"$uri\" /></a>\n";
			} else {
				$res .= "<div style=\"float:$align; padding:.5em 1.5em .5em 1.5em;\"><img src=\"$uri\"";
				$res .= " alt=\"$alt\"" if ($alt ne '');
				$res .= " /></div>\n";
			}
		}
#	}
	return $res;
}
1;
__END__
