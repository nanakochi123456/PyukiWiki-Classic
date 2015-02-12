######################################################################
# pyukiwiki.ini.cgi - This is PyukiWiki, yet another Wiki clone.
# $Id$
#
# PyukiWiki Classic v0.1.6
# Copyright (C) 2004-2006 by Nekyo, PyukiWiki Developers Team
# http://nekyo.hp.infoseek.co.jp/
#
# Return Code:LF Japanese Code=EUC 1TAB=4Spaces
######################################################################
# ����
$::lang = "ja";       # ja:���ܸ�/en:�Ѹ�(����)
$::kanjicode = "euc"; # euc:EUC-JP/utf8:UTF-8

# �ǡ�����Ǽ�ǥ��쥯�ȥ�
$::data_home   = '.'; # �ڡ����ǡ������Υǥ��쥯�ȥ�
$::data_dir    = "$::data_home/wiki";     # �ڡ����ǡ�����¸��
$::diff_dir    = "$::data_home/diff";     # ��ʬ��¸��
$::cache_dir   = "$::data_home/cache";    # �����
$::upload_dir  = "$::data_home/attach";   # ź����
$::counter_dir = "$::data_home/counter";  # ��������
$::plugin_dir  = "$::data_home/plugin";   # �ץ饰������
$::skin_dir    = "$::data_home/skin";     # ��������
$::image_dir   = "$::data_home/image";    # ������
$::info_dir    = "$::data_home/info";     # ������
$::res_dir     = "$::data_home/resource"; # �꥽����

# ������ե�����
#$::skin_file = 'pyukiwiki.skin.cgi';

# �ץ�������
#$proxy_host = '';
#$proxy_port = 8080;

# �����Ծ���(�������Ʋ�����)
$::modifier      = 'YourName';          # ������̾
$::modifierlink  = 'http://localhost/'; # ������URI
$::modifier_mail = '';                  # �����ԥ᡼�륢�ɥ쥹

# �ǥե���ȥڡ���̾
$::script        = 'index.cgi';
$::FrontPage     = 'FrontPage';
$::RecentChanges = 'RecentChanges';
$::CreatePage    = 'CreatePage';
$::IndexPage     = 'IndexPage';
$::MenuBar       = 'MenuBar';
$::Header        = ':Header';
$::Footer        = ':Footer';
$::rule_page     = "�����롼��";

# �����Υѥ����(�ѹ����Ʋ�����)
$::adminpass = crypt("pass", "AA");

# RSS����(�ѹ����Ʋ�����)
$::modifier_rss_title       = "PyukiWiki $::version";
$::modifier_rss_link        = 'http://localhost/';
$::modifier_rss_description = 'This is PyukiWiki.';

# ɽ������
$::usefacemark = 1;                   # �ե������ޡ��� 1:����/0:̤����
$::use_popup = 0;                     # ����� 1:�ݥåץ��å�/0:�ڡ�������
$::last_modified = 2;                 # �ǽ������� 0:��ɽ��/1:���ɽ��/2:����ɽ��
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

#
$::_symbol_anchor = '&dagger;';
$::maxrecent = 50;

# ���������������˴ޤ�ʤ��ڡ���̾(����ɽ����)
$::non_list = '^\:';
# �ʲ��� md5('pass') �ν��Ϸ�̤Ǥ�
#$adminpass = &md5('pass');

# Skin �� gzip �ѥ������ꤹ��Ȱ��̤�ͭ���ˤʤ롣
#$::gzip_path = '/bin/gzip -1';
$::gzip_path = '';

1;
