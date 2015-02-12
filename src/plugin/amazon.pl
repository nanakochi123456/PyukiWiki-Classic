##
# アマゾン(http://www.amazon.co.jp)の商品のイメージ、商品名を表示する。~
# アフェリエイト対応。
# :書式|
#  &amazon(ASIN番号);
#  #amazon
#  #amazon(,clear)
#  #amazon(ASIN番号,[left|right],[タイトル|image])
# -left|right - 表示時の位置指定。省略時はright。~
# -clear - テキスト回り込みの解除。~
# -タイトル - 商品タイトルを指定。省略時は自動取得。
# -image - 商品のイメージのみ表示。省略時はイメージとタイトルを表示。
# :備考|
# アマゾンのアソシエイトプログラムを確認すること。~
use strict;
package amazon;

my $shop = 'http://www.amazon.co.jp/exec/obidos/ASIN/';
my $af_id = 'pyukiwikipubl-22';

sub plugin_block
{
	return &plugin_inline(@_);
}

sub plugin_inline
{
	my @aryargs = split(/,/, shift);

	return '' if (@aryargs < 1 or @aryargs > 3);
	my $asin_aid = '';
	my $align = 'left';	# Set Dafault align;
	$align = lc $aryargs[1] if (@aryargs > 1);
	return '<div style="clear:both"></div>' if ($align eq 'clear'); # 改行挿入

	$align = 'right' if ($align ne 'left');	# 配置決定

	my $asin_all = &::escape($aryargs[0]);

	my $asin = '';
	if ($asin_all =~ /^([A-Z0-9]{10}).?([0-9][0-9])?$/) {
		$asin = $1;
		my $asin_ext = ($2 eq '') ? "09" : $2;
		$asin_all = "$asin.$asin_ext";
	} elsif ($align ne 'clear') {
		return 'Not Asin Code';
	}

	my $title = '';
	my $alt = '';
	if ($aryargs[2] ne '' and $aryargs[2] ne 'image') { # タイトル指定か自動取得か
		$title = &::escape($aryargs[2]); # for XSS
		$alt = $title;
	}
	my $url = "http://images-jp.amazon.com/images/P/$asin_all.MZZZZZZZ.jpg";
	my $div = "";

	my $ref = 'ref=nosim';
	$ref = $af_id if ($af_id ne '');
	if ($title eq '') { # タイトルがなければ、画像のみ表示
		$div .= <<"EOD";
<div style="float:$align;margin:16px 16px 16px 16px;text-align:center">
<a href="$shop$asin/@{[$asin_aid]}$ref"><img src="$url" alt="$alt" /></a>
</div>
EOD
	} else {			# 通常表示
		$div .= <<"EOD";
<div style="float:$align;padding:.5em 1.5em .5em 1.5em;text-align:center">
<table style="width:110px;border:0;text-align:center">
  <tr>
    <td style="text-align:center">
      <a href="$shop$asin/@{[$asin_aid]}$ref"><img src="$url" alt="$alt" /></a>
    </td>
  </tr>
  <tr>
    <td style="text-align:center">
      <a href="$shop$asin/@{[$asin_aid]}$ref">$title</a>
    </td>
  </tr>
</table>
</div>
EOD
	}
	return $div;
}

sub plugin_usage {
	return {
		name => 'amazon',
		version => '1.0',
		author => 'Nekyo.',
		syntax => '&amazon(...)',
		description => 'show amazon books.',
		example => '&amazon(asincode,...)',
	};
}

1;
