############################################################
# contents プラグイン
# contents.inc.pl
# Copyright(c) 2004 Nekyo.
# for PyukiWiki(http://nekyo.hp.infoseek.co.jp)
# 1TAB=4Spaces
# v0.0.2 2005/01/20 base による弊害の対応
# v0.0.1 プロトタイプ

use strict;

sub plugin_contents_convert {
	my ($txt) = $::database{$::form{mypage}};
	my (@txt) = split(/\r?\n/, $txt);
	my $tocnum = 0;
	my (@tocsaved, @tocresult);
	my $title;
	my $nametag = ($::IsMenu == 1) ? "m" : "i";

	foreach (@txt) {
		chomp;
		if (/^(\*{1,3})(.+)/) {
			&back_push('ul', length($1), \@tocsaved, \@tocresult);
			$title = &::inline($2);
			$title =~ s/<[^>]+>//g;
			push(@tocresult, qq(<li><a href="?) . &::encode($::form{mypage})
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
