##
# ʸ����˥�Ӥ�դ롣
# :��|
#  &ruby(���){��Ӥ�դ�ʸ����};
# @author Nekyo.
sub plugin_ruby_inline {
	@arg = split(/,/, shift);
	my $ruby = $arg[0];
	my $body = $arg[1];

	if ($ruby eq '' or $body eq '') {
		return '';
	}
	my $s_ruby = &htmlspecialchars($ruby);
	return "<ruby><rb>$body</rb><rp>(</rp><rt>$s_ruby</rt><rp>)</rp></ruby>";
}
1;
