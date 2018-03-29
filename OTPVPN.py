#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pyotp
import MySQLdb
import time
from flask import Flask
from flask.ext.httpauth import HTTPBasicAuth
from flask import request
import json
from threading import Timer
#renzheng
auth = HTTPBasicAuth()
app = Flask(__name__)

def dingshi():
    db = MySQLdb.connect("localhost", "root", "asin7SGAcdB12ci^t5987.com", "flask")
    cursor = db.cursor()
    BASE = pyotp.random_base32()
    totp = pyotp.TOTP("%s" % BASE)
    PASSWD = totp.now()
    sql4 = "update users set passwd='%s' where name='%s'" % (PASSWD, VPNUSER)
    cursor.execute(sql4)
    db.commit()
    print '修改完毕'
    db.close()
    print '关闭数据库链接'

@app.route('/')
def getvpnpasswd():
    global VPNUSER
    VPNUSER = request.args.get('user')
    BASE = pyotp.random_base32()
    totp = pyotp.TOTP("%s" % BASE)
    PASSWD = totp.now()
# 打开数据库连接
    db = MySQLdb.connect("localhost","root","asin7SGAcdB12ci^t5987.com","flask" )
# 使用cursor()方法获取操作游标
    cursor = db.cursor()
# SQL 查询语句
    sql1 = "SELECT name FROM users where name='%s'" %VPNUSER
# sql insert
    sql2 = ('insert into users(name) values("%s")' %VPNUSER)
    sql3 = "update users set passwd='%s' where name='%s'" %(PASSWD,VPNUSER)
#try:
   # 执行SQL语句
    cursor.execute(sql1)
   # 获取所有记录列表
#results = cursor.fetchone()
    results = cursor.fetchall()
    if results:
        print "have data"
        cursor.execute(sql3)
        db.commit()
        db.close()
        result = {
            'VPNUSER': VPNUSER,
            'PASSWD': PASSWD
        }
        Timer(280, dingshi).start()
        print '定时任务开始执行'
        return json.dumps(result)
    else:
        print "no data"
        cursor.execute(sql2)
        cursor.execute(sql3)
        db.commit()
        print "yijing charu"
        db.close()
        result = {
           'VPNUSER': VPNUSER,
           'PASSWD': PASSWD
         }
        Timer(280, dingshi).start()
        print '定时任务开始执行'
        return json.dumps(result)


#    Timer(10, dingshi, (time.time(),)).start()
#    print  'zhixingwanbi,chakanjieguo'
if __name__ == '__main__':
    app.run()