########################/
# PyukiWiki - Yet another WikiWikiWeb clone.
#
# attach.inc.pl
#
# based on PukiWiki attach.inc.php

#use strict;
use CGI qw(:standard);
if ($::use_perlmd5 == 1) {
	eval { use Digest::perl::MD5 qw(md5_hex); };
} else {
	eval { use Digest::MD5 qw(md5_hex); };
}

#--------------------------------------------------------
my %mime = (
	"\.hqx"           => "application/mac-binhex40",
	"\.doc"           => "application/msword",
	"\.pdf"           => "application/pdf",
	"\.(ppt|pps|pot)" => "application/vnd.ms-powerpoint",
	"\.xls"           => "application/vnd.ms-excel",
	"\.sit"           => "application/x-stuffit",
	"\.swf"           => "application/x-shockwave-flash",
	"\.(zip|nar)"     => "application/zip",

	"\.midi?"         => "audio/midi",
	"\.mp3"           => "audio/mpeg",
	"\.wav"           => "audio/x-wav",

	"\.bmp"           => "image/bmp",
	"\.gif"           => "image/gif",
	"\.jpe?g"         => "image/jpeg",
	"\.png"           => "image/png",

	"\.txt"           => "text/plain",

	"\.mpe?g"         => "video/mpeg",
);

# file icon image
if (!$::file_icon) {
	$::file_icon = '<img src="'
		. $::modifierlink_data
		. '/image/file.png" width="20" height="20" alt="file" style="border-width:0px" />';
}

#-------- convert
sub plugin_attach_convert
{
	if (!$::file_uploads) {
		return 'file_uploads disabled';
	}

	my $nolist = 0;
	my $noform = 0;

	my @arg = split(/,/, shift);
	if (@arg > 0) {
		foreach (@arg) {
			$_ = lc $_;
			$nolist |= ($_ eq 'nolist');
			$noform |= ($_ eq 'noform');
		}
	}
	my $ret = '';
	if (!$nolist) {
	#	$obj = &new AttachPages($vars['page']);
	#	$ret .= $obj->toString($vars['page'],1);
	}
	if (!$noform) {
		$ret .= &attach_form($::form{mypage});
	}
	return $ret;
}

my %_attach_messages;

#アップロードフォーム
sub attach_form
{
	my $page = $::form{mypage};	#split(/,/, shift);
#	$r_page = rawurlencode($page);
	my $r_page = $page;
	my $s_page = &::htmlspecialchars($page);
	my $navi =<<"EOD";
  <span class="small">
   [<a href="$::script?cmd=attach&amp;mypage=$page&amp;pcmd=list&amp;refer=$r_page">$::resource{'attach_msg_listpage'}</a>]
   [<a href="$::script?cmd=attach&amp;mypage=$page&amp;pcmd=list">$::resource{'attach_msg_listall'}</a>]
  </span><br />
EOD
	return $navi if (!$::file_uploads);

	my $maxsize = $::max_filesize;
	my $msg_maxsize = $::resource{attach_msg_maxsize};
	my $kb = $maxsize / 1000 . "kb";

	$msg_maxsize =~ s/%s/$kb/g;

	my $pass = '';
	if ($::file_uploads == 2) {
		$pass = '<br />' . $::resource{attach_msg_password}
			. ': <input type="password" name="pass" size="8" />';
	}
	return <<"EOD";
<form enctype="multipart/form-data" action="$::script" method="post">
 <div>
  <input type="hidden" name="cmd" value="attach" />
  <input type="hidden" name="pcmd" value="post" />
  <input type="hidden" name="refer" value="$s_page" />
  <input type="hidden" name="mypage" value="$page" />
  <input type="hidden" name="max_file_size" value="$maxsize" />
  $navi
  <span class="small">
   $msg_maxsize
  </span><br />
  $::resource{'attach_msg_file'}: <input type="file" name="attach_file" />
  $pass
  <input type="submit" value="$::resource{'btn_upload'}" />
 </div>
</form>
EOD
}

