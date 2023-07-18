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


TICK_PRIVATE_IP_ARR = []

ONE_MIN_PRIVATE_IP_ARR = []

SPECIAL_ONE_MIN_PRIVATE_IP_ARR = []

FIFTEEN_MINS_PRIVATE_IP_ARR = []

OTHER_PRIVATE_IP_ARR = []


def getServerInfo():
    global TICK_PRIVATE_IP_ARR,ONE_MIN_PRIVATE_IP_ARR,FIFTEEN_MINS_PRIVATE_IP_ARR,OTHER_PRIVATE_IP_ARR,SPECIAL_ONE_MIN_PRIVATE_IP_ARR

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
                if instanceInfoArr[i]["InstanceName"].find("tickToWs")>=0:
                    print(instanceInfoArr[i])
                    TICK_PRIVATE_IP_ARR.append(instanceInfoArr[i]["VpcAttributes"]["PrivateIpAddress"]["IpAddress"][0])
                if instanceInfoArr[i]["InstanceName"].find("oneMinKlineToWs_")>=0:
                    print(instanceInfoArr[i])
                    ONE_MIN_PRIVATE_IP_ARR.append(instanceInfoArr[i]["VpcAttributes"]["PrivateIpAddress"]["IpAddress"][0])
                if instanceInfoArr[i]["InstanceName"].find("specialOneMinKlineToWs_")>=0:
                    print(instanceInfoArr[i])
                    SPECIAL_ONE_MIN_PRIVATE_IP_ARR.append(instanceInfoArr[i]["VpcAttributes"]["PrivateIpAddress"]["IpAddress"][0])


                # if instanceInfoArr[i]["InstanceName"].find("fifteenMinsKlineToWs")>=0:
                #     print(instanceInfoArr[i])
                #     FIFTEEN_MINS_PRIVATE_IP_ARR.append(instanceInfoArr[i]["VpcAttributes"]["PrivateIpAddress"]["IpAddress"][0])
                # if instanceInfoArr[i]["InstanceName"].find("otherKlineToWs")>=0:
                #     print(instanceInfoArr[i])
                #     OTHER_PRIVATE_IP_ARR.append(instanceInfoArr[i]["VpcAttributes"]["PrivateIpAddress"]["IpAddress"][0])

        nowPage = nowPage+1


getServerInfo()

useIPARR = TICK_PRIVATE_IP_ARR
user_name = "root"
password = "Caijiali520!"
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
user_name = "root"
password = "Caijiali520!"
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
user_name = "root"
password = "Caijiali520!"
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

# useIPARR = FIFTEEN_MINS_PRIVATE_IP_ARR
# # useIPARR = ["47.243.89.240","8.210.218.167"]
# user_name = "root"
# password = "Caijiali520!"
# exptionIPArr= []

# fileName =  ["fifteenMinsKlineToWs"]



# for a in range(len(useIPARR)):
#     print("useIP:"+str(useIPARR[a]))
#     transport = paramiko.Transport((useIPARR[a], 22))
#     transport.connect(username='root', password="Caijiali520!")
#     sftp = paramiko.SFTPClient.from_transport(transport)
#     sftp.put('./config.py', '/root/config.py')

#     transport = paramiko.Transport((useIPARR[a], 22))
#     transport.connect(username='root', password="Caijiali520!")
#     sftp = paramiko.SFTPClient.from_transport(transport)
#     sftp.put('./commonFunction.py', '/root/commonFunction.py')

#     for b in range(len(fileName)):
#         print("fileName:"+str(fileName[b]))
#         transport = paramiko.Transport((useIPARR[a], 22))
#         transport.connect(username='root', password="Caijiali520!")
#         sftp = paramiko.SFTPClient.from_transport(transport)
#         sftp.put('./'+fileName[b]+'.py', '/root/'+fileName[b]+'.py')

#         normalRun = False
#         while not normalRun:
#             try:
#                 commandArr = [
#                     "ps -efwwww |grep  "+fileName[b]+".py | awk '{print $2}' | xargs kill -9",
#                     "dos2unix  "+fileName[b]+".py",
#                     "chmod +x  "+fileName[b]+".py",
#                     "nohup  ./"+fileName[b]+".py >/dev/null &"
#                 ]
#                 host_ip = useIPARR[a]
#                 ssh = paramiko.SSHClient()   #创建sshclient
#                 ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  #指定当对方主机没有本机公钥的情况时应该怎么办，AutoAddPolicy表示自动在对方主机保存下本机的秘钥
#                 ssh.connect(host_ip, 22, user_name, password)

