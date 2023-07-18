#!/usr/bin/python3
# encoding:utf-8
import re
import urllib.request
import urllib
import os
import sys
import paramiko
import mysql.connector
import json
import time
from mysql.connector.pooling import MySQLConnectionPool
from mysql.connector import connect
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest


MAKER_STOP_LOSS_PRIVATE_IP_ARR = []

GET_BINANCE_POSITION_PRIVATE_IP_ARR = []

POSITION_RISK_PRIVATE_IP_ARR = []

COMMISSION_PRIVATE_IP_ARR = []

WEB_OSS_UPDATE_PRIVATE_IP_ARR = []

CHECK_TIME_OUT_ORDERS_PRIVATE_IP_ARR = []

WS_POSITION_PRIVATE_IP_ARR = []

TRADES_UPDATE_PRIVATE_IP_ARR = []


BINANCE_RECORD_PRIVATE_IP_ARR = []

def getServerInfo():
    global BINANCE_RECORD_PRIVATE_IP_ARR,TRADES_UPDATE_PRIVATE_IP_ARR,WS_POSITION_PRIVATE_IP_ARR,MAKER_STOP_LOSS_PRIVATE_IP_ARR,GET_BINANCE_POSITION_PRIVATE_IP_ARR,POSITION_RISK_PRIVATE_IP_ARR,COMMISSION_PRIVATE_IP_ARR,WEB_OSS_UPDATE_PRIVATE_IP_ARR,CHECK_TIME_OUT_ORDERS_PRIVATE_IP_ARR

    nowPage =1
    emptyReq =False
    while  not emptyReq:
        client =  AcsClient('LTAI5tDkjyCAYHGHAadbVxtv', 'onGH2W2avi114HaCmeQjffy9i6IJTr','ap-northeast-1')
        client.add_endpoint('ap-northeast-1','Ecs',"ecs.ap-northeast-1.aliyuncs.com")
        request = DescribeInstancesRequest()
        request.set_PageNumber(nowPage)
        request.set_PageSize(100)
        request.set_accept_format('json')
        # request.modify_point('cn-hongkong','ecs',"ecs.cn-hongkong.aliyuncs.com")
        # request.set_Endpoint("ecs.cn-hongkong.aliyuncs.com")
        instanceInfoArr = client.do_action_with_exception(request)
        instanceInfoArr=json.loads(str(instanceInfoArr, encoding='utf-8'))

        instanceInfoArr=instanceInfoArr["Instances"]["Instance"]
        if len(instanceInfoArr)==0:
            emptyReq=True
        else:
            for i in range(len(instanceInfoArr)):
                if instanceInfoArr[i]["InstanceName"].find("makerStopLoss")>=0:
                    print(instanceInfoArr[i])
                    MAKER_STOP_LOSS_PRIVATE_IP_ARR.append(instanceInfoArr[i]["VpcAttributes"]["PrivateIpAddress"]["IpAddress"][0])
                if instanceInfoArr[i]["InstanceName"].find("getBinancePosition")>=0:
                    print(instanceInfoArr[i])
                    GET_BINANCE_POSITION_PRIVATE_IP_ARR.append(instanceInfoArr[i]["VpcAttributes"]["PrivateIpAddress"]["IpAddress"][0])
                if instanceInfoArr[i]["InstanceName"].find("positionRisk")>=0:
                    print(instanceInfoArr[i])
                    POSITION_RISK_PRIVATE_IP_ARR.append(instanceInfoArr[i]["VpcAttributes"]["PrivateIpAddress"]["IpAddress"][0])
                if instanceInfoArr[i]["InstanceName"].find("commission")>=0:
                    print(instanceInfoArr[i])
                    COMMISSION_PRIVATE_IP_ARR.append(instanceInfoArr[i]["VpcAttributes"]["PrivateIpAddress"]["IpAddress"][0])
                if instanceInfoArr[i]["InstanceName"].find("checkTimeoutOrders")>=0:
                    print(instanceInfoArr[i])
                    CHECK_TIME_OUT_ORDERS_PRIVATE_IP_ARR.append(instanceInfoArr[i]["VpcAttributes"]["PrivateIpAddress"]["IpAddress"][0])
                if instanceInfoArr[i]["InstanceName"].find("webOssUpdate")>=0:
                    print(instanceInfoArr[i])
                    WEB_OSS_UPDATE_PRIVATE_IP_ARR.append(instanceInfoArr[i]["VpcAttributes"]["PrivateIpAddress"]["IpAddress"][0])
                if instanceInfoArr[i]["InstanceName"].find("wsPosition")>=0:
                    print(instanceInfoArr[i])
                    WS_POSITION_PRIVATE_IP_ARR.append(instanceInfoArr[i]["VpcAttributes"]["PrivateIpAddress"]["IpAddress"][0])
                if instanceInfoArr[i]["InstanceName"].find("tradesUpdate")>=0:
                    print(instanceInfoArr[i])
                    TRADES_UPDATE_PRIVATE_IP_ARR.append(instanceInfoArr[i]["VpcAttributes"]["PrivateIpAddress"]["IpAddress"][0])
                if instanceInfoArr[i]["InstanceName"].find("binanceRecord")>=0:
                    print(instanceInfoArr[i])
                    BINANCE_RECORD_PRIVATE_IP_ARR.append(instanceInfoArr[i]["VpcAttributes"]["PrivateIpAddress"]["IpAddress"][0])
        nowPage = nowPage+1


