##
# PyukiWiki Plugin
# lookup.inc.pl v0.2 Nekyo
#
use strict;

sub plugin_lookup_convert {
	my @args = split(/,/, shift);
#	if (@args < 2) { return ''; }
	my $iwn = &htmlspecialchars(&trim($args[0]));
	my $btn = &htmlspecialchars(&trim($args[1]));

	my $default = '';
	if (@args > 2) {
		$default = &htmlspecialchars(trim($args[2]));
	}
	my $s_page = &htmlspecialchars($::form{mypage});
	my $ret = <<"EOD";
<form action="$::script" method="post">
 <div>
  <input type="hidden" name="cmd" value="lookup" />
  <input type="hidden" name="inter" value="$iwn" />
  $iwn:
  <input type="text" name="page" size="30" value="$default" />
  <input type="submit" value="$btn" />
 </div>
</form>
EOD
	return $ret;
}

sub plugin_lookup_action {
	my $text = &::decode($::form{page});

	# pyukiwiki
	my ($code, $uri) = %{$::interwiki2{$::form{inter}}};
	if ($uri) {
		$uri =~ s/\$1/&interwiki_convert($code, $text)/e;
	} else {
		# yukiwiki
		$uri = $::interwiki{$::form{inter}};
		if ($uri) {
			$uri =~ s/\b(utf8|euc|sjis|ykwk|yw|asis)\(\$1\)/&interwiki_convert($1, $text)/e;
		}
	}
	if ($uri) {
		print("Location: $uri\n\n");
		exit;
	}
	return "";
}
1;
