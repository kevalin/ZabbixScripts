#! /bin/bash

function e1068 (){
    raid_status=`sudo mpt-status | sed -n '1p' | awk -F, '{print $4}' | awk '{print $2}'`
    phy1=`sudo mpt-status | sed -n '2p' | awk -F, '{print $1 $3}' | awk '{print $2,$3,$11}'`
    phy0=`sudo mpt-status | sed -n '3p' | awk -F, '{print $1 $3}' | awk '{print $2,$3,$11}'`
    echo "raid status:" $raid_status "- "$phy1"; "$phy0 > /usr/local/etc/scripts/raid.log
    info
}

function h200 (){
    raid_status=`sudo sas2ircu 0 status | sed -n '10p' | awk -F: '{print $2}'`
    phy=`sudo sas2ircu 0 display | grep -E 'State|Slot #' | grep -Ev 'Standby|: 9' | awk '/^Slot #/{if (n++) print ""}{printf $0}' | tr -s " " | sed 's/)/&;/g' | sed 's/(OPT)//g; s/# ://g; s/State//g' | tr -s " "`
    echo "raid status:"$raid_status "-"$phy > /usr/local/etc/scripts/raid.log
    info
}

function h700 (){
    raid_status=`sudo MegaCli -LDInfo -LALL -aAll | grep 'State' | awk -F: '{print $2}'`
    phy=`sudo MegaCli -PDList -aAll | egrep  "Slot Number|Firmware state" | awk '/^Slot #/{if (n++) print ""}{printf $0}' | sed 's/Number://g;s/, Spun Up/; /g' | tr -s " " | sed 's/F/ F/g' | sed 's/Firmware state//g'`
    err=`MegaCli -pdlist -a0 | grep "Error" | awk 'BEGIN{err=0}{err+=$4}END{print err}'`
    echo "raid status:"$raid_status "- "$phy "Error:"$err > /usr/local/etc/scripts/raid.log
    info
}

function info (){
    cat /usr/local/etc/scripts/raid.log
}

case "$1" in
    1068e)
        e1068
    ;;
    h200)
        h200
    ;;
    h700)
        h700
    ;;
    *)
        echo "请输入正确raid卡类型(1068e,h200,h700)!"
    ;;
esac
