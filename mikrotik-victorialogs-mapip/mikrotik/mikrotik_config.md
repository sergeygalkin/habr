# Mikrotik config

system logging

```
/system logging action set 3 remote=x.x.x.x remote-port=5514 src-address=x.x.x.x syslog-facility=local0
/system logging add action=remote prefix=:Firewall topics=firewall
```


firewall
```
/ip firewall filter add action=passthrough chain=forward comment="all new connections" connection-state=new log=yes log-prefix=new-connection
```
