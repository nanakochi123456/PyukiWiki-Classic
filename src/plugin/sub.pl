##
# ���դ�ʸ��ɽ��~
# pyukiwiki�ȼ������� ^2�Ĥ����Ⱦ��դ��ˤʤ롣
#  2^^2^^=4
# 2^^2^^=4 ��ɽ����~
# yukiwiki, pukiwiki �Ȥθߴ�����Ż뤵������Ϥ��Υץ饰�������Ѥ��뤳�ȡ�
#  2&sup(2);=4
# 2&sup(2);=4 ��ɽ����
use strict;

package sub;

sub plugin_inline {
    my ($escaped_argument) = @_;
    my ($string) = split(/,/, $escaped_argument);
    return qq(<sub>$string</sub>);
}

sub plugin_usage {
    return {
        name => 'sub',
        version => '1.0',
        author => 'Nekyo',
        syntax => '&sub(string)',
        description => 'Make sub.',
        example => '&sub(string)',
    };
}

1;
