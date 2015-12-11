#! /bin/bash
SOFTDIR=/usr/local/src
SZABBIXDIR=/usr/local/zabbix
DZABBIXDIR=/usr/local/etc
LOCALIP=`ifconfig | grep '192.168.20.*' | cut -f 2 -d ":"|cut -f 1 -d " "`
ZABBIXSERVER=192.168.20.12
WGETHTTP='ftp://192.168.20.12/pub'

function log() {
    if [ $? -eq 0 ]; then
        echo -e "$* \033[32m[ OK ]\033[0m"
    elif [ $? -eq 1 ]; then
        echo -e "$* \033[31m[ Faild ]\033[0m"
    else
        echo -e "$* \033[33m[ Warn ]\033[0m"
    fi
}

function initSys() {
    mkdir -p /usr/local/zabbix
    useradd zabbix -s /bin/false

    if [ `grep '10050\/tcp' /etc/services | wc -l` -eq 1 ]; then
        printf  "\033[33mzabbix-agent    10050/tcp 已添加\033[0m\n"
    else
        echo "zabbix-agent    10050/tcp                       # Zabbix Agent TCP" >> /etc/services
        log "add zabbix-agent 10050/tcp"
    fi

    if [ `grep '10050\/udp' /etc/services | wc -l` -eq 1 ]; then
        printf "\033[33mzabbix-agent    10050/udp 已添加\033[0m\n"
    else
        echo "zabbix-agent    10050/udp                       # Zabbix Agent UDP" >> /etc/services
        log "add zabbix-agent 10050/udp"
    fi

    if [ `getconf LONG_BIT` -eq 64 ]; then
        if [ ! -f ${SOFTDIR}/zabbix_agents_2.2.1.linux2_6.amd64.tar.gz ]; then
            wget -P $SOFTDIR ${WGETHTTP}/x64/zabbix_agents_2.2.1.linux2_6.amd64.tar.gz -q
            log "Download zabbix_agents_2.2.1.linux2_6.amd64.tar.gz"
            tar -zxf ${SOFTDIR}/zabbix_agents_2.2.1.linux2_6.amd64.tar.gz -C $SZABBIXDIR
            initZabbixBin
        fi
    elif [ `getconf LONG_BIT` -eq 32 ]; then
        if [ ! -f ${SOFTDIR}/zabbix_agents_2.2.1.linux2_6.i386.tar.gz ]; then
            wget -P $SOFTDIR ${WGETHTTP}/i386/zabbix_agents_2.2.1.linux2_6.i386.tar.gz -q
            log "Download zabbix_agents_2.2.1.linux2_6.i386.tar.gz"
            tar -zxf ${SOFTDIR}/zabbix_agents_2.2.1.linux2_6.i386.tar.gz -C $SZABBIXDIR
            initZabbixBin
        fi
    fi
}

function initZabbixBin() {
    chmod +x ${SZABBIXDIR}/sbin/*
    chmod +x ${SZABBIXDIR}/bin/*
    rm -f bin/sbin/zabbix_agentd
    rm -f bin/sbin/zabbix_get
    ln -s ${SZABBIXDIR}/sbin/zabbix_agentd /usr/sbin/zabbix_agentd
    ln -s ${SZABBIXDIR}/bin/zabbix_get /usr/sbin/zabbix_get
}

function initZabbixSudoers() {
    if [ `grep 'zabbix  ALL=(ALL)' /etc/sudoers | wc -l` -eq 3 ]; then
        printf "\033[33msudoers已经添加zabbix\033[0m\n"
    else
        echo "Defaults:zabbix !requiretty" >> /etc/sudoers
        echo "zabbix  ALL=(ALL) NOPASSWD: /usr/sbin/MegaCli" >> /etc/sudoers
        echo "zabbix  ALL=(ALL) NOPASSWD: /usr/sbin/mpt-status" >> /etc/sudoers
        echo "zabbix  ALL=(ALL) NOPASSWD: /usr/sbin/sas2ircu" >> /etc/sudoers
        log "Add zabbix sudoers"
    fi
}

function configZabbix() {
    cp ${SZABBIXDIR}/conf/zabbix_agentd.conf $DZABBIXDIR
    mkdir -p ${DZABBIXDIR}/scripts
    mkdir -p ${DZABBIXDIR}/zabbix_agentd.conf.d
    touch ${DZABBIXDIR}/scripts/raid.log
    chmod 777 ${DZABBIXDIR}/scripts/raid.log
    mkdir -p ${DZABBIXDIR}/zabbix_agentd.conf.d
    sed -i '81s/.*/Server='${ZABBIXSERVER}'/' ${DZABBIXDIR}/zabbix_agentd.conf
    log "Set Server=${ZABBIXSERVER}"
    sed -i '97s/.*/ListenIP='${LOCALIP}'/' ${DZABBIXDIR}/zabbix_agentd.conf
    log "Set ListenIP=${LOCALIP}"
    sed -i '106s/.*/StartAgents=5/' ${DZABBIXDIR}/zabbix_agentd.conf
    log "Set StartAgents=5"
    sed -i '122s/.*/ServerActive='$ZABBIXSERVER'/' ${DZABBIXDIR}/zabbix_agentd.conf
    log "Set ServerActive=${ZABBIXSERVER}"
    sed -i '133s/.*/Hostname='${LOCALIP}'/' ${DZABBIXDIR}/zabbix_agentd.conf
    log "Set Hostname=${LOCALIP}"
    sed -i '242s/# //' ${DZABBIXDIR}/zabbix_agentd.conf
    log "Set Include zabbix_agentd.userparams.conf"
    sed -i '243s/# //' ${DZABBIXDIR}/zabbix_agentd.conf
    log "Set Include zabbix_agentd.conf.d"
    sed -i '255s/.*/UnsafeUserParameters=1/' ${DZABBIXDIR}/zabbix_agentd.conf
    log "Set UnsafeUserParameters=1"

    wget -P $DZABBIXDIR ${WGETHTTP}/zabbix/zabbix_agentd.userparams.conf -q
    log "Download zabbix_agentd.userparams.conf"
    wget -P $DZABBIXDIR/scripts ${WGETHTTP}/zabbix/scripts/* -q
    log "Download zabbix scripts"

    chmod +x $DZABBIXDIR/scripts/*
}

function startZabbixAgentd() {
    pkill zabbix
    zabbix_agentd -c ${DZABBIXDIR}/zabbix_agentd.conf
    log "Start zabbix_agentd"
}

printf "\033[32mINIT SYSTEM\033[0m\n"
printf "\033[32m=====================================================\033[0m\n"
initSys
printf "\033[32mCONFIG ZABBIX_AGENTD\033[0m\n"
printf "\033[32m=====================================================\033[0m\n"
initZabbixSudoers
configZabbix
printf "\033[32mSTART ZABBIX_AGENTD\033[0m\n"
printf "\033[32m=====================================================\033[0m\n"
startZabbixAgentd
