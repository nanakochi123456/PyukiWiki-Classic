##
# ���դ�ʸ��ɽ��~
# pyukiwiki�ȼ������� _2�Ĥ����Ȳ��դ��ˤʤ롣
#  11001011__2__=0xa9
# 11001011__2__=0xa9 ��ɽ����~
# yukiwiki, pukiwiki �Ȥθߴ�����Ż뤵������Ϥ��Υץ饰�������Ѥ��뤳�ȡ�
#  11001011&sub(2);=0xa9
# 11001011&sub(2);=0xa9 ��ɽ����
use strict;

package sup;

sub plugin_inline {
    my ($escaped_argument) = @_;
    my ($string) = split(/,/, $escaped_argument);
    return qq(<sup>$string</sup>);
}

sub plugin_usage {
    return {
        name => 'sup',
        version => '1.0',
        author => 'Nekyo',
        syntax => '&sup(string)',
        description => 'Make sub.',
        example => '&sup(string)',
    };
}

1;
