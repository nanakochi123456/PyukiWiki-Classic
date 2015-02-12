#!/bin/sh

cd pyuki

# 空のディレクトリが出来ていなければ作成~
if test ! -d counter
then
  mkdir counter
fi
if test ! -d diff
then
  mkdir diff
fi
if test ! -d diff
then
  mkdir info
fi

chmod 755 wiki.cgi
chmod 644 jcode.pl
chmod 755 Yuki
chmod 644 Yuki/YukiWikiDB.pm
chmod 644 Yuki/RSS.pm
chmod 644 Yuki/DiffText.pm
chmod 755 Algorithm
chmod 644 Algorithm/Diff.pm
chmod 755 plugin
chmod 644 plugin/*.inc.pl
chmod 666 touched.txt
chmod 644 resource.ja.txt
chmod 644 resource.cn.txt
chmod 644 resource.en.txt
chmod 644 conflict.txt
chmod 644 format.txt
chmod 766 wiki
chmod 666 wiki/*
chmod 666 counter
chmod 766 diff
chmod 766 info
chmod 644 default.ja.css
chmod 644 print.ja.css
chmod 644 pyukiwiki.png
chmod 755 face
chmod 644 face/*.png
chmod 755 image
chmod 644 image/*.png

cd ..
