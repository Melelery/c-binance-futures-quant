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

FUNCTION_CLIENT = FunctionClient(larkMsgSymbol="uploadDataPy")

TICK_PRIVATE_IP_ARR = get_aliyun_private_ip_arr_by_name("tickToWs")

ONE_MIN_PRIVATE_IP_ARR = get_aliyun_private_ip_arr_by_name("oneMinKlineToWs_")

SPECIAL_ONE_MIN_PRIVATE_IP_ARR = get_aliyun_private_ip_arr_by_name("specialOneMinKlineToWs_")



useIPARR = TICK_PRIVATE_IP_ARR
user_name = ""
password = ""
exptionIPArr= []

fileName =  ["tickToWs"]



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
                    time.sleep(0.1)
                ssh.close()
                # except Exception as e:
                #     print(e)
                #     exptionIPArr.append(useIPARR[a])

                # try:

                ssh = paramiko.SSHClient()   #创建sshclient
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  #指定当对方主机没有本机公钥的情况时应该怎么办，AutoAddPolicy表示自动在对方主机保存下本机的秘钥
                ssh.connect(useIPARR[a], 22, user_name, password)
                stdin, stdout, stderr = ssh.exec_command("ps -e wwww")

                result=str(stdout.read().decode())

                thisSearchStr =  fileName[b]
                startCount = result.count(thisSearchStr,0,len(result))
                if  startCount==1:
                    normalRun= True
                    print("run")
                else:
                    print("not run")

                ssh.close()
            except Exception as e:
                print(e)



useIPARR = ONE_MIN_PRIVATE_IP_ARR
user_name = ""
password = ""
exptionIPArr= []

fileName =  ["oneMinKlineToWs"]

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
                    time.sleep(0.1)
                ssh.close()
                # except Exception as e:
                #     print(e)
                #     exptionIPArr.append(useIPARR[a])

                # try:

                ssh = paramiko.SSHClient()   #创建sshclient
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  #指定当对方主机没有本机公钥的情况时应该怎么办，AutoAddPolicy表示自动在对方主机保存下本机的秘钥
                ssh.connect(useIPARR[a], 22, user_name, password)
                stdin, stdout, stderr = ssh.exec_command("ps -e wwww")

                result=str(stdout.read().decode())

                thisSearchStr =  fileName[b]
                startCount = result.count(thisSearchStr,0,len(result))
                if  startCount==1:
                    normalRun= True
                    print("run")
                else:
                    print("not run")

                ssh.close()
            except Exception as e:
                print(e)





useIPARR = SPECIAL_ONE_MIN_PRIVATE_IP_ARR
user_name = ""
password = ""
exptionIPArr= []

fileName =  ["specialOneMinKlineToWs"]

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
                ssh.close()
                # except Exception as e:
                #     print(e)
                #     exptionIPArr.append(useIPARR[a])

                # try:

                ssh = paramiko.SSHClient()   #创建sshclient
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  #指定当对方主机没有本机公钥的情况时应该怎么办，AutoAddPolicy表示自动在对方主机保存下本机的秘钥
                ssh.connect(useIPARR[a], 22, user_name, password)
                stdin, stdout, stderr = ssh.exec_command("ps -e wwww")

                result=str(stdout.read().decode())

                thisSearchStr =  fileName[b]
                startCount = result.count(thisSearchStr,0,len(result))
                if  startCount==1:
                    normalRun= True
                    print("run")
                else:
                    print("not run")

                ssh.close()
            except Exception as e:
                print(e)
