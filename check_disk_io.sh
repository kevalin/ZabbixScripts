


#####################################################################################################
# check disk io performance for zabbix
# version 0.1  date:2014/05/28
# usage:
#   UserParameter=disk.io.discovery,/usr/local/etc/scripts/check_disk_io.sh disk_io_discovery
#   UserParameter=disk.io.type[*],/usr/local/etc/scripts/check_disk_io.sh io_type $1(rrqm/wrqm/wrqm...)
#####################################################################################################
#! /bin/sh
function disk_io_discovery()
{
    mydiskname=`iostat -d -x -k 1 1 | awk 'NR>=4&&NR<=4 {printf $1}'`
    printf "{\n"
    printf '\t'"\"data\":["
    printf '\n\t\t{'
    printf "\"{#DISK_NAME}\":\"$mydiskname\"}"
    printf  "\n\t]\n"
    printf "}\n"
}

function io_type()
{
    case "$1" in
        rrqm)
        awk 'NR>=7&&NR<=7 {printf $2}' /tmp/iostat.cache
         ;;
        wrqm)
        awk 'NR>=7&&NR<=7 {printf $3}' /tmp/iostat.cache
         ;;
        readtimes)
        awk 'NR>=7&&NR<=7 {printf $4}' /tmp/iostat.cache
         ;;
        writetimes)
        awk 'NR>=7&&NR<=7 {printf $5}' /tmp/iostat.cache
         ;;
        rkB)
        awk 'NR>=7&&NR<=7 {printf $6}' /tmp/iostat.cache
         ;;
        wkB)
        awk 'NR>=7&&NR<=7 {printf $7}' /tmp/iostat.cache
         ;;
        await)
        awk 'NR>=7&&NR<=7 {printf $8}' /tmp/iostat.cache
         ;;
        svctm)
        awk 'NR>=7&&NR<=7 {printf $11}' /tmp/iostat.cache
         ;;
        util)
        awk 'NR>=7&&NR<=7 {printf $12}' /tmp/iostat.cache
         ;;
        *)
        echo "unknown type"
         ;;
    esac
}

case "$1" in
    disk_io_discovery)
    disk_io_discovery
     ;;
    io_type)
    io_type $2
     ;;
    *)
    echo "Usage:$0 disk_io_discovery|io_type [type]}"
     ;;
esac
