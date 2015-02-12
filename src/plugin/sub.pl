##
# 上付き文字表示~
# pyukiwiki独自実装で ^2つで包むと上付きになる。
#  2^^2^^=4
# 2^^2^^=4 と表示。~
# yukiwiki, pukiwiki との互換性を重視される方はこのプラグインを使用すること。
#  2&sup(2);=4
# 2&sup(2);=4 と表示。
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
