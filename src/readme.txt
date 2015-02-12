PyukiWiki - 自由にページを追加・削除・編集できるWebページ構築CGI

-------------------------------------------------
■作者
-------------------------------------------------
Copyright (C) 2004- by Nekyo
Nekyo <nekyo@yamaneko.club.ne.jp>
http://nekyo.hp.infoseek.co.jp/

-------------------------------------------------
■最新情報
-------------------------------------------------
以下のURLで最新情報を入手してください。
http://nekyo.hp.infoseek.co.jp/

-------------------------------------------------
■はじめに
-------------------------------------------------
(1) index.cgiの一行目をあなたのサーバに合わせて修正します。

    #!/usr/local/bin/perl

(2) pyukiwiki.ini.cgi の変数の値を修正します。

(3)「ファイル一覧」にあるファイルをサーバに転送します。
    転送モードやパーミッションを適切に設定します。

(4) ブラウザでサーバ上の index.cgiのURLにアクセスします。

-------------------------------------------------
■ファイル一覧
-------------------------------------------------

●説明文

以下のファイルは、
Webサーバに転送する必要はありません。

+-- README.txt          解説文書（このファイル）


●CGI群

以下のファイルはCGIが実行できるディレクトリにFTPします。

                       転送モード パーミッション   説明
+-- index.cgi               TEXT  755 (rwxr-xr-x)  CGI本体
+-- pyukiwiki.ini.cgi       TEXT  644 (rw-r--r--)  定義ファイル
+-- lib                           755 (rwxr-xr-x)  使用モジュール群
    +-- Algorithm                 755 (rwxr-xr-x)  ディレクトリ
    |   +-- Diff.pm         TEXT  644 (rw-r--r--)  差分用
    +-- Digest                    755 (rwxr-xr-x)  ディレクトリ
    |   +-- MD5.pm          TEXT  644 (rw-r--r--)  md5 計算用
    +-- Jcode                     755 (rwxr-wr-x)  ディレクトリ 
    |   +-- Unicode               755 (rwxr-wr-x)  ディレクトリ
    |   |   +-- Contants.pm TEXT  644 (rw-r--r--)  Jcode.pm で使用
    |   |   +-- NoXS.pm     TEXT  644 (rw-r--r--)  Jcode.pm で使用
    |   +-- Contants.pm     TEXT  644 (rw-r--r--)  Jcode.pm で使用
    |   +-- H2Z.pm          TEXT  644 (rw-r--r--)  Jcode.pm で使用
    |   +-- Tr.pm           TEXT  644 (rw-r--r--)  Jcode.pm で使用
    |   +-- Unicode.pm      TEXT  644 (rw-r--r--)  Jcode.pm で使用
    +-- Yuki                      755 (rwxr-xr-x)  ディレクトリ
        +-- DiffText.pm     TEXT  644 (rw-r--r--)  差分用
        +-- RSS.pm          TEXT  644 (rw-r--r--)  RSS用
        +-- YukiWikiDB.pm   TEXT  644 (rw-r--r--)  ファイルベースのDB用

●参照ファイル

以下のファイルは、
pyukiwiki.ini.cgi 内の変数 $::data_homeで指定するディレクトリに転送します。
詳しくは pyukiwiki.ini.cgi を参照して下さい。

                       転送モード パーミッション   説明
+-- resource.ja.txt         TEXT  644 (rw-r--r--)  リソースファイル
+-- conflict.ja.txt         TEXT  644 (rw-r--r--)  更新の衝突時のテキスト
+-- attach                        777 (rwxrwxrwx)  添付保存用ディレクトリ
|   +-- index.html          TEXT  755 (rwxr-xr-x)  一覧表示防止用
+-- cache                         777 (rwxrwxrwx)  一時ディレクトリ
|   +-- index.html          TEXT  755 (rwxr-xr-x)  一覧表示防止用
+-- counter                       777 (rwxrwxrwx)  カウンタ値保存用ディレクトリ
|   +-- index.html          TEXT  755 (rwxr-xr-x)  一覧表示防止用
+-- diff                          777 (rwxrwxrwx)  差分保存用ディレクトリ
|   +-- index.html          TEXT  755 (rwxr-xr-x)  一覧表示防止用
+-- image                         777 (rwxrwxrwx)  画像保存用ディレクトリ
|   +-- index.html          TEXT  755 (rwxr-xr-x)  一覧表示防止用
+-- info                          777 (rwxrwxrwx)  情報保存用ディレクトリ
|   +-- index.html          TEXT  755 (rwxr-xr-x)  一覧表示防止用
+-- plugin                        777 (rwxrwxrwx)  プラグイン用ディレクトリ
|   +-- index.html          TEXT  755 (rwxr-xr-x)  一覧表示防止用
+-- skin                          777 (rwxrwxrwx)  スキン用ディレクトリ
|   +-- pyukiwiki.skin.ja.cgi     644 (rw-r--r--)  スキンファイル
|   +-- default.ja.css            644 (rw-r--r--)  表示用 css
|   +-- print.ja.css              644 (rw-r--r--)  印刷用 css
|   +-- blosxom.css               644 (rw-r--r--)  blosxom 用 css
|   +-- instag.js                 644 (rw-r--r--)  拡張編集用 JavaScript
|   +-- index.html                644 (rw-r--r--)  一覧表示防止用
+-- wiki                          777 (rwxrwxrwx)  ページデータ保存用ディレクトリ
|   +-- index.html          TEXT  755 (rwxr-xr-x)  一覧表示防止用
