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
        # 读磁盘的次数，成功完成读的总次数
        cmdString = "cat /proc/diskstats | grep " + devName + " | head -1 | awk '{print $4}'"
        print commands.getoutput(cmdString)
    elif item == 'write.ops':
        # 写完成的次数，成功写完成的总次数
        cmdString = "cat /proc/diskstats | grep " + devName + " | head -1 | awk '{print $8}'"
        print commands.getoutput(cmdString)
    elif item == 'read.ms':
        # 读花费的毫秒数，这是所有读操作所花费的毫秒数
        cmdString = "cat /proc/diskstats | grep " + devName + " | head -1 | awk '{print $7}'"
        print commands.getoutput(cmdString)
    elif item == 'write.ms':
        # 写花费的毫秒数，这是所有写操作所花费的毫秒数
        cmdString = "cat /proc/diskstats | grep " + devName + " | head -1 | awk '{print $11}'"
        print commands.getoutput(cmdString)
    elif item == 'io.ms':
        # 花在I/O操作上的毫秒数
        cmdString = "cat /proc/diskstats | grep " + devName + " | head -1 | awk '{print $13}'"
        print commands.getoutput(cmdString)
    elif item == 'read.sectors':
        # 读扇区的次数，成功读过的扇区总次数
        cmdString = "cat /proc/diskstats | grep " + devName + " | head -1 | awk '{print $6}'"
        print commands.getoutput(cmdString)
    elif item == 'write.sectors':
        # 写扇区的次数，成功写扇区总次数
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
