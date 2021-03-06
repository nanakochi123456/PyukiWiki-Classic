##
# ページ中の見出し一覧を表示する。
# :書式|
#  #contents
# pyukiwiki独自拡張~
#  #contents([ページ])
# で指定のページの見出し一覧を表示する。

# @author nekyo.
# @version 1.01
# @license:GPL
use strict;

sub plugin_contents_convert {
	my @args = &func_get_args(shift);
	my $page;
	if (@args > 0) {
		$page = $args[0];
		$::pushedpage = $page;
	} else {
		$page = $::form{mypage};
	}
	my ($txt) = $::database{$page};
	my (@txt) = split(/\r?\n/, $txt);
	my $tocnum = 0;
	my (@tocsaved, @tocresult);
	my $title;
	my $nametag = ($::IsMenu == 1) ? "m" : "i";

	foreach (@txt) {
		chomp;
		if (/^(\*{1,5})(.+)/) {
			&back_push('ul', length($1), \@tocsaved, \@tocresult);
			$title = &::inline($2);
			$title =~ s/<[^>]+>//g;
			push(@tocresult, qq(<li><a href="?)
				# &::encode($::form{mypage})
				. &::rawurlencode($::pushedpage eq '' ? $::form{mypage} : $::pushedpage)
				. qq(#$nametag$tocnum">$title</a></li>\n));
			$tocnum++;
		}
	}
	push(@tocresult, splice(@tocsaved));
	my $body = <<EOD;
<div class="contents">
<a id="contents_1"></a>
EOD
	$body .= join("\n", @tocresult) . "</div>\n";
	return $body;
}
1;