sub plugin_attach_action
{
	# backward compatible
	if ($::form{'openfile'} ne '') {
		$::form{'pcmd'} = 'open';
		$::form{'file'} = $::from{'openfile'};
	}
	if ($::form{'delfile'} ne '') {
		$::form{'pcmd'} = 'delete';
		$::form{'file'} = $::form{'delfile'};
	}

	my $age = $::form{age} ? $::form{age} : 0;
	my $pcmd = $::form{pcmd} ? $::form{pcmd} : '';

	# Authentication
#	if ($::form{refer} ne '') { #and is_pagename($vars['refer'])) {
#		my @read_cmds = ('info','open','list');
#		in_array($pcmd,$read_cmds) ?
#			check_readable($vars['refer']) : check_editable($vars['refer']);
#	}

	# Upload
	if ($::form{attach_file} ne '') {
	#	my $pass = $::form{pass} ? md5_hex($::form{pass}) : '';
		return &attach_upload($::form{attach_file}, $::form{refer}, $::form{pass});
	}

	if ($pcmd eq 'info') {
		return &attach_info;
	} elsif ($pcmd eq 'delete') {
		return &attach_delete;
	} elsif ($pcmd eq 'open') {
		return &attach_open;
	} elsif ($pcmd eq 'list') {
		return &attach_list;
	} elsif ($pcmd eq 'freeze') {
		return &attach_freeze(1);
	} elsif ($pcmd eq 'unfreeze') {
		return &attach_freeze(0);
	} elsif ($pcmd eq 'upload') {
		return &attach_showform;
	}
	return &attach_list if ($::form{mypage} eq '' or !$::database{$::form{mypage}});
	return ('msg'=>$::form{mypage}, 'body'=>&attach_form);
}

# 詳細フォームを表示
sub attach_info
{
	my $obj = new AttachFile($::form{refer}, $::form{file}, $::form{age});
	return $obj->getstatus() ? $obj->info()
		: ('msg'=>$::form{refer}, 'body'=>"error:" . $::resource{attach_err_notfound});
}

# 削除
sub attach_delete
{
	if ($::file_uploads == 2 && !&valid_password($::form{pass})) {
		return ('msg'=>$::form{refer}, 'body'=>$::resource{attach_err_password});
	}

	my $obj = new AttachFile($::form{refer}, $::form{file}, $::form{age});
	return $obj->getstatus()
		? $obj->delete()
		: ('msg'=>$::form{mypage}, 'body'=>$::resource{attach_err_notfound});
}

# ダウンロード
sub attach_open
{
	my $obj = new AttachFile($::form{refer}, $::form{file}, $::form{age});
	return $obj->getstatus() ? $obj->open()
		: ('msg'=>$::form{refer}, 'body'=>"error:" . $::resource{attach_err_notfound});
}

# 一覧取得
sub attach_list
{
	my $refer = $::form{refer};
	my $obj = new AttachPages($refer);
	my $msg = $::resource{$refer eq '' ? 'attach_msg_listall' : 'attach_msg_listpage'};
	my $body = $obj->toString(0, 1);
	undef $obj;
	return ('msg'=>$msg,'body'=>$body);
}

