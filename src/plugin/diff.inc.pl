############################################################
# diff Plugin
# diff.inc.pl
# Copyright(c) 2004 Nekyo.
# for PyukiWiki(http://nekyo.hp.infoseek.co.jp)
# v0.2 BugFix $diffbase -> $::diffbase Tnx Yashigani-modoki san
# v0.1 Proto
# 1TAB=4Spaces

sub plugin_diff_action {
	if (not &is_editable($::form{mypage})) {
		&do_read;
		&close_db;
		exit;
	}
	&open_diff;
	my $title = $::form{mypage};
	$_ = &escape($::diffbase{$::form{mypage}});
	&close_diff;
	my $body = qq(<h3>$::resource{difftitle}</h3>);
	$body .= qq($::resource{diffnotice});
	$body .= qq(<pre class="diff">);
	foreach (split(/\n/, $_)) {
		if (/^\+(.*)/) {
			$body .= qq(<b class="added">$1</b>\n);
		} elsif (/^\-(.*)/) {
			$body .= qq(<s class="deleted">$1</s>\n);
		} elsif (/^\=(.*)/) {
			$body .= qq(<span class="same">$1</span>\n);
		} else {
			$body .= qq|??? $_\n|;
		}
	}
	$body .= qq(</pre>);
	$body .= qq(<hr>);
	return ('msg' => $title, 'body' => $body);
}
1;
