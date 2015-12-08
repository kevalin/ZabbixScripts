#! /usr/bin/python
# -*- coding: utf-8 -*-
import json

f = open("/etc/zabbix/scripts/need_check_ip.txt")
dictIp = {}
infos = []

for line in f:
    tempObj = {}
    tempObj["{#IP}"] = line.replace('\n', '').replace(' ', '')
    infos.append(tempObj)

dictIp["data"] = infos
f.close()
print json.dumps(dictIp, sort_keys=True, indent=4)
