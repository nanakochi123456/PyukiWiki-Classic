##
# 指定されたRSSを取得し、一覧表示する。
# :書式|
#  #showrss(RSSパス, テンプレート名, キャッシュ生存時間)
# RSSパスにはRSSへのファイルパスやURLを指定する。(省略不可)~
# テンプレート名には取得RSSの表示方法を指定。default(省略時), menubar, recent。~
# キャッシュ生存時間はキャッシュをクリアする期限(1時間単位)。
# 省略すると無効になる。

# http://nekyo.hp.infoseek.co.jp/
# License: GPL2
# Return:LF Code=Shift-JIS 1TAB=4Spaces
use strict;

sub plugin_showrss_inline
{
	return &plugin_showrss_convert(shift);
}

sub plugin_showrss_convert
{
	my @arg = &func_get_args(shift);
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
		my $fp = fopen($rssuri, "r");
		my $result;
		($result, $stream) = &get_rss($fp);
		return $stream if ($result != 0); # $stream is errorcode.

		if ($stream =~ /encoding="[Ee][Uu][Cc]/) {
			$code = "euc";
		} elsif($stream=~/encoding="[Ss][Hh][Ii][Ff][Tt]/) {
			$code = "sjis";
		}
		$stream = &replace(&code_convert(\$stream, $::kanjicode, $code));
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

sub get_rss
{
	my ($fp) = @_;
	my (@log, $data);
	@log = <$fp>;
	sleep(1);
	close($fp);
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
