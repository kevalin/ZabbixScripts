####################################################################################
#   H700 Raid卡磁盘监控 FOR Zabbix
#   
#   用法：
#       UserParameter=raid.h700[*],/usr/local/etc/scripts/check_h700_status.py $1        
####################################################################################
#! /usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

def getH700Status():
    infos = {}
    popShell = os.popen("sudo MegaCli -LDPDInfo -aall | egrep 'State|Current Cache Policy|Firmware state|Slot Number|Count:' | grep -v 'Foreign State'")
    popShellResult = popShell.read()
    popShell.close()

    arrayInfo = popShellResult.split('\n')
    del arrayInfo[len(arrayInfo) - 1]
    infos['State'] = arrayInfo[0].split(':')[1].replace(' ', '')
    infos['Current Cache Policy'] = arrayInfo[1].split(':')[1].split(',')[0].replace(' ', '')
    i = 2
    disk = []
    while(i < len(arrayInfo)):
        tempDisk = {}
        for x in arrayInfo[i:i+5]:
            tempDisk[x.split(':')[0]] = x.split(':')[1].split(',')[0].replace(' ', '')
        disk.append(tempDisk)
        i = i + 5
        
    infos['Disk'] = disk
    # 返回一个dict
    return infos

def printMediaError(obj):
    eMediaStr = []
    for i in obj['Disk']:
        if int(i['Media Error Count']) <> 0:
            eMediaStr.append(i['Media Error Count'])
    if len(eMediaStr) > 1:
        print 'Code:1 Info:有%d块磁盘同时存在Media Error'%(len(eMediaStr))
    else:
        print 'Code:0 Info:没有同时存在Media Error的磁盘'

def printOtherError(obj):
    eOtherStr = []
    for i in obj['Disk']:
        if int(i['Other Error Count']) <> 0:
            eOtherStr.append(i['Other Error Count'])
    if len(eOtherStr) > 1:
        print 'Code:1 Info:有%d块磁盘存在Other Error'%(len(eOtherStr))
    else:
        print 'Code:0 Info:没有同时存在Other Error的磁盘'

def printPredictiveFailure(obj):
    pStr = []
    for i in obj['Disk']:
        if int(i['Predictive Failure Count']) <> 0:
            tempObj2 = {}
            tempObj2[i['Slot Number']] = i['Predictive Failure Count']
            pStr.append(tempObj2)
    if len(pStr) > 0:
        print 'Code:1 Info:有%d块磁盘存在Predictive Failure'%(len(pStr))
    else:
        print 'Code:0 Info:没有磁盘存在Predictive Failure'

def printState(obj):
    if obj['State'] != 'Optimal':
        oStr = []
        for i in obj['Disk']:
            if i['Firmware state'] != 'Online':
                tempObj1 = {}
                tempObj1[i['Slot Number']] = i['Firmware state']
                oStr.append(tempObj1)
        print 'Code:1 Info:%s %s'%(obj['State'], oStr)
    else:
        print 'Code:0 Info:%s'%(obj['State'])

def printSumError(obj):
    errSum = 0
    for i in obj['Disk']:
        if int(i['Media Error Count']) <> 0:
            errSum += int(i['Media Error Count'])
        if int(i['Other Error Count']) <> 0:
            errSum += int(i['Other Error Count'])
    print errSum

def printBBU(obj):
    if obj['Current Cache Policy'] != 'WriteBack':
        print 'Code:1 Info:%s'%(obj['Current Cache Policy'])
    else:
        print 'Code:0 Info:%s'%(obj['Current Cache Policy'])

if __name__ == '__main__':
    obj = getH700Status()
   
    if (sys.argv[1] == 'Media Error'):
        printMediaError(obj)
    elif (sys.argv[1] == 'Other Error'):
        printOtherError(obj)
    elif (sys.argv[1] == 'Predictive Failure'):
        printPredictiveFailure(obj)
    elif (sys.argv[1] == 'State'):
        printState(obj)
    elif (sys.argv[1] == 'Sum Error'):
        printSumError(obj)
    elif (sys.argv[1] == 'BBU'):
        printBBU(obj)
    else:
        print "Usage: check_h700_status.py 'Media Error'|'Other Error'|'Predictive Failure'|'State'|'Sum Error'|'BBU'"
