## ZabbixScript
write more scripts for zabbix

* #### check_mysql_slave.py ####

  check the local mysql-slave-status that is based on discovery-function of zabbix.
  
* #### check_h700_status.py ####

  check disk raid status omnibearingly for zabbix
  
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
