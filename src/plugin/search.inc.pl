############################################################
# search プラグイン
# search.inc.pl
# Copyright(c) 2004 Nekyo.
# for PyukiWiki(http://nekyo.hp.infoseek.co.jp)
#
# 1TAB=4Spaces

sub plugin_search_action {
	my $body = "";
	my $word = &htmlspecialchars($::form{mymsg});
	if ($word) {
		@words = split(/\s+/, $word);
		my $total = 0;
		if ($::form{type} eq 'OR') {
			foreach my $wd (@words) {
				$total = 0;
				foreach my $page (sort keys %::database) {
					next if $page =~ /^$::RecentChanges$/;
					if ($::database{$page} =~ /\Q$wd\E/i or $page =~ /\Q$wd\E/i) {
						$found{$page} = 1;
					}
					$total++;
				}
			}
		} else {	# AND 検索
			foreach my $page (sort keys %::database) {
				next if $page =~ /^$::RecentChanges$/;

				my $exist = 1;
				foreach my $wd (@words) {
					if (!($::database{$page} =~ /\Q$wd\E/i or $page =~ /\Q$wd\E/i)) {
						$exist = 0;
					}
				}
				if ($exist) {
					$found{$page} = 1;
				}
				$total++;
			}
		}
		my $counter = 0;
		foreach my $page (sort keys %found) {
			$body .= qq|<ul>| if ($counter == 0);
			$body .= qq(<li><a href ="$::script?@{[&htmlspecialchars($page)]}">@{[&htmlspecialchars($page)]}</a>@{[&htmlspecialchars(&get_subjectline($page))]}</li>);
			$counter++;
		}
		$body .= ($counter == 0) ? $::resource{notfound} : qq|</ul>|;
	#	$body .= "$counter / $total <br />\n";
	}
	$body .= <<"EOD";
<form action="$::script" method="post">
<div>
  <input type="hidden" name="cmd" value="search">
  <input type="text" name="mymsg" value="$word" size="20" />
  <input type="radio" name="type" value="AND" @{[ ($::form{type} ne 'OR' ? qq( checked="checked") : qq()) ]} />$::resource{searchand}
  <input type="radio" name="type" value="OR" @{[ ($::form{type} eq 'OR' ? qq( checked="checked") : qq()) ]}/>$::resource{searchor}
  <input type="submit" value="$::resource{searchbutton}" />
</div>
</form>
EOD
	return ('msg'=>$::resource{searchpage}, 'body'=>$body);
}
1;
