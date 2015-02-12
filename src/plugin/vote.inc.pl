#################################################
# vote ƒvƒ‰ƒOƒCƒ“
# vote.inc.pl
# Copyright(c) 2004 Nekyo.
# for PyukiWiki(http://nekyo.hp.infoseek.co.jp)
# Based on vote.inc.php by Mr.arino.
# 1TAB=4Spaces
#

sub plugin_vote_action
{
	my $lines = $::database{$::form{mypage}};
	my @lines = split(/\r?\n/, $lines);

	my $vote_no = 0;
	my $title = '';
	my $body = '';
	my $postdata = '';
	my @args = ();
	my $cnt = 0;
	my $write = 0;

	foreach (@lines) {
		if (/^#vote\(([^\)]*)\)s*$/) {
			if (++$vote_no != $::form{vote_no}) {
				$postdata .= $_ . "\n";
				next;
			}
			@args = split(/,/, $1);
			$vote_str = '';
			foreach my $arg (@args) {
				$cnt = 0;
				if ($arg =~ /^(.+)\[(\d+)\]$/) {
					$arg = $1;
					$cnt = $2;
				}
				my $e_arg = &encode($arg);
				my $vote_e_arg = "vote_" . $e_arg;

				if ($::form{$vote_e_arg} && ($::form{$vote_e_arg} eq $::resource{vote_plugin_votes})) {
					$cnt++;
				}
				if ($vote_str ne '') {
					$vote_str .= ',';
				}
				$vote_str .= $arg . '[' . $cnt . ']';
			}
			$vote_str = '#vote(' . $vote_str . ")\n";
			$postdata .= $vote_str;
			$write = 1;
		} else {
			$postdata .= $_ . "\n";
		}
	}
	if ($write) {
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

my $vote_no = 0;

sub plugin_vote_convert
{
	$vote_no++;
	my @args = split(/,/, shift);
	return '' if (@args == 0);

	my $escapedmypage = &escape($::form{mypage});
	my $conflictchecker = &get_info($::form{mypage}, $::info_ConflictChecker);
	my $body = <<"EOD";
<form action="$script" method="post">
 <table cellspacing="0" cellpadding="2" class="style_table" summary="vote">
  <tr>
   <td align="left" class="vote_label" style="padding-left:1em;padding-right:1em"><strong>$::resource{vote_plugin_choice}</strong>
    <input type="hidden" name="vote_no" value="$vote_no" />
    <input type="hidden" name="cmd" value="vote" />
    <input type="hidden" name="mypage" value="$escapedmypage" />
    <input type="hidden" name="myConflictChecker" value="$conflictchecker" />
    <input type="hidden" name="mytouch" value="on" />
   </td>
   <td align="center" class="vote_label"><strong>$::resource{vote_plugin_votes}</strong></td>
  </tr>
EOD

	my $tdcnt = 0;
	my $cnt = 0;
	my $link = '';
	my $cls = '';
	foreach (@args) {
		$cnt = 0;

		if (/^(.+)\[(\d+)\]$/) {
			$link = $1;
			$cnt = $2;
		}
		$e_arg = &encode($link);
		$cls = ($tdcnt++ % 2)  ? 'vote_td1' : 'vote_td2';
		$body .= <<"EOD";
  <tr>
   <td align="left" class="$cls" style="padding-left:1em;padding-right:1em;">$link</td>
   <td align="right" class="$cls">$cnt&nbsp;&nbsp;
    <input type="submit" name="vote_$e_arg" value="$::resource{vote_plugin_votes}" class="submit" />
   </td>
  </tr>
EOD
	}

	$body .= <<"EOD";
 </table>
</form>
EOD
	return $body;
}
1;
