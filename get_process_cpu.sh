#####################################################################################################
# check process cpu percent for zabbix
# version 0.1  date:2014/07/02
# usage:
#   UserParameter=my.pid.discovery[*],/usr/local/etc/scripts/get_process_cpu.sh pid_discovery $1
#   UserParameter=my.cpu.percent[*],/usr/local/etc/scripts/get_process_cpu.sh cpu_percent $1
#####################################################################################################
#! /bin/sh

function pid_discovery()
{   
    Arraypid=(`pidof "$1"`)
    leng=${#Arraypid[@]}
    printf "{\n"
    printf '\t'"\"data\":["
    for((i=0;i<$leng;i++))
    do
        printf '\n\t\t{'
        printf "\"{#PID_NUM}\":\"${Arraypid[$i]}\"}"
        if [ $i -lt $[$leng-1] ]; then
            printf ','
        fi
    done
        printf  "\n\t]\n"
        printf "}\n"
}

function cpu_percent()
{
    v=`top -bn1 | grep -w "$1" | awk '{print $9}'`
    echo $v
}

case "$1" in
    pid_discovery)
    pid_discovery $2
     ;;
    cpu_percent)
    cpu_percent $2
     ;;
    *)
    echo "Usage:$0 pid_discovery|cpu_percent [type]}"
     ;;
esac