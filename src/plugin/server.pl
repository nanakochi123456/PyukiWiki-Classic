# Plugin for YukiWiki & PyukiWiki
# Based by beacon.inc.php by Nobuo Yamanaka
# Presented by Nekyo

use strict;
package server;

sub disp {
	my ($s) = @_;

	return ($s ? $s : "-");
}

sub plugin_block {
	return &plugin_inline;
}

sub plugin_inline
{
	my $useragent = $::ENV{'HTTP_USER_AGENT'};
	my $body =<<"EOD";
<dl>
<dt>Server Name</dt>
<dd>@{[ $::ENV{'SERVER_NAME'} ]}</dd>
<dt>Server Software</dt>
<dd>@{[ $::ENV{'SERVER_SOFTWARE'} ]}</dd>
<dt>Server Admin</dt>
<dd><a href="mailto:@{[ $::ENV{'SERVER_ADMIN'} ]}">@{[
	$::ENV{'SERVER_ADMIN'}
]}</a></dd>
<dt>User Agent</dt>
<dd>@{[ $useragent ]}</dd>
EOD
	if ($useragent =~ /^J-PHONE\//) {
# Color:色数 / Display:画面サイズ / GeoCode:位置情報 / Java:Vアプリ対応機種
# MsName:端末機種名 / Region:利用地域(国内・外) / Smaf:Smaf種別
# Sound:和音種別 / UID:ユーザID / Copyright:保存・送出・転送可否指定
		$body .=<<"EOD";
<dt>Color</dt>
<dd>@{[ &disp($::ENV{'HTTP_X_JPHONE_COLOR'})     ]}</dd>
<dt>Display</dt>
<dd>@{[ &disp($::ENV{'HTTP_X_JPHONE_DISPLAY'})   ]}</dd>
<dt>GeoCode</dt>
<dd>@{[ &disp($::ENV{'HTTP_X_JPHONE_GEOCODE'})   ]}</dd>
<dt>Java</dt>
<dd>@{[ &disp($::ENV{'HTTP_X_JPHONE_JAVA'})      ]}</dd>
<dt>MSName</dt>
<dd>@{[ &disp($::ENV{'HTTP_X_JPHONE_MSNAME'})    ]}</dd>
<dt>Region</dt>
<dd>@{[ &disp($::ENV{'HTTP_X_JPHONE_REGION'})    ]}</dd>
<dt>Smaf</dt>
<dd>@{[ &disp($::ENV{'HTTP_X_JPHONE_SMAF'})      ]}</dd>
<dt>Sound</dt>
<dd>@{[ &disp($::ENV{'HTTP_X_JPHONE_SOUND'})     ]}</dd>
<dt>UID</dt>
<dd>@{[ &disp($::ENV{'HTTP_X_JPHONE_UID'})       ]}</dd>
<dt>Copyright</dt>
<dd>@{[ &disp($::ENV{'HTTP_X_JPHONE_COPYRIGHT'}) ]}</dd>
EOD
	} elsif ($useragent =~ /UP\.Browser\//) {
#	} else {
# HTTP_X_UP_DEVCAP_IMMED_ALERT:does(1) or does not(0) support immediate alerts.
# HTTP_X_UP_DEVCAP_MAX_PDU:maximum packet size supported by device.
# HTTP_X_UP_DEVCAP_GUI:device is(1) or is not(0) using a GUI browser.
# HTTP_X_UP_DEVCAP_SCREENPIXELS / HTTP_X_UP_DEVCAP_SCREENCHARS / HTTP_X_UP_DEVCAP_SCREENDEPTH
# HTTP_X_UP_DEVCAP_MSIZE:pixels of the character,"M"
# HTTP_X_UP_DEVCAP_NUMSOFTKEYS / HTTP_X_UP_DEVCAP_SOFTKEYSIZE
# HTTP_X_UP_DEVCAP_ISCOLOR
# HTTP_X_UP_FAX_ACCEPTS / HTTP_X_UP_FAX_ENCODINGS / HTTP_X_UP_FAX_LIMIT
# HTTP_X_UP_SUBNO
# HTTP_X_UP_UPLINK
# HTTP_X_UP_DEVCAP_SMARTDIALING ??
#<dt>Accept Language</dt>
#<dd>@{[ &disp($::ENV{'HTTP_ACCEPT_LANGUAGE'}) ]}</dd>
#<dt>Cookie</dt>
#<dd>@{[ &disp($::ENV{'HTTP_COOKIE'})          ]}</dd>
#<dt>Refer</dt>
#<dd>@{[ &disp($::ENV{'HTTP_REFERER'})         ]}</dd>

		$body .=<<"EOD";
<dt>Immidiate Alerts</dt>
<dd>@{[ &disp($::ENV{'HTTP_X_UP_DEVCAP_IMMED_ALERT'})  ]}</dd>
<dt>Max PDU</dt>
<dd>@{[ &disp($::ENV{'HTTP_X_UP_DEVCAP_MAX_PDU'})      ]}</dd>
<dt>GUI</dt>
<dd>@{[ &disp($::ENV{'HTTP_X_UP_DEVCAP_GUI'})          ]}</dd>
<dt>Screen Pixels</dt>
<dd>@{[ &disp($::ENV{'HTTP_X_UP_DEVCAP_SCREENPIXELS'}) ]}</dd>
<dt>Screen Chars</dt>
<dd>@{[ &disp($::ENV{'HTTP_X_UP_DEVCAP_SCREENCHARS'})  ]}</dd>
<dt>Screen Depth</dt>
<dd>@{[ &disp($::ENV{'HTTP_X_UP_DEVCAP_SCREENDEPTH'})  ]}</dd>
<dt>M Size</dt>
<dd>@{[ &disp($::ENV{'HTTP_X_UP_DEVCAP_MSIZE'})        ]}</dd>
<dt>Num Softkeys</dt>
<dd>@{[ &disp($::ENV{'HTTP_X_UP_DEVCAP_NUMSOFTKEYS'})  ]}</dd>
<dt>Softkey Size</dt>
<dd>@{[ &disp($::ENV{'HTTP_X_UP_DEVCAP_SOFTKEYSIZE'})  ]}</dd>
<dt>Is Color</dt>
<dd>@{[ &disp($::ENV{'HTTP_X_UP_DEVCAP_ISCOLOR'})      ]}</dd>
<dt>Fax Accepts</dt>
<dd>@{[ &disp($::ENV{'HTTP_X_UP_FAX_ACCEPTS'})         ]}</dd>
<dt>Fax Encodings</dt>
<dd>@{[ &disp($::ENV{'HTTP_X_UP_FAX_ENCODINGS'})       ]}</dd>
<dt>Fax Limit</dt>
<dd>@{[ &disp($::ENV{'HTTP_X_UP_FAX_LIMIT'})           ]}</dd>
<dt>Subno</dt>
<dd>@{[ &disp($::ENV{'HTTP_X_UP_SUBNO'})               ]}</dd>
<dt>Uplink</dt>
<dd>@{[ &disp($::ENV{'HTTP_X_UP_UPLINK'})              ]}</dd>
EOD
	}
	return $body . "</dl>\n";
}

sub plugin_usage {
	return {
		name => 'server',
		version => '1.0',
		author => 'Nekyo <nekyo@yamaneko.club.ne.jp>',
		syntax => '#server',
		description => 'Show Server Info.',
		example => '#server',
	};
}

1;
