#
# Based on lookup.inc.php,v 1.9 arino Exp $
use strict;

sub plugin_lookup_convert {
	my @args = split(/,/, shift);
#	if (@args < 2) { return ''; }
	my $iwn = &escape(&trim($args[0]));
	my $btn = &escape(&trim($args[1]));

	my $default = '';
	if (@args > 2) {
		$default = &escape(trim($args[2]));
	}
	my $s_page = &escape($::form{mypage});
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
	my $remoteurl = $::interwiki{$::form{inter}};
	my $text = &decode($::form{page});
	#print "Content-type: text/html\n\n";

	if ($remoteurl) {
		$remoteurl =~ s/\b(utf8|euc|sjis|ykwk|asis)\(\$1\)/&interwiki_convert($1, $text)/e;
		print ("Location: $remoteurl\n\n");
		exit;
	}
	return "";
}
1;
