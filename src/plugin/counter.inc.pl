##
# ページカウンタを設置する。
# :書式|
#  #counter
#  &counter([total|today|yesterday]);
# -total - 総参照回数。(デフォルト)
# -today - 本日参照回数。
# -yesterday − 昨日参照回数
# @author nekyo.
# @version 0.0.2

sub plugin_counter_inline {
	my $arg = shift;
	my %counter = plugin_counter_get_count($::form{mypage});
	my $count;
	if ($arg =~/(today|yesterday)/i) {
		$count = $counter{$arg};
	} else {
		$count = $counter{'total'}
	}
	return " $count";
}

sub plugin_counter_convert {
	my %counter = plugin_counter_get_count($::form{mypage});
	return <<"EOD";
<div class="counter">
Counter: $counter{'total'},
today: $counter{'today'},
yesterday: $counter{'yesterday'}
</div>
EOD
}

sub plugin_counter_get_count {
	my $page = shift;

	my ($mday, $mon, $year) = (localtime(time))[3..5];
	$year += 1900;
	$mon += 1;
	my $date = "$year/$mon/$mday";

	my %default = (
		'total'     => 0,
		'date'      => $date,
		'today'     => 0,
		'yesterday' => 0,
		'ip'        => ''
	);

	my %counter = %default;

	if (!&is_exist_page($page)) {
		return %default;
	}

	$page =~ s/(\C)/unpack('H2', $1)/eg;

	my $file = $::counter_dir . "/" . $page . $::counter_ext;

	my @keys = keys(%default);
	my $modify = 0;
	if (-e $file) {
		open(FILE, "+<$file") or return "Counter Conflict.<br />\n";
		flock(FILE, 2);
		$_ = <FILE>;
		chomp;
		$counter{'total'} = $_;
		$_ = <FILE>;
		chomp;
		$counter{'date'} = $_;
		$_ = <FILE>;
		chomp;
		$counter{'today'} = $_;
		$_ = <FILE>;
		chomp;
		$counter{'yesterday'} = $_;
		$_ = <FILE>;
		chomp;
		$counter{'ip'} = $_;
	} else {
		open(FILE, ">$file") or return "Counter Conflict.<br />\n";
		flock(FILE, 2);
		$counter{'date'} = "";
	}

	if ($counter{'date'} ne $default{'date'}) {
		$modify = 1;
		$counter{'ip'}        = $ENV{'REMOTE_ADDR'};
		$counter{'date'}      = $default{'date'};
		$counter{'yesterday'} = $counter{'today'};
		$counter{'today'}     = 1;
		$counter{'total'}++;
	} elsif ($counter{'ip'} ne $ENV{'REMOTE_ADDR'}) {
		$modify = 1;
		$counter{'ip'}        = $ENV{'REMOTE_ADDR'};
		$counter{'today'}++;
		$counter{'total'}++;
	}

	if ($modify == 1) {
		if (FILE) {
			truncate(FILE, 0);	#
			seek(FILE, 0, 0);	#
		} else {
			open(FILE, ">$file") or return "Counter Conflict.<br />\n";
			flock(FILE, 2);
		}
		print FILE $counter{'total'} . "\n";
		print FILE $counter{'date'} . "\n";
		print FILE $counter{'today'} . "\n";
		print FILE $counter{'yesterday'} . "\n";
		print FILE $counter{'ip'} . "\n";
	}
	if (FILE) {
		flock(FILE, 8);
		close(FILE);
	}
	return %counter;
}
1;
