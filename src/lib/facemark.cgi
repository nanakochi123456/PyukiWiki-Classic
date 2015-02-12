##
# Face Mark Module by Nekyo.
# for PyukiWiki Classic v0.1.7 or later
# If you custamize face mark then override this module.
use strict;

##
# Face Mark Convert to image
# @param $line before replace
# @return $line after replace
sub facemark {
	my $line = shift;
	$line =~ s!\s(\:\)|\(\^\^\))! <img src="$::image_dir/face/smile.png" alt="$1" />!g;
	$line =~ s!\s(\:D|\(\^-\^\))! <img src="$::image_dir/face/bigsmile.png" alt="$1" />!g;
	$line =~ s!\s(\:p|\:d)! <img src="$::image_dir/face/huh.png" alt="$1" />!g;
	$line =~ s!\s(XD|X\(|\(\.\.;)! <img src="$::image_dir/face/oh.png" alt="$1" />!g;
	$line =~ s!\s(;\)|\(\^_-\))! <img src="$::image_dir/face/wink.png" alt="$1" />!g;
	$line =~ s!\s(;\(|\:\(|\(--;\))! <img src="$::image_dir/face/sad.png" alt="$1" />!g;
	$line =~ s!&(heart);!<img src="$::image_dir/face/heart.png" alt="$1" />!g;
	$line =~ s!\s\(\^\^;\)?! <img src="$::image_dir/face/worried.png" alt="$1" />!g;


	# face2
	$line =~ s!\s(8\))! <img src="$::image_dir/face2/glass.png" alt="$1" />!g;
	$line =~ s!\s(B\))! <img src="$::image_dir/face2/sunglass.png" alt="$1" />!g;
	$line =~ s!\s(\|\))! <img src="$::image_dir/face2/sleep.png" alt="$1" />!g;
	$line =~ s!\s(\:o|\:O)! <img src="$::image_dir/face2/oh2.png" alt="$1" />!g;
	$line =~ s!\s(\[:\))! <img src="$::image_dir/face2/headphone.png" alt="$1" />!g;
	$line =~ s!\s(\[:\|\])! <img src="$::image_dir/face2/robot.png" alt="$1" />!g;
	return $line;
}
1;
