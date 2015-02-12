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
# 言語
$::lang = "ja";       # ja:日本語/en:英語(参考)
$::kanjicode = "euc"; # euc:EUC-JP/utf8:UTF-8

# データ格納ディレクトリ
$::data_home   = '.'; # ページデータ等のディレクトリ
$::data_dir    = "$::data_home/wiki";     # ページデータ保存用
$::diff_dir    = "$::data_home/diff";     # 差分保存用
$::cache_dir   = "$::data_home/cache";    # 一時用
$::upload_dir  = "$::data_home/attach";   # 添付用
$::counter_dir = "$::data_home/counter";  # カウンタ用
$::plugin_dir  = "$::data_home/plugin";   # プラグイン用
$::skin_dir    = "$::data_home/skin";     # スキン用
$::image_dir   = "$::data_home/image";    # 画像用
$::info_dir    = "$::data_home/info";     # 情報用
$::res_dir     = "$::data_home/resource"; # リソース

# スキンファイル
#$::skin_file = 'pyukiwiki.skin.cgi';

# プロキシ設定
#$proxy_host = '';
#$proxy_port = 8080;

# 修正者情報(修正して下さい)
$::modifier      = 'YourName';          # 修正者名
$::modifierlink  = 'http://localhost/'; # 修正者URI
$::modifier_mail = '';                  # 修正者メールアドレス

# デフォルトページ名
$::script        = 'index.cgi';
$::FrontPage     = 'FrontPage';
$::RecentChanges = 'RecentChanges';
$::CreatePage    = 'CreatePage';
$::IndexPage     = 'IndexPage';
$::MenuBar       = 'MenuBar';
$::Header        = ':Header';
$::Footer        = ':Footer';
$::rule_page     = "整形ルール";

# 凍結時のパスワード(変更して下さい)
$::adminpass = crypt("pass", "AA");

# RSS情報(変更して下さい)
$::modifier_rss_title       = "PyukiWiki $::version";
$::modifier_rss_link        = 'http://localhost/';
$::modifier_rss_description = 'This is PyukiWiki.';

# 表示設定
$::usefacemark = 1;                   # フェースマーク 1:使用/0:未使用
$::use_popup = 0;                     # リンク先 1:ポップアップ/0:ページ切替
$::last_modified = 2;                 # 最終更新日 0:非表示/1:上に表示/2:下に表示
$::lastmod_prompt = 'Last-modified:'; # 最終更新日のプロンプト

$::enable_convtime = 1; # コンバートタイム 1:表示/0:非表示;

# 日時フォーマット
$::date_format = 'Y-m-d'; # replace &date; to this format.
$::time_format = 'H:i:s'; # replace &time; to this format,

# ページ編集
$::cols = 80;       # テキストエリアのカラム数
$::rows = 25;       # テキストエリアの行数
$::extend_edit = 1; # 拡張機能(JavaScript) 1:使用/0:未使用

# 添付
$::file_uploads = 2;       # 添付を 0:使わない/1:使う/2:認証付きで使う
$::max_filesize = 1000000; # アップロードファイルの最大数

#
$::_symbol_anchor = '&dagger;';
$::maxrecent = 50;

# 一覧・更新一覧に含めないページ名(正規表現で)
$::non_list = '^\:';
# 以下は md5('pass') の出力結果です
#$adminpass = &md5('pass');

# Skin の gzip パスを設定すると圧縮が有効になる。
#$::gzip_path = '/bin/gzip -1';
$::gzip_path = '';

1;
