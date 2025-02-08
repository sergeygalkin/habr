# Mikrotik config

system logging

```
/system logging action set 3 remote=x.x.x.x remote-port=5514 src-address=x.x.x.x syslog-facility=local0
/system logging set 0 action=remote prefix=:Info topics=info,!firewall
/system logging set 1 action=remote disabled=yes prefix=:Error
/system logging set 2 action=remote prefix=:Warning topics=warning,!firewall
/system logging set 3 action=remote prefix=:Critical
/system logging add action=remote disabled=yes prefix=mikrotik-critical topics=critical
/system logging add action=remote disabled=yes prefix=mikrotik topics=!debug,!packet,!dns
/system logging add action=remote prefix=:Firewall topics=firewall
/system logging add action=remote prefix=:Account topics=account
/system logging add action=remote prefix=:Caps topics=caps
/system logging add action=remote prefix=:Wireles topics=wireless
/system logging add action=remote disabled=yes prefix=mikrotik-critical topics=critical
/system logging add action=remote disabled=yes prefix=mikrotik topics=!debug,!packet,!dns
/system logging add action=remote prefix=:Firewall topics=firewall
/system logging add action=remote prefix=:Account topics=account
/system logging add action=remote prefix=:Caps topics=caps
```


firewall
```
/ip firewall filter add action=passthrough chain=forward comment="all new connections" connection-state=new log=yes log-prefix=new-connection
/ip firewall filter add action=drop chain=forward comment="defconf: drop invalid" connection-state=invalid log=yes
/ip firewall filter add action=drop chain=input comment="drop all" in-interface=ether1-wan log=yes log-prefix=dropped
```
