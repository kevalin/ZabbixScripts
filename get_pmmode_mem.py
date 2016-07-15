#! /usr/bin/python
# -*- coding: utf-8 -*-
import os, sys, commands, json

def getMem(ptype, pname):
    if ptype == "vsz":
        if pname == "pm" or pname == "proxy":
            cmd = "ps aux | grep -w " + pname + ".js | grep -v grep | awk '{print $5}'"
        else:
            cmd = "ps aux | grep -v 'python' | awk '$14 == " + '"' + pname + '"' + " {print $5}'"
    elif ptype == "rss":
        if pname == "pm" or pname == "proxy":
            cmd = "ps aux | grep -w " + pname + ".js | grep -v grep | awk '{print $6}'"
        else:
            cmd = "ps aux | grep -v 'python' | awk '$14 == " + '"' + pname + '"' + " {print $6}'"

    (status, output) = commands.getstatusoutput(cmd)

    if status == 0:
        return output
    else:
        return 0

def discovery():
    procList = {}
    procList["data"] = []

    vhosts = "ps aux | grep -w 'vhosts.js' | grep -v grep | awk '{print $14}'"
    (status, output) = commands.getstatusoutput(vhosts)
    
    if status == 0:
        for i in output.split("\n"):
            site = {}
            site["{#SITENAME}"] = i
            procList["data"].append(site)
    
    pm = {}
    pm["{#SITENAME}"] = "pm"

    proxy = {}
    proxy["{#SITENAME}"] = "proxy"

    procList["data"].append(pm)
    procList["data"].append(proxy)

    return json.dumps(procList, sort_keys=True, indent=4)

if __name__ == "__main__":
    if sys.argv[1] == "dis":
        print discovery()
    elif sys.argv[1] == "vsz":
        print getMem("vsz", sys.argv[2])
    elif sys.argv[1] == "rss":
        print getMem("rss", sys.argv[2])
    else:
        print "ERROR: 参数错误"
