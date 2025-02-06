# Mikrotik config

```
[admin@MikroTik-domru] /system/logging> export
# 2025-02-06 10:45:04 by RouterOS 7.17.1
# software id = WVAU-U7QD
#
# model = C53UiG+5HPaxD2HPaxD
# serial number = xxxxxxxxxxxxx
/system logging action
set 3 remote=x.x.x.x remote-port=5514 src-address=x.x.x.y syslog-facility=local0
/system logging
set 0 action=remote prefix=:Info topics=info,!firewall
set 1 action=remote disabled=yes prefix=:Error
set 2 action=remote prefix=:Warning topics=warning,!firewall
set 3 action=remote prefix=:Critical
add action=remote disabled=yes prefix=mikrotik-critical topics=critical
add action=remote disabled=yes prefix=mikrotik topics=!debug,!packet,!dns
add action=remote prefix=:Firewall topics=firewall
add action=remote prefix=:Account topics=account
add action=remote prefix=:Caps topics=caps
add action=remote prefix=:Wireless topics=wireless
```
