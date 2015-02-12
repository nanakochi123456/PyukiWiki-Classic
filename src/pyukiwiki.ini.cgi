##############################
# pyukiwiki.ini.cgi
#
# Copyright (C) 2004 by Nekyo.
# http://nekyo.hp.infoseek.co.jp/
#
# 1TAB=4Spaces
##############################

# 言語
$::lang = "ja";       # ja:日本語/en:英語(参考)
$::kanjicode = "euc"; # euc:EUC-JP/utf8:UTF-8

##
# データ格納ディレクトリ
#
# 通常版設定
$::data_home = '.';
$::uri_home = $::data_home;
#
# nifty 設定
# $::data_home = '/cgi-bin';
# $::uri_home  = 'http://homepage?.nifty.com';

$::data_dir    = "$::data_home/wiki";		# ページデータ保存用
$::diff_dir    = "$::data_home/diff";		# 差分保存用
$::cache_dir   = "$::data_home/cache";		# 一時用
$::upload_dir  = "$::data_home/attach";		# 添付用
$::counter_dir = "$::data_home/counter";	# カウンタ用
$::plugin_dir  = "$::data_home/plugin";		# プラグイン用
$::skin_dir    = "$::data_home/skin";		# スキン用
$::info_dir    = "$::data_home/info";		# 情報用
$::res_dir     = "$::data_home/resource";
$::js_dir      = "$::skin_dir/js";
$::css_dir     = "$::skin_dir/css";

$::skin_uri    = "$::uri_home/skin";
$::image_dir   = "$::uri_home/image";		# 画像用
$::js_uri      = "$::skin_uri/js";
$::css_uri     = "$::skin_uri/css";

# スキンファイル(省略で pyukiwiki.skin.cgi が仕様される。)
#$::skin_file = 'pyukiwiki.skin.cgi';

# プロキシ設定(あれば)
#$proxy_host = '';
#$proxy_port = 8080;

# 修正者情報
$::modifier = 'You Name';				# 修正者名
$::modifierlink = 'Your Site Address';	# 修正者URI
$::modifier_mail = '';					# 修正者メールアドレス

# デフォルトページ名
$::script        = 'index.cgi';
$::FrontPage     = 'FrontPage';
$::CreatePage    = 'CreatePage';
$::IndexPage     = 'IndexPage';
$::MenuBar       = 'MenuBar';
$::Header        = ':Header';
$::Footer        = ':Footer';
$::rule_page     = "整形ルール";

# 管理者パスワードの設定 pass 側を修正 AA はそのまま。
$::adminpass = crypt("pass", "AA");

# RSS情報
$::modifier_rss_title = "PyukiWiki $::version";
$::modifier_rss_description = 'This is PyukiWiki.';
#$::modifier_rss_link = 'http://nekyo.hp.infoseek.co.jp/';	# 設定されているとrssのリンクが全てこれになる。

# 表示設定
$::use_popup = 0;     # リンク先を 1:ポップアップ/0:ページ切替
$::last_modified = 2; # 最終更新日 0:非表示/1:上に表示/2:下に表示
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

$::_symbol_anchor = '&dagger;';
$::maxrecent = 50;

# 一覧・更新一覧に含めないページ名(正規表現で)
$::non_list = '^\:';

# Skin の gzip パスを設定すると圧縮が有効になる。
#$::gzip_path = '/bin/gzip -1';
$::gzip_path = '';

# これが指定されているとRSSのリンクがこれになる。
#$::rssurl = "http://nekyo.hp.infoseek.co.jp/rss.shtml";

##
# フィルター関連
#$::filter_flg = 1;	# 1でフィルター機能を有効にする。
#$::chk_uri_count = 20;	# 1つの投稿ホームページアドレスが20個以上あるとスパムとみなす。
#$::chk_jp_only = 1;	# 日本語が一時も入っていないとスパムとみなす。
#$::deny_log = "$::cache_dir/deny.log";	# ログファイル。指定されているとログを取る。無くても問題ない。

# 禁止文字列を指定。複数文字は改行で連結
#$::disablewords = "poker";

1;
