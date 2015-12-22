#! /usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, json, commands

class zabbixMysqlClass(object):
    version = 0.0.2

    def __init__(self, host='127.0.0.1', user='monitoraccount', password='FC9BF8E98A'):
        self.host = host
        self.user = user
        self.password = password
        popenMysqlPort = os.popen("netstat -anp | grep mysqld | grep -v 'unix' | egrep '0.0.0.0:3[0-9]{3,}' | awk '{print $4}' | awk -F: '{print $2}'")
        a = popenMysqlPort.read()
        self.listMysqlPort = a.replace('\n', ',')[:-1].split(',')
        popenMysqlPort.close()

    def port_discovery(self):
        a = []
        ports = {}
        for i in self.listMysqlPort: 
            checkPortCMD = "mysql -u" + self.user + " -p" + self.password + " -h" + self.host + " -P" + str(i) + " -e 'show slave status \G' | egrep 'Slave_IO_Running|Slave_SQL_Running|Master_Log_File|Relay_Master_Log_File'"
            popenCheckPortStatus = os.popen(checkPortCMD)
            thisPortSlaveStatus = popenCheckPortStatus.read()
            popenCheckPortStatus.close()
            (status, output) = commands.getstatusoutput(checkPortCMD)
            if status != 0:
                continue
            elif thisPortSlaveStatus.strip() == '':
                continue
            else:
                if (thisPortSlaveStatus.replace(' ', '').replace('\n', ','))[:-1].split(',')[0].split(':')[1].strip() == '':
                    continue
                else:
                    x = {}
                    x["{#MYSQL_PORT}"] = i
                    a.append(x)
        ports["data"] = a
        print json.dumps(ports, sort_keys=True, indent=4)
    
    def slave_status(self):
        slaveCMD = "mysql -u" + self.user + " -p" + self.password + " -h" + self.host + " -P" + sys.argv[1] + " -e 'show slave status \G' | egrep 'Slave_IO_Running|Slave_SQL_Running|Master_Log_File|Relay_Master_Log_File'"
        popenSlaveStatus = os.popen(slaveCMD)
        slaveStatus = popenSlaveStatus.read()
        popenSlaveStatus.close()
        result = {}
        a = slaveStatus.replace(' ', '').replace('\n', ',')
        a = a[:-1].split(',')
        if int(a[0].split(':')[1].split('.')[1]) != int(a[1].split(':')[1].split('.')[1]):
            result['Log_File'] = 'delay'
        else:
            result['Log_File'] = 'normal'
        
        result['Slave_IO_Running'] = a[2].split(':')[1]
        result['Slave_SQL_Running'] = a[3].split(':')[1]
        print result

if __name__ == '__main__':
    myClass = zabbixMysqlClass()
    if len(sys.argv) > 1 and len(sys.argv) < 3:
        myClass.slave_status()
    elif len(sys.argv) > 0 and len(sys.argv) < 2:
        myClass.port_discovery()
    else:
        print 'ERROR:参数错误'