# ファイルアップロード
sub attach_upload
{
	my ($filename, $page, $pass) = @_;

	if ($::file_uploads == 2 && !&valid_password($pass)) {
		return ('msg'=>$::form{mypage}, 'body'=>$::resource{attach_err_password});
	}
	my ($parsename, $path, $ffile);
	$parsename = $filename;
	$parsename =~ s#\\#/#g;	# \を/に変換
	$parsename =~ s/^http:\/\///;
	$parsename =~ /([^:\/]*)(:([0-9]+))?(\/.*)?$/;
	$path = $4 || '/';
	$path =~ /(.*\/)(.*)/;			#$ffileには直下のファイル名
	$ffile = $2;			#ファイル名が無い場合'/')
	$ffile =~ s/#.*$//;		# #はページ内リンクなので、削除する

	my $obj = new AttachFile($page, $ffile);
	if ($obj->{exist}) {
		return ('msg'=>$::resource{_attach_err_exists});
	}
	#ファイルの保存
	unless (open (FILE, ">" . $obj->{filename})) {
		print "サーバ側の保存ファイルの作成に失敗しました。: $!\n";
		exit;
	}
	binmode(FILE);
	my $fsize = 0;
	my ($byte, $buffer);
	while ($byte = read($filename, $buffer, 1024)) {
		print FILE $buffer;
		$fsize += $byte;
		if ($fsize > $::max_filesize) {
			close FILE;
			unlink $obj->{filename};
			return ('msg'=>$::form{mypage}, 'body'=>$::resource{attach_err_exceed});
		}
	}
	close FILE;
	return ('msg'=>$::form{mypage}, 'body'=>$::resource{attach_msg_uploaded});

#	$obj->getstatus();
#	$obj->status['pass'] = ($pass !== TRUE and $pass !== NULL) ? $pass : '';
#	$obj->putstatus();

#	return array('result'=>TRUE,'msg'=>$_attach_messages['msg_uploaded'])
#	# パーミッションを変更 
#	chmod (0666, "$Temp/$basename"); 
}

# ファイル名からmimeタイプ取得。
sub attach_mime_content_type
{
	my $filename = shift;
	my $mime_type;
	foreach (keys %mime) {
		next unless ($_ && defined($mime{$_}));
		if ($filename =~ /$_$/i) {
			$mime_type = $mime{$_};
			last;
		}
	}
	return ($mime_type) ? $mime_type : 'application/octet-stream'; #default
}


# php互換関数。
sub md5_file {
	my ($path) = @_;
	open(FILE, $path);
	binmode(FILE);
	my $contents;
	read(FILE, $contents, 16384);
	close(FILE);
	return md5_hex($contents);
}

#----------------------------------------------------
# 1ファイル単位のコンテナ
package AttachFile;

sub new
{
	my $this = bless {};
	shift;
	$this->{page} = shift;	# page
	$this->{file} = shift;	# file
	$this->{age}  = shift;	# age;
	$this->{basename} = $::upload_dir
		. &::dbmname($this->{page}) . '_' . &::dbmname($this->{file});
	$this->{filename} = $this->{basename} . ($this->{age} ? '.' . $this->{age} : '');
	$this->{exist} = (-e $this->{filename}) ? 1 : 0;
	$this->{logname}  = $this->{basename} . ".log";

	$this->{time} = (stat($this->{filename}))[10];
	$this->{md5hash} = ($this->{exist} == 1) ? &::md5_file($this->{filename}) : '';
	return $this;
}

# 添付ファイルのオープン
sub open
{
	my $this = shift;
	my $query = new CGI;

	print $query->header(
		-type=>"$this->{type}",
		-Content_disposition=>"filename=$this->{file}",
		-Content_length=>$this->{size},
		-expires=>"now",
		-P3P=>""
	);
	open(FILE, $this->{filename}) || die $!;
	binmode(FILE);
	my $buffer;
	print $buffer while (read(FILE, $buffer, 4096));
	close(FILE);
	exit;
}

