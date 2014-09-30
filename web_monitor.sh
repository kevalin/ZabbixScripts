#!/bin/bash 
# function:monitor tcp connect status from zabbix 
# usage:
#   UserParameter=web.site.discovery,/etc/zabbix/scripts/web_site_code_status web_site_discovery 
#   UserParameter=web.site.code[*],/etc/zabbix/scripts/web_site_code_status web_site_code $1 
source /etc/bashrc >/dev/null 2>&1 
source /etc/profile  >/dev/null 2>&1 
#/usr/bin/curl -o /dev/null -s -w %{http_code} http://$1/ 
WEB_SITE_discovery () { 
    WEB_SITE=($(cat  WEB1.txt|grep -v "^#")) 
    printf '{\n' 
    printf '\t"data":[\n' 
    for((i=0;i<${#WEB_SITE[@]};++i)) { 
        num=$(echo $((${#WEB_SITE[@]}-1))) 
            if [ "$i" != ${num} ]; then 
                printf "\t\t{ \n" 
                printf "\t\t\t\"{#SITENAME}\":\"${WEB_SITE[$i]}\"},\n" 
            else 
                printf  "\t\t{ \n" 
                printf  "\t\t\t\"{#SITENAME}\":\"${WEB_SITE[$num]}\"}]}\n" 
            fi
        } 
    }

web_site_code () { 
    /usr/bin/curl -o /dev/null -s -w %{http_code} http://$1 
}

case "$1" in 
    web_site_discovery) 
    WEB_SITE_discovery 
    ;; 
    web_site_code) 
    web_site_code $2 
    ;; 
    *) 
    echo "Usage:$0 {web_site_discovery|web_site_code [URL]}" 
    ;; 
esac 
