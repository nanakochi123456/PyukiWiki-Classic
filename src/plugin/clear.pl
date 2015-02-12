######################################################################
# clear.pl - This is PyukiWiki, yet another Wiki clone.
# clear plugin for YukiWiki & PyukiWiki
#
# $Id: clear.pl,v 1.1 2006/01/11 23:14:26 papu Exp $
#
# PyukiWiki Version 0.1.6-alpha1
# Copyright (C) 2004 by Nekyo.
# Copyright (C) 2006 PyukiWiki Developers Team
# License: GPL v2 or (at your option) any later version
# http://nekyo.hp.infoseek.co.jp/
# http://pyukiwiki.sourceforge.jp/
#
# Based on YukiWiki <hyuki@hyuki.com> http://www.hyuki.com/yukiwiki/
# Powerd by PukiWiki http://pukiwiki.sourceforge.jp/
#
# 1TAB=4Spaces
#
# This program is free software; you can redistribute it and/or
# modify it under the same terms as Perl itself.
# Return Code:UNIX=LF/Windows=CR+LF/Mac=CR
# Japanese Code=EUC
######################################################################
# Author: Nanami <nanami@daiba.cx>
######################################################################

use strict;
package clear;

sub plugin_inline {
	return '<div class="clear"></div>';
}
1;
