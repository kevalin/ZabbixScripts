## ZabbixScript
write more scripts for zabbix

* #### check_mysql_slave.py ####

  使用zabbix LLD发现mysql端口完成同步状态（Binlog延迟和slave running2个方面）的监控。
  
    ```bash
    # zabbix_agentd userparams配置
    $ cat zabbix_agentd.conf.d/check_mysql_slave.conf 
    UserParameter=mysql.ports.discovery,sudo /usr/local/etc/scripts/check_mysql_slave.py
    UserParameter=mysql.slave.status[*],sudo /usr/local/etc/scripts/check_mysql_slave.py $1
    
    # zabbix_server调用
    $ zabbix_get -s 192.168.10.100 -k mysql.ports.discovery
    {
        "data": [
            {
                "{#MYSQL_PORT}": "3310"
            }, 
            {
                "{#MYSQL_PORT}": "3312"
            }, 
            {
                "{#MYSQL_PORT}": "3317"
            }, 
            {
                "{#MYSQL_PORT}": "3318"
            }, 
            {
                "{#MYSQL_PORT}": "3319"
            }, 
            {
                "{#MYSQL_PORT}": "3320"
            }, 
            {
                "{#MYSQL_PORT}": "3321"
            }, 
            {
                "{#MYSQL_PORT}": "3322"
            }
        ]
    }
    $ zabbix_get -s 192.168.10.100 -k mysql.slave.status[3322]
    {'Log_File': 'normal', 'Slave_Running': 'Yes'}
    ```
    
* #### check_h700_status.py ####

  使用MegaCli从6个方面检测H700 Raid卡磁盘状态。
  
    ```bash
    # 检测是否都多块磁盘同时存在Media Error
    $./check_h700_status.py 'Media Error'
    # 检测是否有多块磁盘同时存在Other Error
    $./check_h700_status.py 'Other Error'
    # 检测是否有磁盘存在Predictive Failure
    $./check_h700_status.py 'Predictive Failure'
    # 检测Raid状态
    $./check_h700_status.py 'State'
    # 检测所有磁盘存在的Error总数
    $./check_h700_status.py 'Sum Error'
    # 检测磁盘Cache是否为WB还是WT
    $./check_h700_status.py 'Cache'
    ```
* #### check_h700_status_plus.py ####

  使用过程中发现有多个Virtual Drive存在的问题，因此在上一个版本上做了改进。
  
    ```bash
    # zabbix_agentd userparams配置
    $ cat zabbix_agentd.userparams.conf
    UserParameter=raid.h700[*],/usr/local/etc/scripts/check_h700_status_plus.py $1
    
    # zabbix_server调用
    $ zabbix_get -s 192.168.10.100 -k raid.h700['State']
    Virtual Drive:0 Code:0 Info:Optimal
    Virtual Drive:1 Code:0 Info:Optimal
    $ zabbix_get -s 192.168.10.100 -k raid.h700['Cache']
    Virtual Drive:0 Code:0 Info:WriteBack
    Virtual Drive:1 Code:0 Info:WriteBack
    ```
  
* #### check_net_status.py ####

  脚本的主要目的是读取一个IP配置文件，然后输出JSON，再通过discovery完成对这些IP的连通性，丢包率，延迟监控。
  
    ```bash
    # zabbix_agentd userparams配置
    $ cat zabbix_agentd.userparams.conf
    UserParameter=my.net.discovery,/etc/zabbix/scripts/check_net_status.py
    
    $ ./check_net_status.py
    {
        "data": [
            {
                "{#IP}": "172.20.0.1"
            }, 
            {
                "{#IP}": "172.18.0.253"
            }
        ]
    }
    
    # 再使用simple_check完成监控
    # 丢包率
    icmppingloss[{#IP},10,1000,64,5000]
    # response时间
    icmppingsec[{#IP},10,1000,64,5000,avg]
    # 连通性，能ping通与否
    icmpping[{#IP},4,1000,64,10000]
    ```  

* #### install_zabbix_agentd_for_centos.sh ####

  之前的系统都是Debian，后来开始使用Centos，所以又写了一个用于一键安装和配置zabbix_agentd针对Centos的脚本。

* #### check_dev_io.py ####

  网上看过很多shell版本配置都比较多，个人喜欢少配置化，因此用python基于LLD和/proc/diskstats重写了之前的check_disk_io.sh。```注意```新建模板的时候```Store value```一点要选择```speed per second```。
  
    ```bash
    # zabbix_agentd userparams配置 
    $ cat zabbix_agentd.conf.d/check_dev_io.conf
    UserParameter=dev.io.discovery,/usr/local/etc/scripts/check_dev_io.py discovery
    UserParameter=dev.io.status[*],/usr/local/etc/scripts/check_dev_io.py status $1 $2
    
    # zabbix_server调用
    $ zabbix_get -s 192.168.10.100 -k dev.io.discovery
    {
        "data": [
            {
                "{#DEVNAME}": "sdb2", 
                "{#MOUNTNAME}": "/"
            }, 
            {
                "{#DEVNAME}": "sdb1", 
                "{#MOUNTNAME}": "/boot"
            }, 
            {
                "{#DEVNAME}": "sdb3", 
                "{#MOUNTNAME}": "/home"
            }, 
            {
                "{#DEVNAME}": "sda1", 
                "{#MOUNTNAME}": "/opt"
            }, 
            {
                "{#DEVNAME}": "sdb5", 
                "{#MOUNTNAME}": "/var"
            }
        ]
    }
    $ zabbix_get -s 192.168.10.100 -k dev.io.status[sdb5,read.ops]
    871
    ```
