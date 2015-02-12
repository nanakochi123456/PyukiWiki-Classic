##
# �ʰ׷Ǽ��Ĥ����֤��롣
# :��|
#  #article 

# PyukiWiki BBS���ץ饰����
# 2007/01/15 ���ѥ��к�
# 2004/06/12 Nekyo(c) http://nekyo.hp.infoseek.co.jp/
# Based on OKAWARA,Satoshi's PukiWiki Plugin
use strict;

$article::cols = 70;						# �ƥ����ȥ��ꥢ�Υ�����
$article::rows = 5;							# �ƥ����ȥ��ꥢ�ιԿ�
$article::name_cols = 24;					# ̾���ƥ����ȥ��ꥢ�Υ�����
$article::subject_cols = 60;				# ��̾�ƥ����ȥ��ꥢ�Υ�����
$article::name_format = '[[$name]]';		# ̾���������ե����ޥå�
$article::subject_format = '**$subject';	# ��̾�������ե����ޥå�
$article::ins = 0;							# ����������� 1:����� 0:��θ�
$article::comment = 1;						# ����߲��˰�ԥ����Ȥ� 1:����� 0:����ʤ�
$article::auto_br = 1;						# ���Ԥ�ưŪ�Ѵ� 1:���� 0:���ʤ�
$article::no = 0;

my $_no_name = "";
my $_no_subject = "no subject";

sub plugin_article_action
{
	return if ($::form{msg} =~ /^\s*$/); # msg �ʤ��ǽ������ʤ���
	my $postdata = $::form{msg};

	&::spam_filter($postdata, 1);
	my $name = $_no_name;
	if ($::form{name} ne '') {
		#&::spam_filter($::form{name}, 0);	# ���ܸ�����å��ϹԤ�ʤ���
		$name = $article::name_format;
		$name =~ s/\$name/$::form{name}/g;
	}
	my $subject = $article::subject_format;
	if ($::form{subject} ne '') {
		#&::spam_filter($::form{subject}, 0);	# ���ܸ�����å��ϹԤ�ʤ���
		$subject =~ s/\$subject/$::form{subject}/g;
	} else {
		$subject =~ s/\$subject/$_no_subject/g;
	}
	my $artic = "$subject\n>$name (@{[&get_now]})~\n~\n$::form{msg}\n";
	$artic .= "\n#comment\n" if ($article::comment);
	$postdata = '';
	my @postdata_old = split(/\r?\n/, $::database{$::form{'mypage'}});
	my $_article_no = 0;

	foreach (@postdata_old) {
		$postdata .= $_ . "\n" if (!$article::ins);
		if (/^#article/ && (++$_article_no == $::form{article_no})) {
			$postdata .= "$artic\n";
		}
		$postdata .= $_ . "\n" if ($article::ins);
	}
	$::form{mymsg} = $postdata;
	$::form{mytouch} = 'on';
	&do_write("FrozenWrite");
	&close_db;
	exit;
}

sub plugin_article_convert
{
	$article::no++;
	my $conflictchecker = &get_info($::form{mypage}, $::info_ConflictChecker);
	return <<"EOD";
<form action="$::script" method="post">
 <div>
  <input type="hidden" name="article_no" value="$article::no" />
  <input type="hidden" name="cmd" value="article" />
  <input type="hidden" name="mypage" value="$::form{'mypage'}" />
  <input type="hidden" name="myConflictChecker" value="$conflictchecker" />
  <input type="hidden" name="mytouch" value="on" />
  $::resource{article_name} <input type="text" name="name" size="$article::name_cols" /><br />
  $::resource{article_subject} <input type="text" name="subject" size="$article::subject_cols" /><br />
  <textarea name="msg" rows="$article::rows" cols="$article::cols"></textarea><br />
  <input type="submit" value="$::resource{article_btn}" />
 </div>
</form>
EOD
}

1;
