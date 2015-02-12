#
# PyukiWiki BugTrack�ץ饰����
# for Pyukiwiki http://nekyo.hp.infoseek.co.jp/
#
# Based on Pukiwiki BugTrack�ץ饰���� (c)Y.MASUI GPL2 http:#masui.net/pukiwiki/
# Special Thanks! koma http://kamoland.com/
# 
# �ѹ�����:
#  2002.06.17: ���Ϥ�
#
use strict;

@bugtrack::priority_list = ('�۵�','����','����','��');
@bugtrack::state_list = ('���','���','CVS�Ԥ�','��λ','��α','�Ѳ�');
@bugtrack::state_sort = ('���','CVS�Ԥ�','��α','��λ','���','�Ѳ�');
@bugtrack::state_bgcolor = ('#ccccff','#ffcc99','#ccddcc','#ccffcc','#ffccff','#cccccc','#ff3333');

$bugtrack::title = '$1 Bugtrack Plugin';
$bugtrack::base = '�ڡ���';
$bugtrack::summary = '���ޥ�';
$bugtrack::priority = 'ͥ����';
$bugtrack::state = '����';
$bugtrack::name = '��Ƽ�';
$bugtrack::date = '�����';
$bugtrack::body = '��å�����';
$bugtrack::category = '���ƥ��꡼';
$bugtrack::pagename = '�ڡ���̾';
$bugtrack::pagename_comment = '<small>����Τޤޤ��ȼ�ưŪ�˥ڡ���̾�������ޤ���</small>';
$bugtrack::version_comment = '<small>����Ǥ⹽���ޤ���</small>';
$bugtrack::version = '�С������';
$bugtrack::submit = '�ɲ�';

sub plugin_bugtrack_action
{
	if ($::form{mode} eq 'submit') {
		&plugin_bugtrack_write(
			$::form{base}, $::form{pagename}, $::form{summary}, $::form{name}, $::form{priority},
			$::form{state}, $::form{category}, $::form{version}, $::form{body}
		);
		exit;
	}
	return ('msg'=>$bugtrack::title, 'body'=>&plugin_bugtrack_print_form($::form{category}));
}

sub plugin_bugtrack_print_form
{
	my ($base, @category) = @_;
	my $select_priority = '';
	my $i;
	for ($i = 0; $i < @bugtrack::priority_list; ++$i) {
		my $selected = ($i < @bugtrack::lugin_priority_list - 1) ? '' : ' selected="selected"';
		$select_priority .= "<option value=\"$bugtrack::priority_list[$i]\"$selected>$bugtrack::priority_list[$i]</option>\n";
	}

	my $select_state = '';
	for ($i = 0; $i < @bugtrack::state_list; ++$i) {
		$select_state .= "<option value=\"$bugtrack::state_list[$i]\">$bugtrack::state_list[$i]</option>\n";
	}

	my $encoded_category = '<input name="category" type="text" />';
	if (@category != 0) {
		$encoded_category = '<select name="category">';
		foreach my $_category (@category) {
			my $s_category = &htmlspecialchars($_category);
			$encoded_category .= "<option value=\"$s_category\">$s_category</option>\n";
		}
		$encoded_category .= '</select>';
	}

	my $s_base = &htmlspecialchars($base);
	my $body = <<"EOD";
<form action="$::script" method="post">
 <table border="0">
  <tr>
   <th>$bugtrack::name</th>
   <td><input name="name" size="20" type="text" /></td>
  </tr>
  <tr>
   <th>$bugtrack::category</th>
   <td>$encoded_category</td>
  </tr>
  <tr>
   <th>$bugtrack::priority</th>
   <td><select name="priority">$select_priority</select></td>
  </tr>
  <tr>
   <th>$bugtrack::state</th>
   <td><select name="state">$select_state</select></td>
  </tr>
  <tr>
   <th>$bugtrack::pagename</th>
   <td><input name="pagename" size="20" type="text" />$bugtrack::pagename_comment</td>
  </tr>
  <tr>
   <th>$bugtrack::version</th>
   <td><input name="version" size="10" type="text" />$bugtrack::version_comment</td>
  </tr>
  <tr>
   <th>$bugtrack::summary</th>
   <td><input name="summary" size="60" type="text" /></td>
  </tr>
  <tr>
   <th>$bugtrack::body</th>
   <td><textarea name="body" cols="60" rows="6"></textarea></td>
  </tr>
  <tr>
   <td colspan="2" align="center">
    <input type="submit" value="$bugtrack::submit" />
    <input type="hidden" name="cmd" value="bugtrack" />
    <input type="hidden" name="mode" value="submit" />
    <input type="hidden" name="base" value="$s_base" />
   </td>
  </tr>
 </table>
</form>
EOD
	return $body;
}

sub plugin_bugtrack_template
{
	my ($base, $summary, $name, $priority, $state, $category, $version, $body) = @_;

	$name = &::armor_name($name);
	$base = &::armor_name($base);
	return <<"EOD";
*$summary

-$bugtrack::base: $base
-$bugtrack::name: $name
-$bugtrack::priority: $priority
-$bugtrack::state: $state
-$bugtrack::category: $category
-$bugtrack::date: @{[&get_now]}
-$bugtrack::version: $version

**$bugtrack::body
$body
----

#comment
EOD
}

