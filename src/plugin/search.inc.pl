##
# 指定文字列を含むページを検索する。
# :書式|
#  ?cmd=search[パラメータ]
# パラメータに検索条件を指定する。~
# word − 検索文字列。~
# type − 'OR' 指定時、OR検索を行う。(省略時はAND検索)~
# @author Nekyo.
use strict;

sub search {
	my ($word, $type, $base) = @_;
	my %found;
	my $body = "";
	if ($word) {
		my @words = split(/\s+/, $word);
		my $total = 0;
		if (uc($type) eq 'OR') {
			my $firsttime = 1;
			foreach my $wd (@words) {
				foreach my $page (sort keys %::database) {
					if ($base ne '') {
						if ($page !~ /^$base/) {
							next;
						}
					}
					if (($::database{$page} =~ /\Q$wd\E/i) or ($page =~ /\Q$wd\E/i)) {
						$found{$page} = 1;
					}
					if ($firsttime) {
						$total++;
					}
				}
				$firsttime = 0;
			}
		} else {	# AND 検索
			foreach my $page (sort keys %::database) {

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
			$body .= qq|<!-- search result -->\n<ul>| if ($counter == 0);
			$body .= qq(<li><a href ="$::script?@{[&::encode($page)]}">@{[&::htmlspecialchars($page)]}</a>@{[&::htmlspecialchars(&::get_subjectline($page))]}</li>);
			$counter++;
		}
		$body .= ($counter == 0) ? $::resource{notfound} : qq|</ul>\n<!-- search end -->|;
	#	$body .= "$counter / $total <br />\n";
	}
	return $body;
}

sub search_form {
	my ($word, $type, @base) = @_;
	my $result =<<"EOD";
<form action="$::script" method="post">
<div>
  <input type="hidden" name="cmd" value="search">
  <input type="text" name="word" value="$word" size="20" />
  <input type="radio" name="type" value="AND" @{[ ($type ne 'OR' ? qq( checked="checked") : qq()) ]} />$::resource{searchand}
  <input type="radio" name="type" value="OR" @{[ ($type eq 'OR' ? qq( checked="checked") : qq()) ]}/>$::resource{searchor}
  <input type="submit" value="$::resource{searchbutton}" />
</div>
EOD
	if (@base) {
		my $first = ' checked';
		foreach my $bs (@base) {
			if ($bs) {
				$result .= <<"EOD";
  <input type="radio" name="base" value="$bs"$first><strong>$bs</strong>$::resource{search_pages}<br />
EOD
				$first = '';
			}
		}
		if ($first eq '') {
			$result .= <<"EOD";
  <input type="radio" name="base" value=""$first>$::resource{search_all}<br />
EOD


		}
	}
	$result .= "</form>\n";
	return $result;
}

##
# 条件1, 条件2 ... 条件n
sub plugin_search_convert {
	my @arg = split(/,/, shift);
	return &search_form('', 'OR', @arg);
}

##
# PyukiWiki独自機能
# インラインは機能が違う。検索した一覧を表示する。
sub plugin_search_inline {
	my @arg = split(/,/, shift);
	return &search($arg[0], $arg[1]);
}

sub plugin_search_action {
	my $word = &htmlspecialchars($::form{word});
	my $body = &search($word, $::form{type}, $::form{base});
	$body .= &search_form($word, $::form{type}, $::form{base});
	return ('msg'=>$::resource{searchpage}, 'body'=>$body);
}

1;