#                 for k in range(len(commandArr)):
#                     stdin, stdout, stderr = ssh.exec_command(commandArr[k])
#                     time.sleep(0.1)
#                 ssh.close()
#                 # except Exception as e:
#                 #     print(e)
#                 #     exptionIPArr.append(useIPARR[a])

#                 # try:

#                 ssh = paramiko.SSHClient()   #创建sshclient
#                 ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  #指定当对方主机没有本机公钥的情况时应该怎么办，AutoAddPolicy表示自动在对方主机保存下本机的秘钥
#                 ssh.connect(useIPARR[a], 22, user_name, password)
#                 stdin, stdout, stderr = ssh.exec_command("ps -e wwww")

#                 result=str(stdout.read().decode())

#                 thisSearchStr =  fileName[b]
#                 startCount = result.count(thisSearchStr,0,len(result))
#                 if  startCount==1:
#                     normalRun= True
#                     print("run")
#                 else:
#                     print("not run")

#                 ssh.close()
#             except Exception as e:
#                 print(e)


# useIPARR = OTHER_PRIVATE_IP_ARR
# # useIPARR = ["47.243.89.240","8.210.218.167"]
# user_name = "root"
# password = "Caijiali520!"
# exptionIPArr= []

# fileName =  ["otherKlineToWs"]



# for a in range(len(useIPARR)):
#     print("useIP:"+str(useIPARR[a]))
#     transport = paramiko.Transport((useIPARR[a], 22))
#     transport.connect(username='root', password="Caijiali520!")
#     sftp = paramiko.SFTPClient.from_transport(transport)
#     sftp.put('./config.py', '/root/config.py')

#     transport = paramiko.Transport((useIPARR[a], 22))
#     transport.connect(username='root', password="Caijiali520!")
#     sftp = paramiko.SFTPClient.from_transport(transport)
#     sftp.put('./commonFunction.py', '/root/commonFunction.py')

#     for b in range(len(fileName)):
#         print("fileName:"+str(fileName[b]))
#         transport = paramiko.Transport((useIPARR[a], 22))
#         transport.connect(username='root', password="Caijiali520!")
#         sftp = paramiko.SFTPClient.from_transport(transport)
#         sftp.put('./'+fileName[b]+'.py', '/root/'+fileName[b]+'.py')

#         normalRun = False
#         while not normalRun:
#             try:
#                 commandArr = [
#                     "ps -efwwww |grep  "+fileName[b]+".py | awk '{print $2}' | xargs kill -9",
#                     "dos2unix  "+fileName[b]+".py",
#                     "chmod +x  "+fileName[b]+".py",
#                     "nohup  ./"+fileName[b]+".py >/dev/null &"
#                 ]
#                 host_ip = useIPARR[a]
#                 ssh = paramiko.SSHClient()   #创建sshclient
#                 ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  #指定当对方主机没有本机公钥的情况时应该怎么办，AutoAddPolicy表示自动在对方主机保存下本机的秘钥
#                 ssh.connect(host_ip, 22, user_name, password)

#                 for k in range(len(commandArr)):
#                     stdin, stdout, stderr = ssh.exec_command(commandArr[k])
#                     time.sleep(0.1)
#                 ssh.close()
#                 # except Exception as e:
#                 #     print(e)
#                 #     exptionIPArr.append(useIPARR[a])

#                 # try:

#                 ssh = paramiko.SSHClient()   #创建sshclient
#                 ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  #指定当对方主机没有本机公钥的情况时应该怎么办，AutoAddPolicy表示自动在对方主机保存下本机的秘钥
#                 ssh.connect(useIPARR[a], 22, user_name, password)
#                 stdin, stdout, stderr = ssh.exec_command("ps -e wwww")

#                 result=str(stdout.read().decode())

#                 thisSearchStr =  fileName[b]
#                 startCount = result.count(thisSearchStr,0,len(result))
#                 if  startCount==1:
#                     normalRun= True
#                     print("run")
#                 else:
#                     print("not run")

#                 ssh.close()
#             except Exception as e:
#                 print(e)
