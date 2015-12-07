## ZabbixScript
write more scripts for zabbix

* #### check_mysql_slave.py ####

  check the local mysql-slave-status that is based on discovery-function of zabbix.
  
* #### check_h700_status.py ####

  check disk raid status omnibearingly for zabbix
  
    ```bash
    $./check_h700_status.py 'Media Error' #checking all disk that have Media Error
    $./check_h700_status.py 'Other Error' #checking all disk that have Other Error
    $./check_h700_status.py 'Predictive Failure' #checking all disk that have Predictive Failure
    $./check_h700_status.py 'State' #checking raid state
    $./check_h700_status.py 'Sum Error' #checking all disk that have sum Errors
    $./check_h700_status.py 'BBU' #checking WR or WT status of raid
    ```
