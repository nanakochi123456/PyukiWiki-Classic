############################################################
# comment plugin
# comment.inc.pl
# Copyright(c) 2004 Nekyo.
# v 0.0.1 - ProtoType
# for PyukiWiki(http://nekyo.hp.infoseek.co.jp)
# Based on comment.inc.php by Mr.arino.
# 1TAB=4Spaces
#
use strict;

my $comment_format = "\x08MSG\x08 -- \x08NAME\x08 \x08NOW\x08";

sub plugin_comment_action {
	my $lines = $::database{$::form{mypage}};
	my @lines = split(/\r?\n/, $lines);

	my $datestr = ($::form{nodate} == 1) ? '' : &get_now;
	my $_name = $::form{myname} ? " ''[[$::form{myname}]]'' : " : " ";
	my $_now = "&new{$datestr};";

	my $postdata = '';
	my $_comment_no = 0;

	my $comment = $comment_format;
	$comment =~ s/\x08MSG\x08/$::form{mymsg}/;
	$comment =~ s/\x08NAME\x08/$_name/;
	$comment =~ s/\x08NOW\x08/$_now/;
	$comment = "-" . $comment;

	foreach (@lines) {
		if (/^#comment/ && (++$_comment_no == $::form{comment_no})) {
			if ($::form{above} == 1) {
				$_ = ($comment . "\n" . $_);
			} else {
				$_ .= ("\n" . $comment);
			}
		}
		$postdata .= $_ . "\n";
	}
	if ($::form{mymsg}) {
		$::form{mymsg} = $postdata;
		$::form{mytouch} = 'on';
		&do_write;
	} else {
		$::form{cmd} = 'read';
		&do_read;
	}
	&close_db;
	exit;
}

my $comment_no = 0;

sub plugin_comment_convert {
	my @argv = split(/,/, shift);

	my $above = 1;
	my $nodate = '';
	my $nametags = $::resource{yourname} . '<input type="text" name="myname" value="" size="10">';

	foreach (@argv) {
		chomp;
		if (/below/) {
			$above = 0;
		} elsif (/nodate/) {
			$nodate = 1;
		} elsif (/noname/) {
			$nametags = '';
		}
	}
	$comment_no++;
	my $escapedmypage = &escape($::form{mypage});
	my $conflictchecker = &get_info($::form{mypage}, $::info_ConflictChecker);
	return <<"EOD";
<form action="$::script" method="post">
 <div>
   <input type="hidden" name="comment_no" value="$comment_no" />
   <input type="hidden" name="cmd" value="comment" />
   <input type="hidden" name="mypage" value="$escapedmypage" />
   <input type="hidden" name="myConflictChecker" value="$conflictchecker" />
   <input type="hidden" name="mytouch" value="on" />
   <input type="hidden" name="nodate" value="$nodate" />
   <input type="hidden" name="above" value="$above" />
   $nametags
   <input type="text" name="mymsg" value="" size="40" />
   <input type="submit" value="$::resource{commentbutton}" />
 </div>
</form>
EOD
}
1;
