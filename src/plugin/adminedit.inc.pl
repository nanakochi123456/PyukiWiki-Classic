######################################################################
# adminedit.inc.pl - This is PyukiWiki, yet another Wiki clone.
#
# PyukiWiki Classic 0.1.6
# Author: Nekyo
# Copyright (C) 2004-2006 by Nekyo.
# http://nekyo.hp.infoseek.co.jp/
# Copyright (C) 2005-2006 PyukiWiki Developers Team
# http://pyukiwiki.sourceforge.jp/
# Based on YukiWiki http://www.hyuki.com/yukiwiki/
# Powerd by PukiWiki http://pukiwiki.sourceforge.jp/
# License: GPL2 and/or Artistic or each later version
#
# This program is free software; you can redistribute it and/or
# modify it under the same terms as Perl itself.
# Return:LF Code=EUC-JP 1TAB=4Spaces
######################################################################

use strict;

sub plugin_adminedit_action {
	if (1 == &exist_plugin('edit')) {
		my ($page) = &unarmor_name(&armor_name($::form{mypage}));
		my $body;
		if (not &is_editable($page)) {
			$body .= qq(<p><strong>$::resource{cantchange}</strong></p>);
		} else {
			$body .= qq(<p><strong>$::resource{passwordneeded}</strong></p>);
			$body .= &editform($::database{$page},
				&get_info($page, $::info_ConflictChecker), admin=>1);
		}
		return ('msg'=>$page, 'body'=>$body);
	}
	return "";
}
1;
__END__
