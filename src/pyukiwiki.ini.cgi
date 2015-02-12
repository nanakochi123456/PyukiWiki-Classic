##############################
# pyukiwiki.ini.cgi
#
# Copyright (C) 2004 by Nekyo.
# http://nekyo.hp.infoseek.co.jp/
#
# 1TAB=4Spaces
##############################

# ����
$::lang = "ja";       # ja:���ܸ�/en:�Ѹ�(����)
$::kanjicode = "euc"; # euc:EUC-JP/utf8:UTF-8

##
# �ǡ�����Ǽ�ǥ��쥯�ȥ�
#
# �̾�������
$::data_home = '.';
$::uri_home = $::data_home;
#
# nifty ����
# $::data_home = '/cgi-bin';
# $::uri_home  = 'http://homepage?.nifty.com';

$::data_dir    = "$::data_home/wiki";		# �ڡ����ǡ�����¸��
$::diff_dir    = "$::data_home/diff";		# ��ʬ��¸��
$::cache_dir   = "$::data_home/cache";		# �����
$::upload_dir  = "$::data_home/attach";		# ź����
$::counter_dir = "$::data_home/counter";	# ��������
$::plugin_dir  = "$::data_home/plugin";		# �ץ饰������
$::skin_dir    = "$::data_home/skin";		# ��������
$::info_dir    = "$::data_home/info";		# ������
$::res_dir     = "$::data_home/resource";
$::js_dir      = "$::skin_dir/js";
$::css_dir     = "$::skin_dir/css";

$::skin_uri    = "$::uri_home/skin";
$::image_dir   = "$::uri_home/image";		# ������
$::js_uri      = "$::skin_uri/js";
$::css_uri     = "$::skin_uri/css";

# ������ե�����(��ά�� pyukiwiki.skin.cgi �����ͤ���롣)
#$::skin_file = 'pyukiwiki.skin.cgi';

# �ץ�������(�����)
#$proxy_host = '';
#$proxy_port = 8080;

# �����Ծ���
$::modifier = 'You Name';				# ������̾
$::modifierlink = 'Your Site Address';	# ������URI
$::modifier_mail = '';					# �����ԥ᡼�륢�ɥ쥹

# �ǥե���ȥڡ���̾
$::script        = 'index.cgi';
$::FrontPage     = 'FrontPage';
$::CreatePage    = 'CreatePage';
$::IndexPage     = 'IndexPage';
$::MenuBar       = 'MenuBar';
$::Header        = ':Header';
$::Footer        = ':Footer';
$::rule_page     = "�����롼��";

# �����ԥѥ���ɤ����� pass ¦���� AA �Ϥ��Τޤޡ�
$::adminpass = crypt("pass", "AA");

# RSS����
$::modifier_rss_title = "PyukiWiki $::version";
$::modifier_rss_description = 'This is PyukiWiki.';
#$::modifier_rss_link = 'http://nekyo.hp.infoseek.co.jp/';	# ���ꤵ��Ƥ����rss�Υ�󥯤����Ƥ���ˤʤ롣

# ɽ������
$::use_popup = 0;     # ������ 1:�ݥåץ��å�/0:�ڡ�������
$::last_modified = 2; # �ǽ������� 0:��ɽ��/1:���ɽ��/2:����ɽ��
$::lastmod_prompt = 'Last-modified:'; # �ǽ��������Υץ��ץ�

$::enable_convtime = 1; # ����С��ȥ����� 1:ɽ��/0:��ɽ��;

# �����ե����ޥå�
$::date_format = 'Y-m-d'; # replace &date; to this format.
$::time_format = 'H:i:s'; # replace &time; to this format,

# �ڡ����Խ�
$::cols = 80;       # �ƥ����ȥ��ꥢ�Υ�����
$::rows = 25;       # �ƥ����ȥ��ꥢ�ιԿ�
$::extend_edit = 1; # ��ĥ��ǽ(JavaScript) 1:����/0:̤����

# ź��
$::file_uploads = 2;       # ź�դ� 0:�Ȥ�ʤ�/1:�Ȥ�/2:ǧ���դ��ǻȤ�
$::max_filesize = 1000000; # ���åץ��ɥե�����κ����

$::_symbol_anchor = '&dagger;';
$::maxrecent = 50;

# ���������������˴ޤ�ʤ��ڡ���̾(����ɽ����)
$::non_list = '^\:';

# Skin �� gzip �ѥ������ꤹ��Ȱ��̤�ͭ���ˤʤ롣
#$::gzip_path = '/bin/gzip -1';
$::gzip_path = '';

# ���줬���ꤵ��Ƥ����RSS�Υ�󥯤�����ˤʤ롣
#$::rssurl = "http://nekyo.hp.infoseek.co.jp/rss.shtml";

##
# �ե��륿����Ϣ
#$::filter_flg = 1;	# 1�ǥե��륿����ǽ��ͭ���ˤ��롣
#$::chk_uri_count = 20;	# 1�Ĥ���ƥۡ���ڡ������ɥ쥹��20�İʾ夢��ȥ��ѥ�Ȥߤʤ���
#$::chk_jp_only = 1;	# ���ܸ줬��������äƤ��ʤ��ȥ��ѥ�Ȥߤʤ���
#$::deny_log = "$::cache_dir/deny.log";	# ���ե����롣���ꤵ��Ƥ���ȥ����롣̵���Ƥ�����ʤ���

# �ػ�ʸ�������ꡣʣ��ʸ���ϲ��Ԥ�Ϣ��
#$::disablewords = "poker";

1;
