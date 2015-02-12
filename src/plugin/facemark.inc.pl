##
# フェイスマークをイメージに変換する。(pyukiwiki独自プラグイン)~
# :書式|
#  #facemark(フェイスマーク)
#  &facemark(フェイスマーク);
# フェイスマーク機能を分離してプラグイン化しました。~
# このプラグインを改造することで、フェイスマークを拡張できます。~
# PyukiWiki Classic v0.1.7 or later
use strict;

sub plugin_facemark_inline {
	return &plugin_facemark_convert(shift);
}

sub plugin_facemark_convert {
	my $line = shift;
	$line =~ s!\s(\:\)|\(\^\^\))! <img src="$::image_dir/face/smile.png" alt="$1" width="15" height="15"/>!g;
	$line =~ s!\s(\:D|\(\^-\^\))! <img src="$::image_dir/face/bigsmile.png" alt="$1"  width="15" height="15"/>!g;
	$line =~ s!\s(\:p|\:d)! <img src="$::image_dir/face/huh.png" alt="$1"  width="15" height="15"/>!g;
	$line =~ s!\s(XD|X\(|\(\.\.;)! <img src="$::image_dir/face/oh.png" alt="$1" width="15" height="15"/>!g;
	$line =~ s!\s(;\)|\(\^_-\))! <img src="$::image_dir/face/wink.png" alt="$1" width="15" height="15"/>!g;
	$line =~ s!\s(;\(|\:\(|\(--;\))! <img src="$::image_dir/face/sad.png" alt="$1" width="15" height="15"/>!g;
	$line =~ s!&(heart);!<img src="$::image_dir/face/heart.png" alt="$1" width="15" height="15"/>!g;
	$line =~ s!\s\(\^\^;\)?! <img src="$::image_dir/face/worried.png" alt="$1" width="15" height="15"/>!g;
	return $line;
}
1;
