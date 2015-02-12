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
        author => 'Nekyo <nekyo@yamaneko.club.ne.jp>',
        syntax => '&sup(string)',
        description => 'Make sub.',
        example => '&sup(string)',
    };
}

1;
