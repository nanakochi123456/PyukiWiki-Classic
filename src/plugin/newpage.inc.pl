############################################################
# newpage ƒvƒ‰ƒOƒCƒ“
# newpage.inc.pl
# Copyright(c) 2004 Nekyo.
# for PyukiWiki(http://nekyo.hp.infoseek.co.jp)
#
# 1TAB=4Spaces

sub plugin_newpage_action {
	my $body =<<"EOD";
<form action="$::script" method="post">
    <input type="hidden" name="cmd" value="edit">
    $::resource{newpagename}
    <input type="text" name="mypage" value="" size="20">
    <input type="submit" value="$::resource{createbutton}"><br>
</form>
EOD
	return ('msg' => $::CreatePage, 'body' => $body);
}
1;
