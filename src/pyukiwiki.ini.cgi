##############################
# pyukiwiki.ini.cgi
#
# Copyright (C) 2004-2006 by Nekyo.
# http://nekyo.hp.infoseek.co.jp/
#
# 1TAB=4Spaces
##############################
use strict;

# 言語
$::lang = "ja";       # ja:日本語/en:英語(参考)
$::kanjicode = "euc"; # euc:EUC-JP/utf8:UTF-8

# データ格納ディレクトリ
$::data_home   = '.'; # ページデータ等のディレクトリ
$::data_dir    = "$::data_home/wiki";		# ページデータ保存用
$::diff_dir    = "$::data_home/diff";		# 差分保存用
$::cache_dir   = "$::data_home/cache";		# 一時用
$::upload_dir  = "$::data_home/attach";		# 添付用
$::counter_dir = "$::data_home/counter";	# カウンタ用
$::plugin_dir  = "$::data_home/plugin";		# プラグイン用
$::skin_dir    = "$::data_home/skin";		# スキン用
$::image_dir   = "$::data_home/image";		# 画像用
$::info_dir    = "$::data_home/info";		# 情報用
$::res_dir     = "$::data_home/resource";	# リソース
$::js_dir      = "$::skin_dir/js";			# JavaScript用物理パス
# このディレクトリに プラグイン名.js ファイルを入れておくと、
# そのプラグインが使用されているページで自動的に読み込まれる。
$::js_url      = $::js_dir;					# JavaScript用論理パス(相対パスなら同じ?)
$::css_dir     = "$::skin_dir/css";			# CSS用物理パス
# このディレクトリに プラグイン名.css ファイルを入れておくと、
# そのプラグインが使用されているページで自動的に読み込まれる。
$::css_url     = $::css_dir;				# CSS用論理パス

# スキンファイル(省略すれば pyukiwiki.skin.cgi が使われる。
#$::skin_file = "pyukiwiki.skin.cgi";

# 修正者情報
$::modifier = 'Your name';					# 修正者名
$::modifierlink = 'http://your.site.url/'; # 修正者URI
$::modifier_mail = '';					# 修正者メールアドレス

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

# デフォルトの凍結パスワード(ここを変更して下さい)
$::adminpass = crypt("pass", "AA");

# RSS情報
$::modifier_rss_title       = "PyukiWiki $::version";
$::modifier_rss_link        = $::modifierlink;
$::modifier_rss_description = 'This is PyukiWiki.';

# Proxy設定(必要ならば)
#$::proxy_host = 'xxx.xxx.xxx.xxx';
#$::proxy_port = 8080;

# 表示設定
$::usefacemark    = 1; # フェースマークを 1:使う/0:使わない。
$::use_popup      = 0; # リンク先を 1:ポップアップ/0:ページ切替
$::last_modified  = 2; # 最終更新日 0:非表示/1:上に表示/2:下に表示
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

# Skin の gzip パスを設定すると圧縮が有効になる。
#$::gzip_path = '/bin/gzip -1';
$::gzip_path = '';

##
# 拡張JS設定 この設定があると、指定されたプラグインがあるページで、
# 自動的に、ヘッダー部が拡張される。
#$::extend_js{プラグイン}{'js'} = "(METAタグで記述するJSのURL)"; (省略化)
#$::extend_js{プラグイン}{'charset'} = 'UTF-8';  JSのキャラセット (省略化)
#$::extend_js{プラグイン}{'onload'} = 'オンロード関数'; (省略化)
#$::extend_js{プラグイン}{'onunload'} = 'オンアンロード関数'; (省略化)

##
# 入力拒否文字列
# aaa bbb を拒否したい場合は以下の様に改行して記述。
#$::disablewords = "aaa
#bbb";

##
# 接続拒否アドレス
# 192.168.100.* からの接続を拒否したい場合は以下の様に記述。
#$::disableaddr = "192.168.100.";

1;
