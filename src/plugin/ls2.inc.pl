########################/
# 配下のページの見出し(*,**,***)の一覧を表示する
# :書式|
#  #ls2(パターン[,パラメータ])
# -パターン(最初に指定)
# -title:見出しの一覧を表示する
# -reverse:ページの並び順を反転し、降順にする

# 以下は未対応
# -include:インクルードしているページの見出しを再帰的に列挙する
# -link:actionプラグインを呼び出すリンクを表示
# -compact:

# @author Nekyo.
# @version v0.1 2005/04/01 encode バグ Fix Tnx:Junichiさん
# @version v0.0 2004/11/01 簡易版 title,reverse 対応、その他は非対応
# @see based on ls2.inc.php by arino

use strict;

sub plugin_ls2_convert
{
	my $prefix = '';
	my @args = split(/,/, shift);
	my $title = 0;
	my $reverse = 0;
	my (@pages, $txt, @txt, $tocnum);
	my $body = '';

    if (@args > 0) {
		$prefix = shift(@args);
		foreach my $arg (@args) {
			if (lc $arg eq "title") {
				$title = 1;
			} elsif (lc $arg eq "reverse") {
				$reverse = 1;
			}
		}
	}
	$prefix = $::form{mypage} . "/" if ($prefix eq '');

	foreach my $page (sort keys %::database) {
		push(@pages, $page) if ($page =~ /^$prefix/);
	}
	@pages = reverse(@pages) if ($reverse);
	foreach my $page (@pages) {
		$body .= <<"EOD";
<li><a id ="list_1" href="$::script?cmd=read&amp;mypage=@{[&encode($page)]}" title="$page">$page</a></li>
EOD
		if ($title) {
			$txt = $::database{$page};
			@txt = split(/\r?\n/, $txt);
			$tocnum = 0;
			my (@tocsaved, @tocresult);
			foreach (@txt) {
				chomp;
				if (/^(\*{1,3})(.+)/) {
					&back_push('ul', length($1), \@tocsaved, \@tocresult);
					push(@tocresult, qq( <li><a href="$::script?$page#i$tocnum">@{[&escape($2)]}</a></li>\n));	
					$tocnum++;
				}
			}
			push(@tocresult, splice(@tocsaved));
			$body .= join("\n", @tocresult);
		}
	}
	if ($body ne '') {
		return << "EOD";
<ul class="list1" style="padding-left:16px;margin-left:16px">$body</ul>
EOD
	}
	return "No page of a low rank layer in '$prefix'<br />\n";
}

1;
