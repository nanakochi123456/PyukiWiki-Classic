##
# 指定した位置にアンカー(リンクの飛び先)を設定します。
# :書式|
#  &aname(アンカー名,[,{[super],[full],[noid]},アンカー文字列]);
#  #aname(アンカー名,[,{[super],[full],[noid]},アンカー文字列])
# アンカー名がアンカーの指定子に使用される。(省略不可)。半角英字(大文字/小文字)が使用可能。
# super,full,noid でアンカーの出力方式を指定する。
# -super - アンカー文字列を上付き表示する。省略時は上付き表示されない。
# -full - フラグメント指定子以外のURIを補いアンカーを出力する。省略時はフラグメント指定子のみ出力される。
# -noid − アンカーにフラグメント指定子を出力しない。
# アンカー文字列が指定された場合、指定した文字列に対しアンカーが出力される。アンカーの存在を明示する場合に使用する。省略時は空文字となる。

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