getServerInfo()


useIPARR = BINANCE_RECORD_PRIVATE_IP_ARR
user_name = "root"
password = "Caijiali520!"
exptionIPArr= []

fileName =  ["binanceOrdersRecord","binanceTradesRecord"]



for a in range(len(useIPARR)):
    print("useIP:"+str(useIPARR[a]))
    transport = paramiko.Transport((useIPARR[a], 22))
    transport.connect(username='root', password="Caijiali520!")
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put('./config.py', '/root/config.py')

    transport = paramiko.Transport((useIPARR[a], 22))
    transport.connect(username='root', password="Caijiali520!")
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put('./commonFunction.py', '/root/commonFunction.py')

    for b in range(len(fileName)):
        print("fileName:"+str(fileName[b]))
        transport = paramiko.Transport((useIPARR[a], 22))
        transport.connect(username='root', password="Caijiali520!")
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put('./'+fileName[b]+'.py', '/root/'+fileName[b]+'.py')

        normalRun = False
        while not normalRun:
            try:
                commandArr = [
                    "ps -efwwww |grep  "+fileName[b]+".py | awk '{print $2}' | xargs kill -9",
                    "dos2unix  "+fileName[b]+".py",
                    "chmod +x  "+fileName[b]+".py",
                    "nohup  ./"+fileName[b]+".py >/dev/null &"
                ]
                host_ip = useIPARR[a]
                ssh = paramiko.SSHClient()   #创建sshclient
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  #指定当对方主机没有本机公钥的情况时应该怎么办，AutoAddPolicy表示自动在对方主机保存下本机的秘钥
                ssh.connect(host_ip, 22, user_name, password)

                for k in range(len(commandArr)):
                    stdin, stdout, stderr = ssh.exec_command(commandArr[k])
                    time.sleep(0.5)

                stdin, stdout, stderr = ssh.exec_command("ps -e wwww")

                result=str(stdout.read().decode())

                thisSearchStr =  fileName[b]
                startCount = result.count(thisSearchStr,0,len(result))
                if  startCount==1:
                    normalRun= True
                    stdin, stdout, stderr = ssh.exec_command("shred -zvu -n 5 makerStopLoss.py")
                    print("run")
                else:
                    print("not run")

                ssh.close()
            except Exception as e:
                print(e)


useIPARR = MAKER_STOP_LOSS_PRIVATE_IP_ARR
user_name = "root"
password = "Caijiali520!"
exptionIPArr= []

fileName =  ["makerStopLoss"]



