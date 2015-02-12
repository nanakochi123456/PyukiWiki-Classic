##
# ページ編集。
# :書式|
#  ?cmd=edit&mypage=ページ名
# ページ名はエンコードされていなければならない。

# @auther Nekyo (http://nekyo.hp.infoseek.co.jp)
# @license: GPL2 and/or Artistic or each later version.
# 1TAB=4Spaces
use strict;

sub plugin_edit_action {
	my ($page) = &unarmor_name(&armor_name($::form{mypage}));
	my $body;
	if (not &is_editable($page)) {
		$body .= qq(<p><strong>$::resource{cantchange}</strong></p>);
	} elsif (&is_frozen($page)) {
		$body .= qq(<p><strong>$::resource{cantchange}</strong></p>);
	} else {
		$body .= &editform($::database{$page},
			&get_info($page, $::info_ConflictChecker), admin=>0);
	}
	return ('msg'=>$page, 'body'=>$body);
}

sub editform {
	my ($mymsg, $conflictchecker, %mode) = @_;
	my $frozen = &is_frozen($::form{mypage});
	my $body = '';

	if ($::form{mypreview}) {
		if ($::form{mymsg}) {
			unless ($mode{conflict}) {
				$body .= qq(<h3>$::resource{previewtitle}</h3>\n);
				$body .= qq($::resource{previewnotice}\n);
				$body .= qq(<div class="preview">\n);
				$body .= &text_to_html($::form{mymsg}, toc=>1);
				$body .= qq(</div>\n);
			}
		} else {
			$body .= qq($::resource{previewempty});
		}
		$mymsg = $::form{mymsg};
	}
	$mymsg =~ s/\n?#freeze\r?\n//g;
	$mymsg = &htmlspecialchars($mymsg);

	my $edit = $mode{admin} ? 'adminedit' : 'edit';
	my $escapedmypage = &htmlspecialchars($::form{mypage});
	my $escapedmypassword = &htmlspecialchars($::form{mypassword});
	if ($::extend_edit) {
		$body .= <<"EOD";
<div>
<a href="javascript:insTag('\\'\\'','\\'\\'','bold');"><b>B</b></a>
<a href="javascript:insTag('\\'\\'\\'','\\'\\'\\'','italic');"><i>I</i></a>
<a href="javascript:insTag('%%%','%%%','underline');"><u>U</u></a>
<a href="javascript:insTag('%%','%%','delline');"><del>D</del></a>
<a href="javascript:insTag('\\n-','','list');">
<img src="$::image_dir/list.gif" alt="list" border="0" vspace="0"
  hspace="1"></a>
<a href="javascript:insTag('\\n+','','list');">
<img src="$::image_dir/numbered.gif" alt="list" border="0" vspace="0"
  hspace="1"></a>
<a href="javascript:insTag('\\nCENTER:','\\n','centering');">
<img src="$::image_dir/center.gif" alt="center" border="0" vspace="0"
  hspace="1"></a>
<a href="javascript:insTag('\\nLEFT:','\\n','left');">
<img src="$::image_dir/left_just.gif" alt="left" border="0" vspace="0"
  hspace="1"></a>
<a href="javascript:insTag('\\nRIGHT:','\\n','right');">
<img src="$::image_dir/right_just.gif" alt="right" border="0" vspace="0"
  hspace="1"></a>
<a href="javascript:insTag('\\n*','','title');"><b>H</b></a>
<a href="javascript:insTag('[[',']]','wikipage');">[[]]</a>
<a href="javascript:insTag('','~\\n','');">&lt;br&gt;</a>
<a href="javascript:insTag('\\n----\\n','','');"><b>--</b></a>
</div>
EOD
	}
	$body .= <<"EOD";
<form action="$::script" method="post" id="editform" name="editform">
  @{[ $mode{admin} ? qq($::resource{frozenpassword} <input type="password" name="mypassword" value="$escapedmypassword" size="10"><br>) : "" ]}
  <input type="hidden" name="myConflictChecker" value="$conflictchecker">
  <input type="hidden" name="mypage" value="$escapedmypage">
  <textarea cols="$::cols" rows="$::rows" name="mymsg">$mymsg</textarea><br />
@{[
  $mode{admin} ?
  qq(
  <input type="radio" name="myfrozen" value="1" @{[$frozen ? qq(checked="checked") : ""]}>$::resource{frozenbutton}
  <input type="radio" name="myfrozen" value="0" @{[$frozen ? "" : qq(checked="checked")]}>$::resource{notfrozenbutton}<br>)
  : ""
]}
@{[$mode{conflict} ? '' :
  qq(
  <input type="submit" name="mypreview_$edit" value="$::resource{previewbutton}">
  <input type="submit" name="mypreview_write" value="$::resource{savebutton}">
  <input type="checkbox" name="mytouch" value="on" checked="checked">$::resource{touch}&nbsp;
  <input type="button" value="$::resource{cancel}" onClick="JavaScript:location.href='$::script?$::form{mypage}'">
)]}
</form>
EOD
	unless ($mode{conflict}) {
		# Show the format rule.
		#open(FILE, $::file_format) or &print_error("($::file_format)");
		#my $content = join('', <FILE>);
		#&code_convert(\$content, $::kanjicode);
		#close(FILE);
		#$body .= &text_to_html($content, toc=>0);
		$body .= &text_to_html($::database{$::rule_page}, toc=>0);

	}
	return $body;
}

1;
