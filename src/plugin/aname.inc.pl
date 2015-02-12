##
# ���ꤷ�����֤˥��󥫡�(��󥯤�������)�����ꤷ�ޤ���
# :��|
#  &aname(���󥫡�̾,[,{[super],[full],[noid]},���󥫡�ʸ����]);
#  #aname(���󥫡�̾,[,{[super],[full],[noid]},���󥫡�ʸ����])
# ���󥫡�̾�����󥫡��λ���Ҥ˻��Ѥ���롣(��ά�Բ�)��Ⱦ�ѱѻ�(��ʸ��/��ʸ��)�����Ѳ�ǽ��
# super,full,noid �ǥ��󥫡��ν�����������ꤹ�롣
# -super - ���󥫡�ʸ�������դ�ɽ�����롣��ά���Ͼ��դ�ɽ������ʤ���
# -full - �ե饰���Ȼ���Ұʳ���URI���䤤���󥫡�����Ϥ��롣��ά���ϥե饰���Ȼ���ҤΤ߽��Ϥ���롣
# -noid �� ���󥫡��˥ե饰���Ȼ���Ҥ���Ϥ��ʤ���
# ���󥫡�ʸ���󤬻��ꤵ�줿��硢���ꤷ��ʸ������Ф����󥫡������Ϥ���롣���󥫡���¸�ߤ�����������˻��Ѥ��롣��ά���϶�ʸ���Ȥʤ롣

###############################################
# aname plugin
# aname.inc.pl
# Copyright(c) 2004 Nekyo.
# for PyukiWiki(http://nekyo.hp.infoseek.co.jp)
# Based on aname.inc.php by Mr.arino.

sub plugin_aname_inline
{
	my ($args) = @_;
	return plugin_aname_convert($args);
}

sub plugin_aname_convert
{
	return '' if (@_ < 1);	# no param
	my @args = split(/,/, shift);
	my $id = shift(@args);
	return false if (!($id =~ /^[A-Za-z][\w\-]*$/));

	my $body = '';
	if (@args) {
		$body = pop(@args);
		$body =~ s/<\/?a[^>]*>//;
	}
	my $class = 'anchor';
	my $url = '';
	my $attr_id = " id=\"$id\"";

	foreach (@args) {
		if (/super/) {
			$class = 'anchor_super';
		}
		if (/full/) {
			$url = "$script?" . rawurlencode($vars['page']);
		}
		if (/noid/) {
			$attr_id = '';
		}
	}
	return "<a class=\"$class\"$attr_id href=\"$url#$id\" title=\"$id\">$body</a>";
}

1;
