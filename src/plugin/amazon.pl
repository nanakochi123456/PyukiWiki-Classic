##
# ���ޥ���(http://www.amazon.co.jp)�ξ��ʤΥ��᡼��������̾��ɽ�����롣~
# ���ե��ꥨ�����б���
# :��|
#  &amazon(ASIN�ֹ�);
#  #amazon
#  #amazon(,clear)
#  #amazon(ASIN�ֹ�,[left|right],[�����ȥ�|image])
# -left|right - ɽ�����ΰ��ֻ��ꡣ��ά����right��~
# -clear - �ƥ����Ȳ����ߤβ����~
# -�����ȥ� - ���ʥ����ȥ����ꡣ��ά���ϼ�ư������
# -image - ���ʤΥ��᡼���Τ�ɽ������ά���ϥ��᡼���ȥ����ȥ��ɽ����
# :����|
# ���ޥ���Υ����������ȥץ������ǧ���뤳�ȡ�~
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
	return '<div style="clear:both"></div>' if ($align eq 'clear'); # ��������

	$align = 'right' if ($align ne 'left');	# ���ַ���

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
	if ($aryargs[2] ne '' and $aryargs[2] ne 'image') { # �����ȥ���꤫��ư������
		$title = &::escape($aryargs[2]); # for XSS
		$alt = $title;
	}
	my $url = "http://images-jp.amazon.com/images/P/$asin_all.MZZZZZZZ.jpg";
	my $div = "";

	my $ref = 'ref=nosim';
	$ref = $af_id if ($af_id ne '');
	if ($title eq '') { # �����ȥ뤬�ʤ���С������Τ�ɽ��
		$div .= <<"EOD";
<div style="float:$align;margin:16px 16px 16px 16px;text-align:center">
<a href="$shop$asin/@{[$asin_aid]}$ref"><img src="$url" alt="$alt" /></a>
</div>
EOD
	} else {			# �̾�ɽ��
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
