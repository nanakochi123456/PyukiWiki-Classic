##############################
# pyukiwiki.ini.cgi
#
# Copyright (C) 2004 by Nekyo.
# http://nekyo.hp.infoseek.co.jp/
#
# 1TAB=4Spaces
##############################
use strict;

# Modifier Info.
$::modifierlink = 'http://Change me!/';
$::modifier = 'Nekyo';
$::modifier_mail = '';

$::modifier_dir_data = '.'; # Your data directory (not URL, but DIRECTORY).
$::modifierlink_data = '.'; # Your data URL (not DIRECTORY, but URL).
$::icontag = qq(<img id="logo" src="$::modifierlink_data/pyukiwiki.png" width="80" height="80" alt="[PyukiWiki]" title="[PyukiWiki]" />);

# Language
$::lang = "ja";       # ja:Japanese/cn:Chainese/en:English
$::kanjicode = "euc"; # euc:EUC-JP/utf8:UTF-8

# Page Info
$::script = 'wiki.cgi';
$::FrontPage = 'FrontPage';
$::RecentChanges = 'RecentChanges';
$::CreatePage = 'CreatePage';
$::IndexPage = 'IndexPage';
$::MenuBar = 'MenuBar';

# RSS
$::modifier_rss_title = "PyukiWiki $::version";
$::modifier_rss_link = 'http://nekyo.hp.infoseek.co.jp/';
$::modifier_rss_description = 'This is PyukiWiki.';

# Display Control
$::usefacemark = 1;   # 1:Enable :) -> Face Mark./0:Not
$::use_popup = 0;     # 1:PopUp New Window/0:Not at Link
$::last_modified = 2; # 0:Non/1:Upper/2:Lower
$::lastmod_prompt = 'Last-modified:';

# Formats
$::date_format = 'Y-m-d'; # replace &date; to this format.
$::time_format = 'H:i:s'; # replace &time; to this format,
