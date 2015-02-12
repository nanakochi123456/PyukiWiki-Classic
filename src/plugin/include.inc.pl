##
# 記述した位置に引数で指定したページを表示する。
# :書式|
#  #include(ページ名)
sub plugin_include_convert {
	my $page = shift;
	if ($page eq '') { return ''; }
	my $body = '';
	if (&is_exist_page($page)) {
		my $rawcontent = $::database{$page};
		$body = &text_to_html($rawcontent, toc=>1);
		my $cookedpage = &encode($page);
		my $link = "<a href=\"$::script?$cookedpage\">$page</a>";
		if ($::form{mypage} eq $::MenuBar) {
			$body = <<"EOD";
<span align="center"><h5 class="side_label">$link</h5></span>
<small>$body</small>
EOD
		} else {
			$body = "<h1>$link</h1>\n$body\n";
		}
	}
	return $body;
}
1;
