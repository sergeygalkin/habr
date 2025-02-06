# Loki queries

![Loki dashboard](loki_dashboard.png)

## Visualization Logs: "Incoming connections"

Request
```
{host="MikroTik-domru"} |= "dnat" | pattern `<_> src-mac <_>, proto <_>, <src_ip>:<src_port>-><dst_ip>:<dst_port>, <_>`
| line_format "{{.src_ip}}: Country:{{.geoip_country_name}}, City:{{.geoip_city_name}} "
```

## Visualization Pie Chart: "Incoming connections by country"

Request
```
count by(geoip_country_name) (rate({host="MikroTik-domru"} |= `dnat` [$__auto] ) )
```

