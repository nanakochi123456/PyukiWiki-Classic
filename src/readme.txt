PyukiWiki - ���R�Ƀy�[�W��ǉ��E�폜�E�ҏW�ł���Web�y�[�W�\�zCGI

-------------------------------------------------
�����
-------------------------------------------------
Copyright (C) 2004- by Nekyo
Nekyo <nekyo@yamaneko.club.ne.jp>
http://nekyo.hp.infoseek.co.jp/

-------------------------------------------------
���ŐV���
-------------------------------------------------
�ȉ���URL�ōŐV������肵�Ă��������B
http://nekyo.hp.infoseek.co.jp/

-------------------------------------------------
���͂��߂�
-------------------------------------------------
(1) index.cgi�̈�s�ڂ����Ȃ��̃T�[�o�ɍ��킹�ďC�����܂��B

    #!/usr/local/bin/perl

(2) pyukiwiki.ini.cgi �̕ϐ��̒l���C�����܂��B

(3)�u�t�@�C���ꗗ�v�ɂ���t�@�C�����T�[�o�ɓ]�����܂��B
    �]�����[�h��p�[�~�b�V������K�؂ɐݒ肵�܂��B

(4) �u���E�U�ŃT�[�o��� index.cgi��URL�ɃA�N�Z�X���܂��B

-------------------------------------------------
���t�@�C���ꗗ
-------------------------------------------------

��������

�ȉ��̃t�@�C���́A
Web�T�[�o�ɓ]������K�v�͂���܂���B

+-- README.txt          ��������i���̃t�@�C���j


��CGI�Q

�ȉ��̃t�@�C����CGI�����s�ł���f�B���N�g����FTP���܂��B

                       �]�����[�h �p�[�~�b�V����   ����
+-- index.cgi               TEXT  755 (rwxr-xr-x)  CGI�{��
+-- pyukiwiki.ini.cgi       TEXT  644 (rw-r--r--)  ��`�t�@�C��
+-- lib                           755 (rwxr-xr-x)  �g�p���W���[���Q
    +-- Algorithm                 755 (rwxr-xr-x)  �f�B���N�g��
    |   +-- Diff.pm         TEXT  644 (rw-r--r--)  �����p
    +-- Digest                    755 (rwxr-xr-x)  �f�B���N�g��
    |   +-- MD5.pm          TEXT  644 (rw-r--r--)  md5 �v�Z�p
    +-- Jcode                     755 (rwxr-wr-x)  �f�B���N�g�� 
    |   +-- Unicode               755 (rwxr-wr-x)  �f�B���N�g��
    |   |   +-- Contants.pm TEXT  644 (rw-r--r--)  Jcode.pm �Ŏg�p
    |   |   +-- NoXS.pm     TEXT  644 (rw-r--r--)  Jcode.pm �Ŏg�p
    |   +-- Contants.pm     TEXT  644 (rw-r--r--)  Jcode.pm �Ŏg�p
    |   +-- H2Z.pm          TEXT  644 (rw-r--r--)  Jcode.pm �Ŏg�p
    |   +-- Tr.pm           TEXT  644 (rw-r--r--)  Jcode.pm �Ŏg�p
    |   +-- Unicode.pm      TEXT  644 (rw-r--r--)  Jcode.pm �Ŏg�p
    +-- Yuki                      755 (rwxr-xr-x)  �f�B���N�g��
        +-- DiffText.pm     TEXT  644 (rw-r--r--)  �����p
        +-- RSS.pm          TEXT  644 (rw-r--r--)  RSS�p
        +-- YukiWikiDB.pm   TEXT  644 (rw-r--r--)  �t�@�C���x�[�X��DB�p

���Q�ƃt�@�C��

�ȉ��̃t�@�C���́A
pyukiwiki.ini.cgi ���̕ϐ� $::data_home�Ŏw�肷��f�B���N�g���ɓ]�����܂��B
�ڂ����� pyukiwiki.ini.cgi ���Q�Ƃ��ĉ������B

                       �]�����[�h �p�[�~�b�V����   ����
+-- resource.ja.txt         TEXT  644 (rw-r--r--)  ���\�[�X�t�@�C��
+-- conflict.ja.txt         TEXT  644 (rw-r--r--)  �X�V�̏Փˎ��̃e�L�X�g
+-- attach                        777 (rwxrwxrwx)  �Y�t�ۑ��p�f�B���N�g��
|   +-- index.html          TEXT  755 (rwxr-xr-x)  �ꗗ�\���h�~�p
+-- cache                         777 (rwxrwxrwx)  �ꎞ�f�B���N�g��
|   +-- index.html          TEXT  755 (rwxr-xr-x)  �ꗗ�\���h�~�p
+-- counter                       777 (rwxrwxrwx)  �J�E���^�l�ۑ��p�f�B���N�g��
|   +-- index.html          TEXT  755 (rwxr-xr-x)  �ꗗ�\���h�~�p
+-- diff                          777 (rwxrwxrwx)  �����ۑ��p�f�B���N�g��
|   +-- index.html          TEXT  755 (rwxr-xr-x)  �ꗗ�\���h�~�p
+-- image                         777 (rwxrwxrwx)  �摜�ۑ��p�f�B���N�g��
|   +-- index.html          TEXT  755 (rwxr-xr-x)  �ꗗ�\���h�~�p
+-- info                          777 (rwxrwxrwx)  ���ۑ��p�f�B���N�g��
|   +-- index.html          TEXT  755 (rwxr-xr-x)  �ꗗ�\���h�~�p
+-- plugin                        777 (rwxrwxrwx)  �v���O�C���p�f�B���N�g��
|   +-- index.html          TEXT  755 (rwxr-xr-x)  �ꗗ�\���h�~�p
+-- skin                          777 (rwxrwxrwx)  �X�L���p�f�B���N�g��
|   +-- pyukiwiki.skin.ja.cgi     644 (rw-r--r--)  �X�L���t�@�C��
|   +-- default.ja.css            644 (rw-r--r--)  �\���p css
|   +-- print.ja.css              644 (rw-r--r--)  ����p css
|   +-- blosxom.css               644 (rw-r--r--)  blosxom �p css
|   +-- instag.js                 644 (rw-r--r--)  �g���ҏW�p JavaScript
|   +-- index.html                644 (rw-r--r--)  �ꗗ�\���h�~�p
+-- wiki                          777 (rwxrwxrwx)  �y�[�W�f�[�^�ۑ��p�f�B���N�g��
|   +-- index.html          TEXT  755 (rwxr-xr-x)  �ꗗ�\���h�~�p
