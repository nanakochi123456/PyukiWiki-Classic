YukiWiki - ���R�Ƀy�[�W��ǉ��E�폜�E�ҏW�ł���Web�y�[�W�\�zCGI

-------------------------------------------------
�����
-------------------------------------------------

Copyright (C) 2000-2004 by Hiroshi Yuki.
����_ <hyuki@hyuki.com>
http://www.hyuki.com/
http://www.hyuki.com/yukiwiki/


-------------------------------------------------
���ŐV���
-------------------------------------------------

�ȉ���URL�ōŐV������肵�Ă��������B
http://www.hyuki.com/yukiwiki/


-------------------------------------------------
���͂��߂�
-------------------------------------------------

YukiWiki�i����E�B�L�j�͎Q���҂����R�Ƀy�[�W��ǉ��E�폜�E�ҏW�ł���Ƃ���
�s�v�c��Web�y�[�W�Q�����CGI�ł��B
Web�œ��삷��f���Ƃ�����Ǝ��Ă��܂����A
Web�f�����P�Ƀ��b�Z�[�W��ǉ����邾���Ȃ̂ɑ΂��āA
YukiWiki�́AWeb�y�[�W�S�̂����R�ɕύX���邱�Ƃ��ł��܂��B

YukiWiki�́AWard Cunningham��Wiki�̎d�l���Q�l�ɂ��ēƎ��ɍ���܂����B
����������CGI�͐��E���ɖ����ɂ���uWiki�N���[���v�ƌĂ΂�Ă��܂��B
YukiWiki��Wiki�N���[���̈��ł��B

YukiWiki��Perl�ŏ����ꂽCGI�X�N���v�g�Ƃ��Ď�������Ă��܂��̂ŁA
Perl�����삷��Web�T�[�o�Ȃ�Δ�r�I�e�Ղɐݒu�ł��܂��B

YukiWiki�̓t���[�\�t�g�ł��B
�����R�ɂ��g�����������B


-------------------------------------------------
�����C�Z���X
-------------------------------------------------

This program is free software; you can redistribute it and/or
modify it under the same terms as Perl itself.

-------------------------------------------------
���ݒu�菇
-------------------------------------------------

(1) wiki.cgi�̈�s�ڂ����Ȃ��̃T�[�o�ɍ��킹�ďC�����܂��B

    #!/usr/local/bin/perl

(2) wiki.cgi�̂͂��߂̕��ɂ���A�ϐ�$modifier_...�̒l���C�����܂�(�K�{)

    my $modifier_mail
        �Ǘ��҃��[���A�h���X

    my $modifier_url
        �Ǘ���Web�y�[�W

    my $modifier_name
        �Ǘ��Җ��O

    my $modifier_dbtype
        �f�[�^�x�[�X�̎��(�ȉ��̂����ꂩ)
            'YukiWikiDB'        (����)���͂��ꂽ�e�L�X�g�����̂܂܃t�@�C���Ƃ��ĕۑ�
            'dbmopen'           �T�[�o�ɂ���Ďg���Ȃ��ꍇ����
            'AnyDBM_File'       �T�[�o�ɂ���Ďg���Ȃ��ꍇ����

    my $modifier_sendmail
        YukiWiki�������ݎ��ɊǗ��҂Ƀ��[���𑗂邽�߂�
        sendmail�̃R�}���h���C��
            '/usr/sbin/sendmail -t -n'      ���
            ''                              ���[���𑗂�Ȃ�/����Ȃ��ꍇ

    my $modifier_dir_data
        CGI���ǂݏ�������f�[�^��u���f�B���N�g���B

    my $modifier_url_data
        CSS��摜�t�@�C����u���f�B���N�g���ɑΉ�����URL�B

    my $modifier_rss_title
        �^�C�g��(RSS�p)

    my $modifier_rss_link
        �ݒu����YukiWiki��URL(RSS�p)

    my $modifier_rss_description
        ������(RSS�p)


(3) �u�t�@�C���ꗗ�v�ɂ���t�@�C�����T�[�o�ɓ]�����܂��B
    �]�����[�h��p�[�~�b�V������K�؂ɐݒ肵�܂��B

(4) �u���E�U�ŃT�[�o���wiki.cgi��URL�ɃA�N�Z�X���܂��B

(5) FrontPage���\�����ꂽ��AAdminChangePassword�Ƃ��������N�����ǂ��āA
    �Ǘ��җp�̃p�X���[�h��ݒ肵�܂��B

(6) �ݒ肪�ς񂾂�Afrontpage.txt�t�@�C�������������A�ēx�]�����܂��B


-------------------------------------------------
���t�@�C���ꗗ
-------------------------------------------------

��������

�ȉ��̃t�@�C���́A
Web�T�[�o�ɓ]������K�v�͂���܂���B

+-- readme.txt          ��������i���̃t�@�C���j
+-- history.txt         �J���L�^


��CGI�Q

�ȉ��̃t�@�C����CGI�����s�ł���f�B���N�g����FTP���܂��B

                        �]�����[�h  �p�[�~�b�V����      ����
+-- wiki.cgi            TEXT        755 (rwxr-xr-x)     CGI�{��
+-- jcode.pl            TEXT        644 (rw-r--r--)     �����R�[�h�ϊ����C�u����
+-- Yuki                            755 (rwxr-xr-x)     �f�B���N�g��
|   +-- YukiWikiDB.pm   TEXT        644 (rw-r--r--)     �t�@�C���x�[�X��DB�p
|   +-- RSS.pm          TEXT        644 (rw-r--r--)     RSS�p
|   +-- DiffText.pm     TEXT        644 (rw-r--r--)     �����p
+-- Algorithm                       755 (rwxr-xr-x)     �f�B���N�g��
    +-- Diff.pm         TEXT        644 (rw-r--r--)     �����p


���Q�ƃt�@�C��

�ȉ��̃t�@�C���́A
wiki.cgi���̕ϐ�$modifier_dir_data�Ŏw�肷��f�B���N�g���ɓ]�����܂��B

                    �]�����[�h  �p�[�~�b�V����      ����
+-- touched.txt     TEXT        666 (rw-rw-rw-)     �ҏW���̍X�V�t�@�C��
+-- frontpage.txt   TEXT        644 (rw-r--r--)     FrontPage�̃e�L�X�g
+-- resource.txt    TEXT        644 (rw-r--r--)     ���\�[�X�t�@�C��
+-- conflict.txt    TEXT        644 (rw-r--r--)     �X�V�̏Փˎ��̃e�L�X�g
+-- format.txt      TEXT        644 (rw-r--r--)     ���`���[���̃e�L�X�g

�v���o�C�_�ɂ���ẮA
CGI��u���f�B���N�g���ɂ���t�@�C���́ACGI����A�N�Z�X�ł��Ȃ��ꍇ������܂��B

���̏ꍇ�ɂ́A�ϐ�$modifier_dir_data���g���āA
�uCGI���ǂݏ����ł���t�@�C����u���f�B���N�g���v���w�肵�Ă����A
���̃f�B���N�g���ɏ�L�̃t�@�C����]�����܂��B

���̂悤�Ȑ������Ȃ��ꍇ�ɂ́A
�ϐ�$modifier_dir_data�ł�wiki.cgi��]�������f�B���N�g�����w�肵�A
�����f�B���N�g���ɏ�L�t�@�C����]�����܂��B


���X�^�C���V�[�g�Ɖ摜�t�@�C��

�ȉ��̃t�@�C���́A
wiki.cgi���̕ϐ�$modifier_url_data�Ŏw�肷��URL�ɑΉ������f�B���N�g���ɓ]�����܂��B

+-- wiki.css        TEXT        644 (rw-r--r--)     �X�^�C���V�[�g
+-- icon40x40.gif   BINARY      644 (rw-r--r--)     �A�C�R��(��)
+-- icon80x80.gif   BINARY      644 (rw-r--r--)     �A�C�R��(��)

�v���o�C�_�ɂ���ẮA
CGI��u���f�B���N�g���ɃX�^�C���V�[�g��摜�t�@�C����u���Ă�
Web�T�[�o����Q�Ƃł��Ȃ��ꍇ������܂��B

���̏ꍇ�ɂ́A
Web�T�[�o����Q�Ƃł���ꏊ��URL��$modifier_url_data���g���Ďw�肵�A
���̃f�B���N�g���ɏ�L�t�@�C����]�����܂��B

���̂悤�Ȑ������Ȃ��ꍇ�ɂ́A
�ϐ�$modifier_url_data�ł�wiki.cgi��]�������f�B���N�g�����w�肵�A
�����f�B���N�g���ɏ�L�t�@�C����]�����܂��B


-------------------------------------------------
���f�[�^�̃o�b�N�A�b�v���@
-------------------------------------------------

YukiWiki�ō\�z���ꂽWeb�y�[�W�̃R���e���c�́A
wiki.cgi�����o���f�[�^�x�[�X���ɕێ�����܂��B

���ꂽ�f�[�^�͂��ׂ�
�ϐ�$modifier_dir_data�Ŏw�肵���f�B���N�g���ȉ��ɍ���܂��̂ŁA
���̃f�B���N�g���̉������ׂăo�b�N�A�b�v���Ă����΂悢�ł��傤�B

�ϐ�$modifier_dbtype��'YukiWikiDB'�ɂ����ꍇ�ɂ́A
wiki, info, diff�Ƃ���3�̃f�B���N�g��������A
���̉��Ƀy�[�W���ƂɃt�@�C��������܂��B
�o�b�N�A�b�v���ꂪ�Ȃ��悤�ɒ��ӂ��Ă��������B


-------------------------------------------------
����{�I�Ȏg����
-------------------------------------------------

���V�����y�[�W�̍���

1.�u�V�K�쐬�v�Ƃ��������N�����ǂ�܂��B
2. �V�����y�[�W�̖��O����͂��܂��B
3. �y�[�W�̓��e����͂��܂��B

���e�L�X�g���`�̃��[��

format.txt���Q�Ƃ��Ă��������B

���n�C�p�[�����N

LinkToSomePage��FrontPage�̂悤�ɁA
�p�P��̍ŏ��̈ꕶ����啶���ɂ������̂�
��ȏ�A���������̂�YukiWiki�̃y�[�W���ƂȂ�A
���ꂪ���͒��Ɋ܂܂��ƃ����N�ɂȂ�܂��B

��d�̑傩����[[ ]]�ł���������������A
YukiWiki�̃y�[�W���ɂȂ�܂��B
�傩�����̒��ɂ̓X�y�[�X���܂߂Ă͂����܂���B
���{����g���܂��B

http://www.hyuki.com/
�̂悤��URL�͎����I�Ƀ����N�ɂȂ�܂��B


-------------------------------------------------
���ӎ�
-------------------------------------------------

�{�Ƃ�Wiki�������Ward Cunningham�Ɋ��ӂ��܂��B
http://c2.com/cgi/wiki

YukiWiki���y����Ŏg���Ă�������l�b�g��̕��X�Ɋ��ӂ��܂��B

������Wiki�N���[���̍�҂��񂽂��ƁA
YukiWiki�̃��[�U���񂽂��ɐ[�����ӂ��܂��B

��PukiWiki (PHP)
http://pukiwiki.org/
����InterWiki, �ꌾ�R�����g�@�\�ȂǂɊ��ӂ��܂��B

��Tiki (Ruby)
http://www.todo.org/cgi-bin/jp/tiki.cgi

��RWiki (Ruby)
http://www.jin.gr.jp/~nahi/RWiki/

��KbWiki (Perl + HTML::Template)
http://www.hippo2000.info/cgi-bin/KbWiki/KbWiki.pl

���u�Ɉ��v�����wiki (Perl)
http://hpcgi1.nifty.com/dune/gwiki.pl
���ɁAYukiWikiDB�Ɋ��ӂ��܂��B

���˖{�q�������WalWiki (Perl)
http://digit.que.ne.jp/work/
���ɁA�e�[�u���@�\�Ɋ��ӂ��܂��B

YukiWiki�̃��S���f�U�C�����Ă������������{��ނ���
http://city.hokkai.or.jp/~reina/
�Ɋ��ӂ��܂��B


-------------------------------------------------
���֘A�����N
-------------------------------------------------

������_�̃y�[�W
http://www.hyuki.com/

��YukiWiki�z�[���y�[�W
http://www.hyuki.com/yukiwiki/

���{�Ƃ�Wiki
http://c2.com/cgi/wiki?WikiWikiWeb

�����{����wiki�N���[�����X�g
http://www1.neweb.ne.jp/wa/yamdas/column/technique/clonelist.html

�����{����wiki�N���[�����X�g2
http://www1.neweb.ne.jp/wa/yamdas/column/technique/clonelist2.html
