##
# 管理者用編集プラグイン~
# ※内部で edit プラグインの機能を呼び出している。~
# メニューから呼び出される。
# :書式|
# なし

# @author: Nekyo (http://nekyo.hp.infoseek.co.jp/)
# @license: GPL2 and/or Artistic or each later version.

use strict;

sub plugin_adminedit_action {
	if (1 == &exist_plugin('edit')) {
		my ($page) = &unarmor_name(&armor_name($::form{mypage}));
		my $body;
		if (not &is_editable($page)) {
			$body .= qq(<p><strong>$::resource{cantchange}</strong></p>);
		} else {
			$body .= qq(<p><strong>$::resource{passwordneeded}</strong></p>);
			$body .= &editform(
				$::database{$page},
				&get_info($page, $::info_ConflictChecker),
				admin => 1
			);
		}
		return ('msg'=>$page, 'body'=>$body);
	}
	return "";
}
1;
__END__
