############################################################
# edit plugin
# edit.inc.pl
# Copyright(c) 2004 Nekyo.
# for PyukiWiki(http://nekyo.hp.infoseek.co.jp)
#
# 1TAB=4Spaces
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