for a in range(len(useIPARR)):
    print("useIP:"+str(useIPARR[a]))
    transport = paramiko.Transport((useIPARR[a], 22))
    transport.connect(username='root', password="Caijiali520!")
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put('./config.py', '/root/config.py')

    transport = paramiko.Transport((useIPARR[a], 22))
    transport.connect(username='root', password="Caijiali520!")
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put('./commonFunction.py', '/root/commonFunction.py')

    for b in range(len(fileName)):
        print("fileName:"+str(fileName[b]))
        transport = paramiko.Transport((useIPARR[a], 22))
        transport.connect(username='root', password="Caijiali520!")
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put('./'+fileName[b]+'.py', '/root/'+fileName[b]+'.py')

        normalRun = False
        while not normalRun:
            try:
                commandArr = [
                    "ps -efwwww |grep  "+fileName[b]+".py | awk '{print $2}' | xargs kill -9",
                    "dos2unix  "+fileName[b]+".py",
                    "chmod +x  "+fileName[b]+".py",
                    "nohup  ./"+fileName[b]+".py >/dev/null &"
                ]
                host_ip = useIPARR[a]
                ssh = paramiko.SSHClient()   #创建sshclient
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  #指定当对方主机没有本机公钥的情况时应该怎么办，AutoAddPolicy表示自动在对方主机保存下本机的秘钥
                ssh.connect(host_ip, 22, user_name, password)

                for k in range(len(commandArr)):
                    stdin, stdout, stderr = ssh.exec_command(commandArr[k])
                    time.sleep(0.5)

                stdin, stdout, stderr = ssh.exec_command("ps -e wwww")

                result=str(stdout.read().decode())

                thisSearchStr =  fileName[b]
                startCount = result.count(thisSearchStr,0,len(result))
                if  startCount==1:
                    normalRun= True
                    stdin, stdout, stderr = ssh.exec_command("shred -zvu -n 5 makerStopLoss.py")
                    print("run")
                else:
                    print("not run")

                ssh.close()
            except Exception as e:
                print(e)



useIPARR = GET_BINANCE_POSITION_PRIVATE_IP_ARR
user_name = "root"
password = "Caijiali520!"
exptionIPArr= []

fileName =  ["getBinancePosition"]

for a in range(len(useIPARR)):
    print("useIP:"+str(useIPARR[a]))
    transport = paramiko.Transport((useIPARR[a], 22))
    transport.connect(username='root', password="Caijiali520!")
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put('./config.py', '/root/config.py')

    transport = paramiko.Transport((useIPARR[a], 22))
    transport.connect(username='root', password="Caijiali520!")
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put('./commonFunction.py', '/root/commonFunction.py')

    for b in range(len(fileName)):
        print("fileName:"+str(fileName[b]))
        transport = paramiko.Transport((useIPARR[a], 22))
        transport.connect(username='root', password="Caijiali520!")
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put('./'+fileName[b]+'.py', '/root/'+fileName[b]+'.py')

        normalRun = False
        while not normalRun:
            try:
                commandArr = [
                    "ps -efwwww |grep  "+fileName[b]+".py | awk '{print $2}' | xargs kill -9",
                    "dos2unix  "+fileName[b]+".py",
                    "chmod +x  "+fileName[b]+".py",
                    "nohup  ./"+fileName[b]+".py >/dev/null &"
                ]
                host_ip = useIPARR[a]
                ssh = paramiko.SSHClient()   #创建sshclient
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  #指定当对方主机没有本机公钥的情况时应该怎么办，AutoAddPolicy表示自动在对方主机保存下本机的秘钥
                ssh.connect(host_ip, 22, user_name, password)

                for k in range(len(commandArr)):
                    stdin, stdout, stderr = ssh.exec_command(commandArr[k])
                    time.sleep(0.5)

                stdin, stdout, stderr = ssh.exec_command("ps -e wwww")

                result=str(stdout.read().decode())

                thisSearchStr =  fileName[b]
                startCount = result.count(thisSearchStr,0,len(result))
                if  startCount==1:
                    normalRun= True
                    stdin, stdout, stderr = ssh.exec_command("shred -zvu -n 5 getBinancePosition.py")
                    print("run")
                else:
                    print("not run")

                ssh.close()
            except Exception as e:
                print(e)



useIPARR = POSITION_RISK_PRIVATE_IP_ARR
# useIPARR = ["47.243.89.240","8.210.218.167"]
user_name = "root"
password = "Caijiali520!"
exptionIPArr= []

fileName =  ["positionRisk"]



