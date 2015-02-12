##
# 下付き文字表示~
# pyukiwiki独自実装で _2つで包むと下付きになる。
#  11001011__2__=0xa9
# 11001011__2__=0xa9 と表示。~
# yukiwiki, pukiwiki との互換性を重視される方はこのプラグインを使用すること。
#  11001011&sub(2);=0xa9
# 11001011&sub(2);=0xa9 と表示。
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
