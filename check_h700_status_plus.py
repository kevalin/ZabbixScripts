####################################################################################
#   H700 Raid卡磁盘监控扩展版（包括对多个Virtual Drive进行检查） FOR Zabbix
#   
#   用法：
#       UserParameter=raid.h700[*],/usr/local/etc/scripts/check_h700_status.py $1        
####################################################################################
#! /usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

def formatList(list):
    info = {}
    arrayInfo = list.split('\n')
    del arrayInfo[len(arrayInfo) - 1]
    info['Virtual Drive'] = arrayInfo[0].split(' ')[0]
    info['State'] = arrayInfo[1].split(':')[1].replace(' ', '')
    info['Current Cache Policy'] = arrayInfo[2].split(':')[1].split(',')[0].replace(' ', '')
    i = 3
    disk = []
    while(i < len(arrayInfo)):
        tempDisk = {}
        for x in arrayInfo[i:i+5]:
            tempDisk[x.split(':')[0]] = x.split(':')[1].split(',')[0].replace(' ', '')
        disk.append(tempDisk)
        i = i + 5
        
    info['Disk'] = disk
    # 返回一个dict
    return info

def getH700Status():
    infos = []
    popShell = os.popen("sudo MegaCli -LDPDInfo -aall | egrep 'Virtual Drive|State|Current Cache Policy|Firmware state|Slot Number|Count:' | egrep -v 'Foreign State|Media Type'")
    popShellResult = popShell.read()
    popShell.close()
    tempFormat = popShellResult.split('Virtual Drive: ')
    del tempFormat[0]
    for i in range(len(tempFormat)):
        infos.append(formatList(tempFormat[i]))
    # 返回一个list
    return infos
    
def printMediaError(obj):
    eMediaStr = []
    for i in obj['Disk']:
        if int(i['Media Error Count']) <> 0:
            eMediaStr.append(i['Media Error Count'])
    if len(eMediaStr) > 1:
        return 'Code:1 Info:有%d块磁盘同时存在Media Error'%(len(eMediaStr))
    else:
        return 'Code:0 Info:没有同时存在Media Error的磁盘'

def printOtherError(obj):
    eOtherStr = []
    for i in obj['Disk']:
        if int(i['Other Error Count']) <> 0:
            eOtherStr.append(i['Other Error Count'])
    if len(eOtherStr) > 1:
        return 'Code:1 Info:有%d块磁盘存在Other Error'%(len(eOtherStr))
    else:
        return 'Code:0 Info:没有同时存在Other Error的磁盘'

def printPredictiveFailure(obj):
    pStr = []
    for i in obj['Disk']:
        if int(i['Predictive Failure Count']) <> 0:
            tempObj2 = {}
            tempObj2[i['Slot Number']] = i['Predictive Failure Count']
            pStr.append(tempObj2)
    if len(pStr) > 0:
        return 'Code:1 Info:有%d块磁盘存在Predictive Failure %s'%(len(pStr), pStr)
    else:
        return 'Code:0 Info:没有磁盘存在Predictive Failure'

def printState(obj):
    if obj['State'] != 'Optimal':
        oStr = []
        for i in obj['Disk']:
            if i['Firmware state'] != 'Online':
                tempObj1 = {}
                tempObj1[i['Slot Number']] = i['Firmware state']
                oStr.append(tempObj1)
        return 'Code:1 Info:%s %s'%(obj['State'], oStr)
    else:
        return 'Code:0 Info:%s'%(obj['State'])

def printSumError(obj):
    errSum = 0
    for i in obj['Disk']:
        if int(i['Media Error Count']) <> 0:
            errSum += int(i['Media Error Count'])
        if int(i['Other Error Count']) <> 0:
            errSum += int(i['Other Error Count'])
    return errSum

def printCache(obj):
    if obj['Current Cache Policy'] != 'WriteBack':
        return 'Code:1 Info:%s'%(obj['Current Cache Policy'])
    else:
        return 'Code:0 Info:%s'%(obj['Current Cache Policy'])

if __name__ == '__main__':
    obj = getH700Status()
   
    if sys.argv[1] == 'Media Error':
        for i in range(len(obj)):
            print 'Virtual Drive:%s %s'%(obj[i]['Virtual Drive'], printMediaError(obj[i]))
    elif sys.argv[1] == 'Other Error':
        for i in range(len(obj)):
            print 'Virtual Drive:%s %s'%(obj[i]['Virtual Drive'], printOtherError(obj[i]))
    elif sys.argv[1] == 'Predictive Failure':
        for i in range(len(obj)):
            print 'Virtual Drive:%s %s'%(obj[i]['Virtual Drive'], printPredictiveFailure(obj[i]))
    elif sys.argv[1] == 'State':
        for i in range(len(obj)):
            print 'Virtual Drive:%s %s'%(obj[i]['Virtual Drive'], printState(obj[i]))
    elif sys.argv[1] == 'Sum Error':
        sumErr = 0
        for i in range(len(obj)):
            sumErr += printSumError(obj[i])
        print sumErr
    elif sys.argv[1] == 'Cache':
        for i in range(len(obj)):
            print 'Virtual Drive:%s %s'%(obj[i]['Virtual Drive'], printCache(obj[i]))
    else:
        print "Usage: check_h700_status.py 'Media Error'|'Other Error'|'Predictive Failure'|'State'|'Sum Error'|'Cache'"
