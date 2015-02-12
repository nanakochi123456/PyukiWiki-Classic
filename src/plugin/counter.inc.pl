############################################################
# counter プラグイン
# counter.inc.pl
# Copyright(c) 2004 Nekyo.
# v0.0.1 排他制御追加
# for PyukiWiki(http://nekyo.hp.infoseek.co.jp)
# 1TAB=4Spaces

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

	my $file = $::counter_dir . &encode($page) . $::counter_ext;

	my @keys = keys(%default);
	my $modify = 0;
	if (-e $file) {
		open(FILE, "+<$file") or return "Counter Conflict.<br />\n";
		flock(FILE, 2);
		foreach my $key (@keys) {
			$_ = <FILE>;
			chomp;
			$counter{$key} = $_;
		}
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
			truncate(FILE, 0);	# ファイルサイズを0バイトにする
			seek(FILE, 0, 0);	# ファイルポインタを先頭にセット
		} else {
			open(FILE, ">$file") or return "Counter Conflict.<br />\n";
			flock(FILE, 2);
		}
		foreach my $key (@keys) {
			print FILE $counter{$key} . "\n";
		}
	}
	if (FILE) {
		flock(FILE, 8);
		close(FILE);
	}
	return %counter;
}
1;
