#! /usr/bin/python
# -*- coding: utf-8 -*-
import os, sys, json, commands

def getDevInfo():
    popShell = os.popen("df -h | grep dev | egrep -v 'udev|tmpfs' | awk '{print $1, $6}'")
    popShellResult = popShell.read()
    popShell.close()
    
    infos = {}
    data = []
    arrayInfo = popShellResult.split('\n')
    del arrayInfo[len(arrayInfo) - 1]
    
    for i in range(len(arrayInfo)):
        tempDict = {}
        tempDict['{#DEVNAME}'] = arrayInfo[i].split(' ')[0].split('/')[2]
        tempDict['{#MOUNTNAME}'] = arrayInfo[i].split(' ')[1]
        
        data.append(tempDict)
    infos['data'] = data
    return json.dumps(infos, sort_keys=True, indent=4)
    
def getIoStatus(devName, item):
    if item == 'read.ops':
        cmdString = "cat /proc/diskstats | grep " + devName + " | head -1 | awk '{print $4}'"
        print commands.getoutput(cmdString)
    elif item == 'write.ops':
        cmdString = "cat /proc/diskstats | grep " + devName + " | head -1 | awk '{print $8}'"
        print commands.getoutput(cmdString)
    elif item == 'read.ms':
        cmdString = "cat /proc/diskstats | grep " + devName + " | head -1 | awk '{print $7}'"
        print commands.getoutput(cmdString)
    elif item == 'write.ms':
        cmdString = "cat /proc/diskstats | grep " + devName + " | head -1 | awk '{print $11}'"
        print commands.getoutput(cmdString)
    elif item == 'io.ms':
        cmdString = "cat /proc/diskstats | grep " + devName + " | head -1 | awk '{print $13}'"
        print commands.getoutput(cmdString)
    elif item == 'read.sectors':
        cmdString = "cat /proc/diskstats | grep " + devName + " | head -1 | awk '{print $6}'"
        print commands.getoutput(cmdString)
    elif item == 'write.sectors':
        cmdString = "cat /proc/diskstats | grep " + devName + " | head -1 | awk '{print $10}'"
        print commands.getoutput(cmdString)
    else:
        print "ERROR: item error"
    
if __name__ == '__main__':
    if sys.argv[1] == 'discovery':
        print getDevInfo()
    elif sys.argv[1] == 'status':
        getIoStatus(sys.argv[2], sys.argv[3])
    else:
        print "ERROR: argument error"