# 情報表示
sub info
{
	my $this = shift;

	my $msg_delete = '<input type="radio" name="pcmd" value="delete" />'
		 . $::resource{attach_msg_delete} . $::resource{attach_msg_require} . '<br />';

	my $info = $this->toString(1, 0);
	my %retval;

	$retval{msg} = $::resource{attach_msg_info};
	$retval{body} =<<EOD;
<p class="small">
 [<a href="$::script?cmd=attach&amp;mypage=$::form{mypage}&amp;pcmd=list&amp;refer=$::form{refer}">$::resource{attach_msg_listpage}</a>]
 [<a href="$::script?cmd=attach&amp;pcmd=list">$::resource{attach_msg_listall}</a>]
</p>
<dl>
 <dt>$info</dt>
 <dd>$::resource{attach_msg_page}:$::form{refer}</dd>
 <dd>$::resource{attach_msg_filename}:$this->{filename}</dd>
 <dd>$::resource{attach_msg_md5hash}:$this->{md5hash}</dd>
 <dd>$::resource{attach_msg_filesize}:$this->{size_str} ($this->{size} bytes)</dd>
 <dd>Content-type:$this->{type}</dd>
 <dd>$::resource{attach_msg_date}:$this->{time_str}</dd>
</dl>
EOD

	if ($::file_uploads) {
		my $msg_pass;

		if ($::file_uploads == 2) {
			$msg_pass = $::resource{attach_msg_password}
			. '<input type="password" name="pass" size="8" />';
		}

		my $s_page = &::htmlspecialchars($this->{page});

		$retval{body} .=<<EOD;
<hr />
<form action="$::script" method="get">
 <div>
  <input type="hidden" name="cmd" value="attach" />
  <input type="hidden" name="mypage" value="$this->{page}" />
  <input type="hidden" name="refer" value="$s_page" />
  <input type="hidden" name="file" value="$this->{file}" />
  <input type="hidden" name="age" value="$this->{age}" />
  $msg_delete
  $msg_pass
  <input type="submit" value="$::resource{attach_btn_submit}" />
 </div>
</form>
EOD
	}
	return %retval;
}

sub delete
{
	my $this = shift;

	# バックアップ
	if ($this->{age}) {
		unlink($this->{filename});
	} else {
		my $age;
		do {
			$age = ++$this->{age};
		} while (-e $this->{basename} . '.' . $age);

		if (!rename($this->{basename}, $this->{basename} . '.' . $age)) {
			# rename 失敗
			return ('msg'=>$this->{page}, 'body'=>$::resource{attach_err_delete});
		}
	}
	return ('msg'=>$this->{page}, 'body'=>$::resource{attach_msg_deleted});
}

# ステータス取得
sub getstatus
{
	my $this = shift;

	return 0 if (!$this->{exist});

	# ログファイル取得
	if (-e $this->{logname}) {
	#	$data = file($this->logname);
	#	foreach ($this->status as $key=>$value)
	#	{
	#		$this->status[$key] = chop(array_shift($data));
	#	}
	#	$this->status['count'] = explode(',',$this->status['count']);
	}
#	$this->time_str = get_date('Y/m/d H:i:s',$this->time);
	my ($sec, $min, $hour, $day, $mon, $year) = localtime($this->{time});
	$this->{time_str} = sprintf("%d/%02d/%02d %02d:%02d:%02d",
			$year + 1900, $mon + 1, $day, $hour, $min, $sec);
	$this->{size} = -s $this->{filename};
	$this->{size_str} = sprintf('%01.1f', $this->{size}/1000) . 'KB';
	$this->{type} = &::attach_mime_content_type($this->{file});
	return 1;
}

# ステータス保存
sub putstatus
{
#	$this->status['count'] = join(',',$this->status['count']);
#	$fp = fopen($this->logname,'wb')
#		or die_message('cannot write '.$this->logname);
#	flock($fp,LOCK_EX);
#	foreach ($this->status as $key=>$value)
#	{
#		fwrite($fp,$value."\n");
#	}
#	flock($fp,LOCK_UN);
#	fclose($fp);
}

