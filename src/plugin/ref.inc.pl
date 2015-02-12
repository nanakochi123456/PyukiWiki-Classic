######################################################
#*プラグイン ref
#ページに添付されたファイルを展開する
#URLを展開する
#
#*Usage
# #ref(filename[,page][,parameters][,title])
#
#*パラメータ
# -filename~
# 添付ファイル名、あるいはURL~
# 'ページ名/添付ファイル名'を指定すると、そのページの添付ファイルを参照する
# -page~
# ファイルを添付したページ名(省略可)~
# -パラメータ
# --Left|Center|Right~
# 横の位置合わせ
# --Wrap|Nowrap~
# テーブルタグで囲む/囲まない
# -Around~
# テキストの回り込み
# -noicon~
# アイコンを表示しない
# -nolink~
# 元ファイルへのリンクを張らない
# -noimg~
# 画像を展開しない
# -zoom~
# 縦横比を保持する
# -999x999~
# サイズを指定(幅x高さ)
# -999%~
# サイズを指定(拡大率)
# -その他~
# imgのalt/hrefのtitleとして使用~
# ページ名やパラメータに見える文字列を使用するときは、#ref(hoge.png,,zoom)のように
# タイトルの前にカンマを余分に入れる

use strict;

my $file_icon = '<img src="'
	. $::image_dir
	. '/file.png" width="20" height="20" alt="file" style="border-width:0px" />';

# default alignment
my $ref_default_align = 'left'; # 'left','center','right'

# force wrap on default
my $REF_WRAP_TABLE = 0; # 1,0

sub plugin_ref_inline
{
	my ($args) = @_;
	my @args = split(/,/, $args);
	return 'no argument(s).' if (@args < 1);	#エラーチェック
	my %params = &plugin_ref_body($args, $::form{mypage});
	return ($params{_error}) ? $params{_error} : $params{_body};
}

sub plugin_ref_convert
{
	my ($args) = @_;
	my @args = split(/,/, $args);
	return '<p>no argument(s).</p>' if (@args < 1);	#エラーチェック
	my %params = &plugin_ref_body($args, $::form{mypage});

	# divで包む
	my $style;
	if ($params{around}) {
		$style = ($params{_align} eq 'right') ? 'float:right' : 'float:left';
	} else {
		$style = "text-align:$params{_align}";
	}
	return "<div class=\"img_margin\" style=\"$style\">$params{_body}</div>\n";
}

sub getimagesize
{
	my ($imgfile, $datafile) = @_;
	my $width  = 0;
	my $height = 0;
	my ($data, $m, $c, $l);

	if (!$datafile) {
		$datafile = $imgfile;
	}

	if ($imgfile =~ /\.jpe?g$/i) {
		open(FILE, "$datafile") || return (0, 0);
		binmode FILE;
		read(FILE, $data, 2);
		while (1) { # read Exif Blocks
			read(FILE, $data, 4);
			($m, $c, $l) = unpack("a a n", $data);
			if ($m ne "\xFF") {
				$width = $height = 0;
				last;
			} elsif ((ord($c) >= 0xC0) && (ord($c) <= 0xC3)) {
				read(FILE, $data, 5);
				($height, $width) = unpack("xnn", $data);
				last;
			} else {
				read(FILE, $data, ($l - 2));
			}
		}
		close(FILE);
	} elsif ($imgfile =~ /\.gif$/i) {
		open(FILE, "$datafile") || return (0,0);
		binmode(FILE);
		sysread(FILE, $data, 10);
		close(FILE);
		$data = substr($data, -4) if ($data =~ /^GIF/);

		$width  = unpack("v", substr($data, 0, 2));
		$height = unpack("v", substr($data, 2, 2));
	} elsif ($imgfile =~ /\.png$/i) {
		open(FILE, "$datafile") || return (0,0);
		binmode(FILE);
		read(FILE, $data, 24);
		close(FILE);

		$width  = unpack("N", substr($data, 16, 20));
		$height = unpack("N", substr($data, 20, 24));
	}
	return ($width, $height);
}

