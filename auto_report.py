#! /usr/bin/env python
#coding=utf-8
import time, os
import urllib
import urllib2
import cookielib
import MySQLdb
import smtplib
from email.mime.text import MIMEText
from email.Header import Header

save_graph_path = "/usr/share/zabbix/report/%s"%time.strftime("%Y-%m-%d")
if not os.path.exists(save_graph_path):
    os.makedirs(save_graph_path)

# zabbix web
zabbix_host = "IP/zabbix"
username = "Admin"
password = "XXXX"
width = 900
height = 200
period = 604800

# zabbix DB
dbhost = "localhost"
dbuser = "zabbix"
dbpasswd = "XXXXX"
dbport = 3306
dbname = "zabbix"

# mail
to_list = ["XXXX", "XXXX"]
smtp_server = "smtp.163.com"
mail_user = "XXXX"
mail_pass = "XXXX"
domain = "163.com"

def mysql_query(sql):
    try:
        conn = MySQLdb.connect(host = dbhost, user = dbuser, passwd = dbpasswd, port = dbport, connect_timeout = 20)
        conn.select_db(dbname)
        cur = conn.cursor()
        rows = cur.execute(sql)
        if rows == 0:
            result = 0
        else:
            result = cur.fetchall()
        return result
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print "mysql error:",e

def get_io_graph(zabbix_host,username,password,width,height,period,save_graph_path):
    global html
    myinfo = ''
    sql = """select a.graphid from graphs a where a.graphid in (
        select t2.graphid from items t1
        INNER JOIN graphs_items t2
        ON t1.itemid = t2.itemid
        where t1.hostid in (select t.hostid from `hosts` t where t.`status` = 0))
        and a.`name` = 'Disk I/O performance'"""
    graph_id = mysql_query(sql)
    for i in graph_id:
        login_opt = urllib.urlencode({
        "name": username,
        "password": password,
        "autologin": 1,
        "enter": "Sign in"})

        get_graph_opt = urllib.urlencode({
        "graphid": i[0],
        "width": width,
        "height": height,
        "period": period})

        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        login_url = r"http://%s/index.php"%zabbix_host
        save_graph_url = r"http://%s/zabbix_chart.php"%zabbix_host
        opener.open(login_url,login_opt).read()
        data = opener.open(save_graph_url,get_graph_opt).read()
        filename = "%s/%s.png"%(save_graph_path,i[0])
        myinfo += '<img width="500" height="350" src="http://%s/%s/%s/%s.png">'%(zabbix_host,save_graph_path.split("/")[len(save_graph_path.split("/"))-2],save_graph_path.split("/")[len(save_graph_path.split("/"))-1],i[0])
        f = open(filename,"wb")
        f.write(data)
        f.close()
    html += '<h3>平台数据库I/O性能监控</h3>%s<br>'%(myinfo)

def get_tcp_graph(zabbix_host,username,password,width,height,period,save_graph_path):
    global html
    myinfo = ''
    sql = """select a.graphid from graphs a where a.graphid in (
        select t2.graphid from items t1
        INNER JOIN graphs_items t2
        ON t1.itemid = t2.itemid
        where t1.hostid in (select t.hostid from `hosts` t where t.`status` = 0))
        and a.`name` = 'TCP connections'"""
    graph_id = mysql_query(sql)
    for i in graph_id:
        login_opt = urllib.urlencode({
        "name": username,
        "password": password,
        "autologin": 1,
        "enter": "Sign in"})

        get_graph_opt = urllib.urlencode({
        "graphid": i[0],
        "width": width,
        "height": height,
        "period": period})

        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        login_url = r"http://%s/index.php"%zabbix_host
        save_graph_url = r"http://%s/zabbix_chart.php"%zabbix_host
        opener.open(login_url,login_opt).read()
        data = opener.open(save_graph_url,get_graph_opt).read()
        filename = "%s/%s.png"%(save_graph_path,i[0])
        myinfo += '<img width="500" height="350" src="http://%s/%s/%s/%s.png">'%(zabbix_host,save_graph_path.split("/")[len(save_graph_path.split("/"))-2],save_graph_path.split("/")[len(save_graph_path.split("/"))-1],i[0])
        f = open(filename,"wb")
        f.write(data)
        f.close()
    html += '<h3>平台TCP连接数统计</h3>%s<br>'%(myinfo)

def get_events_count():
    global html
    mytable = ''
    info = ''
    sql = "select t2.priority, count(t2.priority) AS count FROM `events` t1 INNER JOIN `triggers` t2 ON t1.objectid = t2.triggerid WHERE t1.clock > UNIX_TIMESTAMP(date_sub(now(), INTERVAL 1 WEEK)) GROUP BY t2.priority"
    result = mysql_query(sql)
    for row in result:
        if row[0] == 1:
            info = "信息"
        elif row[0] == 2:
            info = "警告"
        elif row[0] == 3:
            info = "一般"
        elif row[0] == 4:
            info = "严重"
        elif row[0] == 5:
            info = "灾难"
        else:
            info = "其他"
        mytable += '<tr><td>%s</td><td>%s</td></tr>'%(info, row[1])
    html += '<h3>ZABBIX周报警统计</h3><table border="1" bordercolor="#000000" cellpadding="2" cellspacing="0" style="font-size: 10pt; border-collapse:collapse; border:none"><tr><th>报警等级</th><th>数量</th></tr>%s</table><br>'%(mytable)
    #print html

def send_mail(username,password,smtp_server,to_list,sub,content):
    print to_list
    me = "Zabbix"+"<"+username+"@"+domain+">"
    msg = MIMEText(content,_subtype="html",_charset="UTF-8")
    msg["Subject"] = Header(sub, 'UTF-8')
    msg["From"] = me
    msg["To"] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(smtp_server)
        server.login(username,password)
        server.sendmail(me,to_list,msg.as_string())
        server.close()
        print "send mail Ok!"
    except Exception, e:
        print e

if __name__ == '__main__':
    global html
    html = ''
    date = time.strftime("%Y/%m/%d")
    title = "%s 平台运维报告"%date
    get_events_count()
    get_io_graph(zabbix_host,username,password,width,height,period,save_graph_path)
    get_tcp_graph(zabbix_host,username,password,width,height,period,save_graph_path)
    send_mail(mail_user,mail_pass,smtp_server,to_list,title,html)