# ファイルのリンクを作成
sub toString {
	my $this = shift;
	my $showicon = shift;
	my $showinfo = shift;

	my $body;
	my $finfo = "&file=" . &::encode($this->{file})
		. "&mypage=" . &::encode($::form{mypage})
		. "&refer="  . &::encode($this->{page})
		. ($this->{age} >= 1 ? "&age=$this->{age}" : "");

	$body .= $::file_icon if ($showicon);
	$body .= "<a href=\"$::script?cmd=attach&pcmd=open$finfo\">$this->{file} "
		. ($this->{age} >= 1 ? "(Backup No.$this->{age})" : "") . "</a>";

	if ($showinfo) {
		$body .= " [<a href=\"$::script?cmd=attach&pcmd=info"
		. "$finfo\">$::resource{attach_msg_description}</a>]";
	}
	return $body;
}

#----------------------------------------------------
# ファイル一覧コンテナ作成
package AttachFiles;
my %files;

sub new {
	my $this = bless {};
	shift;
	$this->{page} = shift;	# page
	return $this;
}

sub add {
	my $this = shift;
	my $file = shift;
	my $age  = shift;

	# 美しくないけど３次元配列
	$files{$this->{page}}{$file}{$age} = new AttachFile($this->{page}, $file, $age);
}

# ページ単位の一覧表示
sub toString {
	my $this = shift;
	my $flat = shift;
	my $page = $this->{page};

	my $ret = "";
	my $files = $this->{files};
	$ret .= "<li>" . &::make_link($this->{page}) . "\n<ul>\n";
	my ($target, $notarget, $backup);
	foreach my $key (sort keys %{$files{$page}}) {
		$target = '';
		$notarget = '';
		$backup = '';
		foreach (sort keys %{$files{$page}{$key}}) {
			if ($_ >= 1) {
				$backup .= "<li>" . $files{$page}{$key}{$_}->toString(0, 1) . "</li>\n";
				$notarget = $files{$page}{$key}{$_}->{file};
			} else {
				$target .= $files{$page}{$key}{$_}->toString(0, 1);
			}
		}
		$ret .= "<li>" . ($target ? $target : $notarget);
		$ret .= "\n<ul>\n$backup\n</ul>\n" if ($backup);
		$ret .= "</li>\n";
	}
	return $ret . "</ul>\n</li>\n";
}

sub to_flat {
	my $this = shift;
	my $flat = shift;
	my $ret = "";
	my %files = $this->{files};
	foreach my $key (sort keys %files) {
		foreach (sort keys %{$files{$key}}) {
			$ret .= $key . "." . $_ . $files{$key}{$_}->toString(1, 1) . ' ';
		}
	}
	return $ret;
}

#-------------------------------------------------
# ページコンテナ作成
package AttachPages;

my %pages;

# ページコンテナ作成
sub new {
	my $this = bless {};
	shift;
	$this->{page} = shift;
	my $age = shift;

	opendir(DIR, $::upload_dir)
		or die('directory '. $::upload_dir . ' is not exist or not readable.');
	my @file = readdir(DIR);
	closedir(DIR);

	my $page_pattern = ($this->{page} eq '')
		? '(?:[0-9A-F]{2})+' : &::dbmname($::form{mypage});
	my $age_pattern = ($age eq '') ? '(?:\.([0-9]+))?' : ($age ? "\.($age)" : '');
	my $pattern = "^($page_pattern)_((?:[0-9A-F]{2})+)$age_pattern\$";

	my ($_page, $_file, $_age);

	foreach (@file) {
		next if (!/$pattern/);
		$_page = pack("H*", $1);
		$_file = pack("H*", $2);
		$_age = $3 ? $3 : 0;

		$pages{$_page} = new AttachFiles($_page) if (!exists($pages{$_page}));
		$pages{$_page}->add($_file, $_age);
	}
	return $this;
}

# 全ページの添付一覧表示
sub toString {
	my $this = shift;
	my $page = shift;
	my $flat = shift;

	# page exist check;
	my $body = "";
	foreach (sort keys %pages) {
		$body .= $pages{$_}->toString($flat);
	}
	return "\n<div id=\"body\">" . $::resource{attach_err_noexist} . "</div>\n"
			if ($body eq "");
	return "\n<ul>\n$body</ul>\n";
}

1;