sub plugin_ref_body
{
	my ($args) = @_;
	my @args = split(/,/, $args);
	my $name = &trim(shift(@args));
	my $page;

#	my %params = {
#		'left'   => 0,	# 左寄せ
#		'center' => 0,	# 中央寄せ
#		'right'  => 0,	# 右寄せ
#		'wrap'   => 0,	# TABLEで囲む
#		'nowrap' => 0,	# TABLEで囲まない
#		'around' => 0,	# 回り込み
#		'noicon' => 0,	# アイコンを表示しない
#		'nolink' => 0,	# 元ファイルへのリンクを張らない
#		'noimg'  => 0,	# 画像を展開しない
#		'zoom'   => 0,	# 縦横比を保持する
#		'_size'  => 0,	# (サイズ指定あり)
#		'_w'     => 0,	# (幅)
#		'_h'     => 0,	# (高さ)
#		'_%'     => 0,	# (拡大率)
#		'_args'  => '',
#		'_done'  => 0,
#		'_error' => ''
#	};

	my (%params, $_title, $_backup);
	foreach (@args) {
		$_backup = $_;
		$_ = &trim($_);
		if (/^([0-9]+)x([0-9]+)$/i) { # size pixcel
			$params{_size} = 1;
			$params{_w} = $1;
			$params{_h} = $2;
		} elsif (/^([0-9.]+)%$/i) { # size %
			$params{_par} = $1;
		} elsif (/(left|center|right|wrap|nowrap|around|noicon|nolink|noimg|zoom)/i) { # align
			$params{lc $_} = 1;
		} else {
			if (!$page and &is_exist_page($_)) {
				$page = $_;
			} else {
				$_title = $_backup;
			}
		}
	}

	my ($url, $url2, $title, $is_image, $info);
	my $width  = 0;
	my $height = 0;

	if ($name =~ /^(https?|ftp|news)(:\/\/[-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]*)$/) {	#URL
		$url = $url2 = &htmlspecialchars($name);
		$title = &htmlspecialchars(($name =~ '/([^\/]+)$/') ? $1 : $url);
		$is_image = (!$params{noimg} and $name =~ /\.(gif|png|jpe?g)$/i);
	} else {	# 添付ファイル
		if (!-d "$::upload_dir/") {
			$params{_error} = 'no $::upload_dir.';
			return %params;
		}
		# ページ指定のチェック
		$page = $::form{mypage} if (!$page);
		if ($name =~ /^(.+)\/([^\/]+)$/) {
			$1 .= '/' if ($1 eq '.' or $1 eq '..');
			$page = get_fullname($1, $page);
			$name = $2;
		}
		$title = &htmlspecialchars($name);
		my $file  = "$::upload_dir/" . &::dbmname($page) . '_' . &::dbmname($name);
		# my $file2 = "$::upload_dir/" . &::dbmname($page) . '_' . &::dbmname($name);
		if (!-e $file) {
			$params{_error} = 'file not found.' . $file;
			return %params;
		}
		$is_image = (!$params{noimg} and $name =~ /\.(gif|png|jpe?g)$/i);

		$url = "$::script?cmd=attach&amp;pcmd=open"
			. "&amp;file=$name&amp;mypage=$page&amp;refer=$page";
		if ($is_image) {
			($width, $height) = getimagesize($name, $file);
			$url2 = $url;
		#	$url = $file2;
			$url =($::download_dir ne '') ? "$::download_dir/" : "$::upload_dir/" . &::dbmname($page) . '_' . &::dbmname($name);
		} else {
			my ($sec, $min, $hour, $day, $mon, $year) = localtime((stat($file))[10]);
			$info = sprintf("%d/%02d/%02d %02d:%02d:%02d %01.1fK",
				$year + 1900, $mon + 1, $day, $hour, $min, $sec,
				(-s $file) / 1000
			);
		}
	}

	# 画像サイズ調整
	if ($is_image) {
		# 指定されたサイズを使用する
		if ($params{_size}) {
			if ($width == 0 and $height == 0) {
				$width  = $params{_w};
				$height = $params{_h};
			} elsif ($params{zoom}) {
				my $_w = $params{_w} ? $width  / $params{_w} : 0;
				my $_h = $params{_h} ? $height / $params{_h} : 0;
				my $zoom = ($_w > $_h) ? $_w : $_h;
				if ($zoom != 0) {
					$width  = ($width  / $zoom);
					$height = ($height / $zoom);
				}
			} else {
				$width  = $params{_w} ? $params{_w} : $width;
				$height = $params{_h} ? $params{_h} : $height;
			}
		}
		if ($params{_par}) {
			$width  = ($width  * $params{_par} / 100);
			$height = ($height * $params{_par} / 100);
		}
		if ($width and $height) {
			$info = "width=\"$width\" height=\"$height\" ";
		}
	}

	#アラインメント判定
	if ($params{right}) {
		$params{_align} = 'right';
	} elsif ($params{left}) {
		$params{_align} = 'left';
	} elsif ($params{center}) {
		$params{_align} = 'center';
	} else {
		$params{_align} = $ref_default_align;
	}

	$title = $_title if ($_title);

	# ファイル種別判定
	if ($is_image) {	# 画像
		my $_url = "<img src=\"$url\" alt=\"$title\" title=\"$title\" $info/>";
		if (!$params{nolink} and $url2) {
			$_url = "<a href=\"$url2\" title=\"$title\">$_url</a>";
		}
		$params{_body} = $_url;
	} else {	# 通常ファイル
		my $icon = $params{noicon} ? '' : $file_icon;
		$params{_body} = "<a href=\"$url\" title=\"$info\">$icon$title</a>\n";
	}
	return %params;
}

1;
