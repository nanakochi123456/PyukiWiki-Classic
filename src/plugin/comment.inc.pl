##
# コメント入力欄を表示する。
# :書式|
#  #comment({[above],[below],[nodate],[noname]})
# -above - コメントを入力欄の上に追加する。
# -below - コメントを入力欄の下に追加する。(default)
# -nodate - コメントに挿入時刻を付加しない。(省略時は付加する。)
# -noname - 記入者名の入力欄を非表示とする。(省略時は表示。)

# Copyright(c) 2004 Nekyo.
# v 0.0.3 - 2006/01/15 Tnx:Birgus-Latro
# v 0.0.2 - 2004/10/28 Tnx:Birgus-Latro
# v 0.0.1 - ProtoType
# for PyukiWiki(http://nekyo.hp.infoseek.co.jp)
# Based on comment.inc.php by Mr.arino.
# 1TAB=4Spaces
use strict;

my $comment_format = "\x08MSG\x08 -- \x08NAME\x08 \x08NOW\x08";

sub plugin_comment_action {
	my $comment = $::form{mymsg};

	&::spam_filter($comment, 1);

	my $lines = $::database{$::form{mypage}};
	my @lines = split(/\r?\n/, $lines);
	my $datestr = ($::form{nodate} == 1) ? '' : &get_now;
	my $_name = " ";

	if ($::form{myname}) {
	#	&::spam_filter($::form{myname}, 0);
		$_name = " ''[[$::form{myname}]]'' : ";
	}
	my $_now = "&new{$datestr};";
	my $postdata = '';
	my $_comment_no = 0;

	$comment = $comment_format;
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

		&do_write('FrozenWrite');
	} else {
		$::form{cmd} = 'read';
		&do_read;
	}
	&close_db;
	exit;
}

my $comment_no = 0;
my %comment_numbers = {}; # Tnx:Birgus-Latro

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
	if (!exists $comment_numbers{$::form{mypage}}) { # Tnx:Birgus-Latro
		$comment_numbers{$::form{mypage}} = 0;
	}
	$comment_no = ++$comment_numbers{$::form{mypage}};
	my $escapedmypage = &htmlspecialchars($::form{mypage});
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
