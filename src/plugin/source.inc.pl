##
# �ڡ����Υ�������ɽ�����롣
# :��|
#  ?cmd=source&page=�ڡ���̾
# @author: Nekyo.
use strict;
sub plugin_source_action {
	return if ($::form{'page'} eq '');
	my $page = $::form{'page'};
	print "Content-Type: text/plain\r\n\r\n";
	print $::database{$page};
	&close_db;
	exit(0);
}
1;