for a in range(len(useIPARR)):
    print("useIP:"+str(useIPARR[a]))
    transport = paramiko.Transport((useIPARR[a], 22))
    transport.connect(username='root', password="Caijiali520!")
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put('./config.py', '/root/config.py')

    transport = paramiko.Transport((useIPARR[a], 22))
    transport.connect(username='root', password="Caijiali520!")
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put('./commonFunction.py', '/root/commonFunction.py')

    for b in range(len(fileName)):
        print("fileName:"+str(fileName[b]))
        transport = paramiko.Transport((useIPARR[a], 22))
        transport.connect(username='root', password="Caijiali520!")
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put('./'+fileName[b]+'.py', '/root/'+fileName[b]+'.py')

        normalRun = False
        while not normalRun:
            try:
                commandArr = [
                    "ps -efwwww |grep  "+fileName[b]+".py | awk '{print $2}' | xargs kill -9",
                    "dos2unix  "+fileName[b]+".py",
                    "chmod +x  "+fileName[b]+".py",
                    "nohup  ./"+fileName[b]+".py >/dev/null &"
                ]
                host_ip = useIPARR[a]
                ssh = paramiko.SSHClient()   #创建sshclient
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  #指定当对方主机没有本机公钥的情况时应该怎么办，AutoAddPolicy表示自动在对方主机保存下本机的秘钥
                ssh.connect(host_ip, 22, user_name, password)

                for k in range(len(commandArr)):
                    stdin, stdout, stderr = ssh.exec_command(commandArr[k])
                    time.sleep(0.5)

                stdin, stdout, stderr = ssh.exec_command("ps -e wwww")

                result=str(stdout.read().decode())

                thisSearchStr =  fileName[b]
                startCount = result.count(thisSearchStr,0,len(result))
                if  startCount==1:
                    normalRun= True
                    stdin, stdout, stderr = ssh.exec_command("shred -zvu -n 5 positionRisk.py")
                    print("run")
                else:
                    print("not run")

                ssh.close()
            except Exception as e:
                print(e)

useIPARR = COMMISSION_PRIVATE_IP_ARR
# useIPARR = ["47.243.89.240","8.210.218.167"]
user_name = "root"
password = "Caijiali520!"
exptionIPArr= []

fileName =  ["commission"]



for a in range(len(useIPARR)):
    print("useIP:"+str(useIPARR[a]))
    transport = paramiko.Transport((useIPARR[a], 22))
    transport.connect(username='root', password="Caijiali520!")
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put('./config.py', '/root/config.py')

    transport = paramiko.Transport((useIPARR[a], 22))
    transport.connect(username='root', password="Caijiali520!")
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put('./commonFunction.py', '/root/commonFunction.py')

    for b in range(len(fileName)):
        print("fileName:"+str(fileName[b]))
        transport = paramiko.Transport((useIPARR[a], 22))
        transport.connect(username='root', password="Caijiali520!")
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put('./'+fileName[b]+'.py', '/root/'+fileName[b]+'.py')

        normalRun = False
        while not normalRun:
            try:
                commandArr = [
                    "ps -efwwww |grep  "+fileName[b]+".py | awk '{print $2}' | xargs kill -9",
                    "dos2unix  "+fileName[b]+".py",
                    "chmod +x  "+fileName[b]+".py",
                    "nohup  ./"+fileName[b]+".py >/dev/null &"
                ]
                host_ip = useIPARR[a]
                ssh = paramiko.SSHClient()   #创建sshclient
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  #指定当对方主机没有本机公钥的情况时应该怎么办，AutoAddPolicy表示自动在对方主机保存下本机的秘钥
                ssh.connect(host_ip, 22, user_name, password)

                for k in range(len(commandArr)):
                    stdin, stdout, stderr = ssh.exec_command(commandArr[k])
                    time.sleep(0.5)

                stdin, stdout, stderr = ssh.exec_command("ps -e wwww")

                result=str(stdout.read().decode())

                thisSearchStr =  fileName[b]
                startCount = result.count(thisSearchStr,0,len(result))
                if  startCount==1:
                    normalRun= True
                    stdin, stdout, stderr = ssh.exec_command("shred -zvu -n 5 positionRisk.py")
                    print("run")
                else:
                    print("not run")

                ssh.close()
            except Exception as e:
                print(e)


useIPARR = WEB_OSS_UPDATE_PRIVATE_IP_ARR
# useIPARR = ["47.243.89.240","8.210.218.167"]
user_name = "root"
password = "Caijiali520!"
exptionIPArr= []

fileName =  ["webOssUpdate"]