sub plugin_bugtrack_write
{
	my ($base, $pagename, $summary, $name, $priority, $state, $category, $version, $body) = @_;

	$base = &::unarmor_name($base);
	$pagename = &::unarmor_name($pagename);

	my $postdata = &plugin_bugtrack_template($base, $summary, $name, $priority, $state, $category, $version, $body);

	my $page;
	my $i = 0;
	do {
		$i++;
		$page = "$base/$i";
	} while ($::database{$page});

	if ($pagename == '') {
		$::form{mypage} = $page;
		$::form{mymsg} = $postdata;
		$::form{mytouch} = 'on';
		&do_write;
		exit;
	} else {
	#	$pagename = get_fullname($pagename,$base);
		# ���Ǥ˥ڡ�����¸�ߤ��뤫��̵���ʥڡ���̾�����ꤵ�줿
	#	if (is_page($pagename) or !$::database{$pagename}) {
			# �ڡ���̾��ǥե���Ȥ��᤹
			$pagename = $page;
	#	} else {
	#		page_write($page,"move to [[$pagename]]");
	#	}
	#	page_write($pagename,$postdata);
	}

	return $page;
}

sub plugin_bugtrack_convert
{
	my $base = $::form{mypage};
	my @category = split(/,/, shift);
	if (@category > 0) {
		my $_base = &::unarmor_name(shift(@category));
		if ($::database{$_base}) {
			$base = $_base;
		}
	}
	return &plugin_bugtrack_print_form($base, @category);
}


sub plugin_bugtrack_pageinfo
{
	my ($page, $no) = @_;

	if (@_ == 1) {
		$no = ($page =~ /\/([0-9]+)$/) ? $1 : 0;
	}
	my $body = $::database{$page};

	if ($body =~ /move\s*to\s*($::WikiName|$::InterWikiName|\[\[$::BracketName\]\])/) {
		return &plugin_bugtrack_pageinfo(&::unarmor_name($1), $no);
	}
	my ($summary, $name, $priority, $state, $category);
	$summary = $name = $priority = $state = $category = 'test';
	my @itemlist = ($bugtrack::summary, $bugtrack::name, $bugtrack::priority, $bugtrack::state, $bugtrack::category);
	foreach my $itemname (@itemlist) {
		if ($body =~ /-\s*$itemname\s*:\s*(.*)\s*/) {
			if ($itemname eq $bugtrack::name) {
				$name = &htmlspecialchars(&::unarmor_name($1));
			} elsif ($itemname eq $bugtrack::summary) {
				$summary = &::htmlspecialchars($1);
			} elsif ($itemname eq $bugtrack::priority) {
				$priority = &::htmlspecialchars($1);
			} elsif ($itemname eq $bugtrack::state) {
				$state = &::htmlspecialchars($1);
			} elsif ($itemname eq $bugtrack::category) {
				$category = &::htmlspecialchars($1);
			}
		}
	}

	if ($body =~ /\*([^\n]+)/) {
		$summary = $1;
	}
	return join('<>', ($page, $no, $summary, $name, $priority, $state, $category));
}

sub plugin_bugtrack_list_convert
{
	my ($_page) = split(',', shift);
	my $page = $::form{mypage};

	# �����ǻ��ꤵ�줿�ڡ�����¸�ߤ����顢���Υڡ�������Ѥ��롣
	$page = $_page if ($::database{$_page});

	my @data = ();
	my $pattern = "$page/";
	my $pattern_len = length($pattern);
	my ($line, $i);

	foreach $page (keys %::database) {
		if (index($page, $pattern) == 0 && substr($page, $pattern_len) =~ /[1-9][0-9]*/) {
			$line = &plugin_bugtrack_pageinfo($page);
			push(@data, $line);
		}
	}

	my @table;
	for ($i = 0; $i < @bugtrack::state_list; $i++) {
		$table[$i] = '';
	}

	foreach $line (@data) {
		my ($page, $no, $summary, $name, $priority, $state, $category) = split(/<>/, $line);
		my $state_no = $#bugtrack::state_list;
		for ($i = 0; $i <= $#bugtrack::state_sort; $i++) {
			if ($bugtrack::state_sort[$i] eq $state) {
				$state_no = $i;
				last;
			}
		}
		my $page_link = &::make_link($page);
		my $bgcolor = $bugtrack::state_bgcolor[$state_no];
		my $row = <<"EOD";
 <tr>
  <td style="background-color:$bgcolor">$page_link</td>
  <td style="background-color:$bgcolor">$state</td>
  <td style="background-color:$bgcolor">$priority</td>
  <td style="background-color:$bgcolor">$category</td>
  <td style="background-color:$bgcolor">$name</td>
  <td style="background-color:$bgcolor">$summary</td>
 </tr>
EOD
		$table[$state_no] .= "$no<>$row\n\n";
	}
	my $table_html = <<"EOD";
<table border="1">
 <tr>
  <th>&nbsp;</th>
  <th>$bugtrack::state</th>
  <th>$bugtrack::priority</th>
  <th>$bugtrack::category</th>
  <th>$bugtrack::name</th>
  <th>$bugtrack::summary</th>
 </tr>
EOD

	for ($i = 0; $i <= $#bugtrack::state_list; $i++) {
		my (%rowlist) = {};
		foreach my $tab (split(/\n\n/, $table[$i])) {
			my($no, $row) = split(/<>/, $tab);
			$rowlist{$no} = $row;
		}
		my (@newkeys) = sort {$b <=> $a} keys(%rowlist);
		foreach my $newkey (@newkeys) {
			$table_html .= "$rowlist{$newkey}\n";
		}
	}
	return $table_html . "</table>";
}

1;
