##
# バグレポートを一覧表示する。
# :書式|
#  #bugtrack_list([ページ名])
# -ページ名はバグレポートとして作成されるページの親階層のページ名を指定。省略時は設置ページとなる。~
# bugtrackプラグインの機能を使用しているため、bugtrackプラグイン必須。

require $::plugin_dir . '/bugtrack.inc.pl';
1;
