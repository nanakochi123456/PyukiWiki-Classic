############################################################
# contents ƒvƒ‰ƒOƒCƒ“
# contents.inc.pl
# Copyright(c) 2004 Nekyo.
# for PyukiWiki(http://nekyo.hp.infoseek.co.jp)
# 1TAB=4Spaces

sub plugin_contents_convert {
	my ($txt) = $::database{$::form{mypage}};
	my (@txt) = split(/\r?\n/, $txt);
	my $tocnum = 0;
	my (@tocsaved, @tocresult);
	foreach (@txt) {
		chomp;
		if (/^(\*{1,3})(.+)/) {
			&back_push('ul', length($1), \@tocsaved, \@tocresult);
			push(@tocresult, qq( <li><a href="#i$tocnum">@{[&escape($2)]}</a></li>\n));
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