for a in range(len(useIPARR)):
    print("useIP:"+str(useIPARR[a]))
    transport = paramiko.Transport((useIPARR[a], 22))
    transport.connect(username='root', password="Caijiali520!")
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put('./config.py', '/root/config.py')

    transport = paramiko.Transport((useIPARR[a], 22))
    transport.connect(username='root', password="Caijiali520!")
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put('./commonFunction.py', '/root/commonFunction.py')

    for b in range(len(fileName)):
        print("fileName:"+str(fileName[b]))
        transport = paramiko.Transport((useIPARR[a], 22))
        transport.connect(username='root', password="Caijiali520!")
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put('./'+fileName[b]+'.py', '/root/'+fileName[b]+'.py')

        normalRun = False
        while not normalRun:
            try:
                commandArr = [
                    "ps -efwwww |grep  "+fileName[b]+".py | awk '{print $2}' | xargs kill -9",
                    "dos2unix  "+fileName[b]+".py",
                    "chmod +x  "+fileName[b]+".py",
                    "nohup  ./"+fileName[b]+".py >/dev/null &"
                ]
                host_ip = useIPARR[a]
                ssh = paramiko.SSHClient()   #创建sshclient
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  #指定当对方主机没有本机公钥的情况时应该怎么办，AutoAddPolicy表示自动在对方主机保存下本机的秘钥
                ssh.connect(host_ip, 22, user_name, password)

                for k in range(len(commandArr)):
                    stdin, stdout, stderr = ssh.exec_command(commandArr[k])
                    time.sleep(0.5)

                stdin, stdout, stderr = ssh.exec_command("ps -e wwww")

                result=str(stdout.read().decode())

                thisSearchStr =  fileName[b]
                startCount = result.count(thisSearchStr,0,len(result))
                if  startCount==1:
                    normalRun= True
                    stdin, stdout, stderr = ssh.exec_command("shred -zvu -n 5 positionRisk.py")
                    print("run")
                else:
                    print("not run")

                ssh.close()
            except Exception as e:
                print(e)




useIPARR = CHECK_TIME_OUT_ORDERS_PRIVATE_IP_ARR
# useIPARR = ["47.243.89.240","8.210.218.167"]
user_name = "root"
password = "Caijiali520!"
exptionIPArr= []

fileName =  ["checkTimeoutOrders"]



for a in range(len(useIPARR)):
    print("useIP:"+str(useIPARR[a]))
    transport = paramiko.Transport((useIPARR[a], 22))
    transport.connect(username='root', password="Caijiali520!")
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put('./config.py', '/root/config.py')

    transport = paramiko.Transport((useIPARR[a], 22))
    transport.connect(username='root', password="Caijiali520!")
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put('./commonFunction.py', '/root/commonFunction.py')

    for b in range(len(fileName)):
        print("fileName:"+str(fileName[b]))
        transport = paramiko.Transport((useIPARR[a], 22))
        transport.connect(username='root', password="Caijiali520!")
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put('./'+fileName[b]+'.py', '/root/'+fileName[b]+'.py')

        normalRun = False
        while not normalRun:
            try:
                commandArr = [
                    "ps -efwwww |grep  "+fileName[b]+".py | awk '{print $2}' | xargs kill -9",
                    "dos2unix  "+fileName[b]+".py",
                    "chmod +x  "+fileName[b]+".py",
                    "nohup  ./"+fileName[b]+".py >/dev/null &"
                ]
                host_ip = useIPARR[a]
                ssh = paramiko.SSHClient()   #创建sshclient
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  #指定当对方主机没有本机公钥的情况时应该怎么办，AutoAddPolicy表示自动在对方主机保存下本机的秘钥
                ssh.connect(host_ip, 22, user_name, password)

                for k in range(len(commandArr)):
                    stdin, stdout, stderr = ssh.exec_command(commandArr[k])
                    time.sleep(0.5)

                stdin, stdout, stderr = ssh.exec_command("ps -e wwww")

                result=str(stdout.read().decode())

                thisSearchStr =  fileName[b]
                startCount = result.count(thisSearchStr,0,len(result))
                if  startCount==1:
                    normalRun= True
                    stdin, stdout, stderr = ssh.exec_command("shred -zvu -n 5 positionRisk.py")
                    print("run")
                else:
                    print("not run")

                ssh.close()
            except Exception as e:
                print(e)


useIPARR = TRADES_UPDATE_PRIVATE_IP_ARR
# useIPARR = ["47.243.89.240","8.210.218.167"]
user_name = "root"
password = "Caijiali520!"
exptionIPArr= []

fileName =  ["tradesUpdate"]



