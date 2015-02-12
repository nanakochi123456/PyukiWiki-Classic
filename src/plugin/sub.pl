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
        author => 'Nekyo <nekyo@yamaneko.club.ne.jp>',
        syntax => '&sub(string)',
        description => 'Make sub.',
        example => '&sub(string)',
    };
}

1;
