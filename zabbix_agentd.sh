##############################################################################################
# configuration of zabbix-agentd for client
# version 0.3  date:2014/05/28
# usage:Run this script,input the type of your system(32 or 64).
#       Then,come back to zabbix-web,add your server-pc at configuration of hosts.It's so easy!
##############################################################################################
#! /bin/bash
mkdir -p /usr/local/zabbix
MY_IP=`ifconfig | grep '192.168.20.*' | cut -f 2 -d ":"|cut -f 1 -d " "`
ZABBIX_IP=192.168.20.12
MY_DIR1=/usr/local/src
MY_DIR2=/usr/local/zabbix
MY_DIR3=/usr/local/etc
MY_TAR32=zabbix_agents_32.tar.gz
MY_TAR64=zabbix_agents_64.tar.gz

function add_user_zabbix (){
    useradd zabbix -s /bin/false
}

function install_zabbix (){
    a=0
    while [ $a -eq 0 ]
    do
        echo "Please input the type of your system (32 or 64): "
        read yn
        if [ "$yn" = "32" ]; then
            cd $MY_DIR1
            wget ftp://192.168.20.12/pub/i386/$MY_TAR32
            tar -zvxf $MY_DIR1/$MY_TAR32 -C $MY_DIR2
            a=1
        elif [ "$yn" = "64" ]; then
            cd $MY_DIR1
            wget ftp://192.168.20.12/pub/x64/$MY_TAR64
            tar -zvxf $MY_DIR1/$MY_TAR64 -C $MY_DIR2
            a=1
        else
            a=0
        fi
    done
}

function add_zabbix_port (){
    echo "zabbix-agent    10050/tcp                       # Zabbix Agent TCP" >> /etc/services
    echo "zabbix-agent    10050/udp                       # Zabbix Agent UDP" >> /etc/services
}

function config_zabbix (){
    ln -s $MY_DIR2/sbin/zabbix_agentd /usr/sbin/zabbix_agentd
    cp $MY_DIR2/conf/zabbix_agentd.conf $MY_DIR3
    sed -i '81s/.*/Server='$ZABBIX_IP'/' $MY_DIR3/zabbix_agentd.conf
    sed -i '97s/.*/ListenIP='$MY_IP'/' $MY_DIR3/zabbix_agentd.conf
    sed -i '106s/.*/StartAgents=5/' $MY_DIR3/zabbix_agentd.conf
    sed -i '122s/.*/ServerActive='$ZABBIX_IP'/' $MY_DIR3/zabbix_agentd.conf
    sed -i '133s/.*/Hostname='$MY_IP'/' $MY_DIR3/zabbix_agentd.conf
    sed -i '242s/# //' $MY_DIR3/zabbix_agentd.conf
    sed -i '243s/# //' $MY_DIR3/zabbix_agentd.conf
    sed -i '255s/.*/UnsafeUserParameters=1/' $MY_DIR3/zabbix_agentd.conf
    touch $MY_DIR3/zabbix_agentd.userparams.conf
    mkdir -p $MY_DIR3/zabbix_agentd.conf.d
    mkdir -p $MY_DIR3/scripts
    cp $MY_DIR2/sbin/zabbix-agent /etc/init.d/
    chmod +x /etc/init.d/zabbix-agent
}

function get_userparams (){
    rm -f $MY_DIR3/zabbix_agentd.userparams.conf
    wget -P $MY_DIR3 ftp://192.168.20.12/pub/zabbix/zabbix_agentd.userparams.conf
}

function get_scripts (){
    wget -P $MY_DIR3/scripts ftp://192.168.20.12/pub/zabbix/scripts/*
    chmod +x $MY_DIR3/scripts/*
    touch $MY_DIR3/scripts/raid.log
    chmod 775 $MY_DIR3/scripts/raid.log
}

function get_userparams_conf (){
    wget -P /usr/local/etc/zabbix_agentd.conf.d/ ftp://192.168.20.12/pub/zabbix/zabbix_agentd.conf.d/*
}

function add_sudo (){
    echo "Defaults:zabbix !requiretty" >> /etc/sudoers
    echo "zabbix  ALL=(ALL) NOPASSWD: /usr/sbin/MegaCli" >> /etc/sudoers
    echo "zabbix  ALL=(ALL) NOPASSWD: /usr/sbin/mpt-status" >> /etc/sudoers
    echo "zabbix  ALL=(ALL) NOPASSWD: /usr/sbin/sas2ircu" >> /etc/sudoers
}

add_user_zabbix
add_zabbix_port
install_zabbix
config_zabbix
get_userparams
get_userparams_conf
get_scripts
chmod a+r /var/log/auth.log
chown -R root:zabbix $MY_DIR3/*
add_sudo
/etc/init.d/zabbix-agent start