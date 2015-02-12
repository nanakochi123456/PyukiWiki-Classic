############################################################
# online ƒvƒ‰ƒOƒCƒ“
# online.inc.pl
# Copyright(c) 2004 Nekyo.
# for PyukiWiki(http://nekyo.hp.infoseek.co.jp)
# 1TAB=4Spaces

my $timeout = 300;

sub plugin_online_inline {
	return &plugin_online_convert;
}

sub plugin_online_convert {
	my $file = $::counter_dir . 'user.dat';

	if (!(-e $file)) {
		open(FILE, ">$file");
		close(FILE);
	}
	my $addr = $ENV{'REMOTE_ADDR'};

	open(FILE, "<$file");
	flock(FILE, 1);		# lock ReadBlock
	my @usr_arr = <FILE>;
	flock(FILE, 8);		# unlock

	close(FILE);
	open(FILE, ">$file");
	flock(FILE, 2);		# lock WriteBlock
	$now = time();
	foreach (@usr_arr) {
		chomp;
		($ip_addr, $tim_stmp) = split(/|/);

		if (($now - $tim_stmp) < $timeout and $ip_addr ne $addr) {
			print FILE "$ip_addr|$tim_stmp\n";
		}
	}
	print FILE "$addr|$now\n";
	flock(FILE, 8);		# unlock
	close(FILE);

	open(FILE, "<$file");
	flock(FILE, 1);		# lock ReadBlock
	@usr_arr = <FILE>;
	flock(FILE, 8);		# unlock
	close(FILE);
	return @usr_arr;
}
