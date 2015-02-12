############################################################
# showrss.inc.pl
# by Nekyo.
#
use strict;
use Socket;
use FileHandle;
use Jcode;

sub plugin_showrss_inline
{
	return &plugin_showrss_convert(shift);
}

sub plugin_showrss_convert
{
	my @arg = split(/,/, shift);
	return "argument error." if (@arg <= 0);
	my $rssuri   = $arg[0];
	my $tmplname = (@arg >= 2) ? $arg[1] : "";
	my $usecache = (@arg >= 3) ? $arg[2] : 0;

	my $expire = $usecache * 3600;
	my $code = 'utf8';
	my $cachefile = $::cache_dir . "/" . &dbmname($rssuri) . ".tmp";
	my $stream;
	my $body = "";

	my $lastmod = (stat($cachefile))[9];
	if ($lastmod + $expire < time || $lastmod == 0) {
		$rssuri =~ m!(http:)?(//)?([^:/]*)?(:([0-9]+)?)?(/.*)?!;
		my $host = ($3 ne "") ? $3 : "localhost";
		my $port = ($5 ne "") ? $5 : 80;
		my $path = ($6 ne "") ? $6 : "/";

		my $result;
		($result, $stream) = &get_rss($host, $path, $port);
		return $stream if ($result != 0); # $stream is errorcode.

		$stream = &Jcode::convert($stream, $::kanjicode, $code);
		$stream = &replace($stream);
		if (open(OUT, ">$cachefile")) {
			flock(OUT, 2);	# lock WriteBlock
			print OUT $stream;
			flock(OUT, 8);	# unlock
			close OUT;
		}
	} else {
		# read_cache
		my @line;
		open(IN, "<$cachefile") || return "Can't read cache.";
		@line = <IN>;
		close IN;
		undef $stream;
		$stream = join('', @line);
	}

	my %xml = &xmlParser($stream);
	my @title = split(/\n/,
		($xml{'rdf:RDF/item/title'} ne ""
		? $xml{'rdf:RDF/item/title'} : $xml{'rss/channel/item/title'}
		)
	);
	my @date = split(/\n/,
		($xml{'rdf:RDF/item/dc:date'} ne ""
		? $xml{'rdf:RDF/item/dc:date'} : $xml{'rss/channel/dc:date'}
		)
	);
	my @link = split(/\n/,
		($xml{'rdf:RDF/item/link'} ne ""
		? $xml{'rdf:RDF/item/link'} : $xml{'rss/channel/item/link'}
		)
	);

#	my @desc  = split(/\n/, $xml{'rdf:RDF/item/description'});

	my ($footer, $ll, $lr);

	if (lc $tmplname eq "menubar") {
		$body .=<<"EOD";
<div class="small">
<ul class="recent_list">
EOD
		$ll = "<li>";
		$lr = "</li>\n";
		$footer = "</ul>\n</div>\n";
	} elsif (lc $tmplname eq "recent") {
		$body .=<<"EOD";
<div class="small">
<string>$date[0]</strong>
<ul class="recent_list">
EOD
		$ll = "<li>";
		$lr = "</li>\n";
		$footer = "</ul>\n</div>\n";
	} else {
		$ll = $footer = "";
		$lr = "<br />\n";
	}

	my $count = 0;
	foreach (@title) {
		$body .=<<"EOD";
$ll<a href="$link[$count]" title="$title[$count]">$title[$count]</a>$lr
EOD
		$count++;
	}
	$body .= $footer;

	return $body;
}

# rss取得
sub get_rss
{
	my ($host, $path, $port) = @_;
	my (@log, $sock, $sockaddr, $ip, $data);
	$sock = new FileHandle;
	if ($host =~ /^(\d+).(\d+).(\d+).(\d+)$/) {
		$ip = pack('C4', split(/\./, $host));
	} else {
		#HOST名をIPに直す
	#	$ip = (gethostbyname($host))[4] || return (1, "Host Not Found.");
		$ip = inet_aton($host) || return (1, "Host Not Found.");
	}
	$sockaddr = pack_sockaddr_in($port, $ip) || (2, "Can't Create Socket address.");
	socket($sock, PF_INET, SOCK_STREAM, 0) || return (3, "Socket Error.");
	connect($sock, $sockaddr) || return (4, "Can't connect Server.");
	autoflush $sock(1);
	print $sock "GET $path HTTP/1.1\r\nHost: $host\r\n\r\n";
	@log = <$sock>;
	sleep(1);
	close($sock);
	undef $data;
	foreach (@log) {
		s/\r\n/\n/g;
		s/\r/\n/g;
		s/\n//g;
		$data .= $_;
	}
	return (0, $data);
}

sub replace
{
	my ($xmlStream) = @_;
	$xmlStream =~ s/<\?(.*)\?>//g;
	$xmlStream =~ s/<rdf:RDF(.*?)>/<rdf:RDF>/g;
	$xmlStream =~ s/<rss(.*?)>/<rss>/g;
	$xmlStream =~ s/<channel(.*?)>/<channel>/g;
	$xmlStream =~ s/<item(.*?)>/<item>/g;
	$xmlStream =~ s/<content:encoded>(.*?)<\/content:encoded>//g;
	$xmlStream =~ s/\ *\/>/\/>/g;
	$xmlStream =~ s/<([^<>\ ]*)\ ([^<>]*)\/>/<$1>$2<\/$1>/g;
	$xmlStream =~ s/<([^<>\/]*)\/>/<$1><\/$1>/g;
	return $xmlStream;
}

sub xmlParser
{
	my ($stream) = @_;
	my ($i, $ch, $name, @node, $val, $key, %xml);
	my $flg = 0;	# 1:key / 0:value
	foreach $i (0..length $stream) {
		$ch = substr($stream, $i, 1);
		if ($ch eq '<') {
			$flg = 1;
			undef $name;
			foreach (@node) {
				$name .= "$_/";
			}
			chop $name;
			$val =~ s/<//g;
			$val =~ s/>//g;
			$xml{$name} .= "$val\n";
			undef $val;
		}
		if ($flg) {
			$key .= $ch;
		} else {
			$val .= $ch;
		}
		if ($ch eq '>') {
			$flg = 0;
			if ($key =~ /\//) {
				pop @node;
			} else {
				$key =~ s/<//g;
				$key =~ s/>//g;
				push @node, $key;
			}
			undef $key;
		}
	}
	return %xml;
}

1;