for a in range(len(useIPARR)):
    print("useIP:"+str(useIPARR[a]))
    transport = paramiko.Transport((useIPARR[a], 22))
    transport.connect(username='root', password="Caijiali520!")
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put('./config.py', '/root/config.py')

    transport = paramiko.Transport((useIPARR[a], 22))
    transport.connect(username='root', password="Caijiali520!")
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put('./commonFunction.py', '/root/commonFunction.py')

    for b in range(len(fileName)):
        print("fileName:"+str(fileName[b]))
        transport = paramiko.Transport((useIPARR[a], 22))
        transport.connect(username='root', password="Caijiali520!")
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put('./'+fileName[b]+'.py', '/root/'+fileName[b]+'.py')

        normalRun = False
        while not normalRun:
            try:
                commandArr = [
                    "ps -efwwww |grep  "+fileName[b]+".py | awk '{print $2}' | xargs kill -9",
                    "dos2unix  "+fileName[b]+".py",
                    "chmod +x  "+fileName[b]+".py",
                    "nohup  ./"+fileName[b]+".py >/dev/null &"
                ]
                host_ip = useIPARR[a]
                ssh = paramiko.SSHClient()   #创建sshclient
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  #指定当对方主机没有本机公钥的情况时应该怎么办，AutoAddPolicy表示自动在对方主机保存下本机的秘钥
                ssh.connect(host_ip, 22, user_name, password)

                for k in range(len(commandArr)):
                    stdin, stdout, stderr = ssh.exec_command(commandArr[k])
                    time.sleep(0.5)

                stdin, stdout, stderr = ssh.exec_command("ps -e wwww")

                result=str(stdout.read().decode())

                thisSearchStr =  fileName[b]
                startCount = result.count(thisSearchStr,0,len(result))
                if  startCount==1:
                    normalRun= True
                    stdin, stdout, stderr = ssh.exec_command("shred -zvu -n 5 positionRisk.py")
                    print("run")
                else:
                    print("not run")

                ssh.close()
            except Exception as e:
                print(e)

useIPARR = WS_POSITION_PRIVATE_IP_ARR
# useIPARR = ["47.243.89.240","8.210.218.167"]
user_name = "root"
password = "Caijiali520!"
exptionIPArr= []

fileName =  ["wsPosition"]



for a in range(len(useIPARR)):
    print("useIP:"+str(useIPARR[a]))
    transport = paramiko.Transport((useIPARR[a], 22))
    transport.connect(username='root', password="Caijiali520!")
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put('./config.py', '/root/config.py')

    transport = paramiko.Transport((useIPARR[a], 22))
    transport.connect(username='root', password="Caijiali520!")
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put('./commonFunction.py', '/root/commonFunction.py')

    for b in range(len(fileName)):
        print("fileName:"+str(fileName[b]))
        transport = paramiko.Transport((useIPARR[a], 22))
        transport.connect(username='root', password="Caijiali520!")
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put('./'+fileName[b]+'.py', '/root/'+fileName[b]+'.py')

        normalRun = False
        while not normalRun:
            try:
                commandArr = [
                    "ps -efwwww |grep  "+fileName[b]+".py | awk '{print $2}' | xargs kill -9",
                    "dos2unix  "+fileName[b]+".py",
                    "chmod +x  "+fileName[b]+".py",
                    "nohup  ./"+fileName[b]+".py >/dev/null &"
                ]
                host_ip = useIPARR[a]
                ssh = paramiko.SSHClient()   #创建sshclient
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  #指定当对方主机没有本机公钥的情况时应该怎么办，AutoAddPolicy表示自动在对方主机保存下本机的秘钥
                ssh.connect(host_ip, 22, user_name, password)

                for k in range(len(commandArr)):
                    stdin, stdout, stderr = ssh.exec_command(commandArr[k])
                    time.sleep(0.5)

                stdin, stdout, stderr = ssh.exec_command("ps -e wwww")

                result=str(stdout.read().decode())

                thisSearchStr =  fileName[b]
                startCount = result.count(thisSearchStr,0,len(result))
                if  startCount==1:
                    normalRun= True
                    stdin, stdout, stderr = ssh.exec_command("shred -zvu -n 5 wsPosition.py")
                    print("run")
                else:
                    print("not run")

                ssh.close()
            except Exception as e:
                print(e)


os.system("shred -zvu -n 5 makerStopLoss.py")

os.system("shred -zvu -n 5 getBinancePosition.py")

os.system("shred -zvu -n 5 positionRisk.py")

os.system("shred -zvu -n 5 commission.py")

os.system("shred -zvu -n 5 checkTimeoutOrders.py")

os.system("shred -zvu -n 5 webOssUpdate.py")

os.system("shred -zvu -n 5 wsPosition.py")

os.system("shred -zvu -n 5 tradesUpdate.py")
