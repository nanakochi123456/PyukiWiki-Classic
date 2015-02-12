########################/
# �۲��Υڡ����θ��Ф�(*,**,***)�ΰ�����ɽ������
# :��|
#  #ls2(�ѥ�����[,�ѥ�᡼��])
# -�ѥ�����(�ǽ�˻���)
# -title:���Ф��ΰ�����ɽ������
# -reverse:�ڡ������¤ӽ��ȿž�����߽�ˤ���

# �ʲ���̤�б�
# -include:���󥯥롼�ɤ��Ƥ���ڡ����θ��Ф���Ƶ�Ū����󤹤�
# -link:action�ץ饰�����ƤӽФ���󥯤�ɽ��
# -compact:

# @author Nekyo.
# @version v0.1 2005/04/01 encode �Х� Fix Tnx:Junichi����
# @version v0.0 2004/11/01 �ʰ��� title,reverse �б�������¾�����б�
# @see based on ls2.inc.php by arino

use strict;

sub plugin_ls2_convert
{
	my $prefix = '';
	my @args = split(/,/, shift);
	my $title = 0;
	my $reverse = 0;
	my (@pages, $txt, @txt, $tocnum);
	my $body = '';

    if (@args > 0) {
		$prefix = shift(@args);
		foreach my $arg (@args) {
			if (lc $arg eq "title") {
				$title = 1;
			} elsif (lc $arg eq "reverse") {
				$reverse = 1;
			}
		}
	}
	$prefix = $::form{mypage} . "/" if ($prefix eq '');

	foreach my $page (sort keys %::database) {
		push(@pages, $page) if ($page =~ /^$prefix/);
	}
	@pages = reverse(@pages) if ($reverse);
	foreach my $page (@pages) {
		$body .= <<"EOD";
<li><a id ="list_1" href="$::script?cmd=read&amp;mypage=@{[&encode($page)]}" title="$page">$page</a></li>
EOD
		if ($title) {
			$txt = $::database{$page};
			@txt = split(/\r?\n/, $txt);
			$tocnum = 0;
			my (@tocsaved, @tocresult);
			foreach (@txt) {
				chomp;
				if (/^(\*{1,3})(.+)/) {
					&back_push('ul', length($1), \@tocsaved, \@tocresult);
					push(@tocresult, qq( <li><a href="$::script?$page#i$tocnum">@{[&escape($2)]}</a></li>\n));	
					$tocnum++;
				}
			}
			push(@tocresult, splice(@tocsaved));
			$body .= join("\n", @tocresult);
		}
	}
	if ($body ne '') {
		return << "EOD";
<ul class="list1" style="padding-left:16px;margin-left:16px">$body</ul>
EOD
	}
	return "No page of a low rank layer in '$prefix'<br />\n";
}

1;
