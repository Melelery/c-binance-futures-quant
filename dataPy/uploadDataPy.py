#!/usr/bin/python3
# encoding:utf-8
import re
import urllib.request
import urllib
import os
import sys
import paramiko
import json
import time
from config import *
from commonFunction import FunctionClient

FUNCTION_CLIENT = FunctionClient(larkMsgSymbol="uploadDataPy")

TICK_PRIVATE_IP_ARR = FUNCTION_CLIENT.get_aliyun_private_ip_arr_by_name("tickToWs")

ONE_MIN_PRIVATE_IP_ARR = FUNCTION_CLIENT.get_aliyun_private_ip_arr_by_name("oneMinKlineToWs_")

SPECIAL_ONE_MIN_PRIVATE_IP_ARR = FUNCTION_CLIENT.get_aliyun_private_ip_arr_by_name("specialOneMinKlineToWs_")

IP_ARR = [TICK_PRIVATE_IP_ARR,ONE_MIN_PRIVATE_IP_ARR,SPECIAL_ONE_MIN_PRIVATE_IP_ARR]

FILE_NAME_ARR = [["tickToWs"],["oneMinKlineToWs"],["specialOneMinKlineToWs"]]

server_user_name = ""

server_password = ""

if len(IP_ARR)!=len(FILE_NAME_ARR):
    print("len(IP_ARR)!=len(FILE_NAME_ARR)")
    time.sleep(999999999)

for i in range(len(IP_ARR)):

    useIPArr = IP_ARR[i]

    fileNameArr =  FILE_NAME_ARR[i]

    for a in range(len(useIPArr)):
        print("useIP:"+str(useIPArr[a]))
        transport = paramiko.Transport((useIPArr[a], 22))
        transport.connect(username=server_user_name, password=server_password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put('./config.py', '/root/config.py')
        sftp.put('./commonFunction.py', '/root/commonFunction.py')

        for b in range(len(fileNameArr)):
            print("fileName:"+str(fileNameArr[b]))
            sftp.put('./'+fileNameArr[b]+'.py', '/root/'+fileNameArr[b]+'.py')

            normalRun = False
            while not normalRun:
                try:
                    commandArr = [
                        "ps -efwwww |grep  "+fileNameArr[b]+".py | awk '{print $2}' | xargs kill -9",
                        "dos2unix  "+fileNameArr[b]+".py",
                        "chmod +x  "+fileNameArr[b]+".py",
                        "nohup  ./"+fileNameArr[b]+".py >/dev/null &"
                    ]
                    host_ip = useIPArr[a]
                    ssh = paramiko.SSHClient()   
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
                    ssh.connect(host_ip, 22, server_user_name, server_password)

                    for k in range(len(commandArr)):
                        stdin, stdout, stderr = ssh.exec_command(commandArr[k])
                        time.sleep(0.1)

                    time.sleep(3)

                    stdin, stdout, stderr = ssh.exec_command("ps -e wwww")

                    result=str(stdout.read().decode())

                    thisSearchStr =  fileNameArr[b]
                    startCount = result.count(thisSearchStr,0,len(result))
                    if  startCount==1:
                        normalRun= True
                        stdin, stdout, stderr = ssh.exec_command("shred -zvu -n 5 "+fileNameArr[b]+".py")
                        print("run")
                    else:
                        print("not run")

                    ssh.close()
                except Exception as e:
                    print(e)
        sftp.close()

for a in range(len(FILE_NAME_ARR)):
    for b in range(len(FILE_NAME_ARR[a])):
        print(FILE_NAME_ARR[a])
        print(FILE_NAME_ARR[a][b])
        try:
            (status, output) = os.system("shred -zvu -n 5 "+FILE_NAME_ARR[a][b]+".py")
        except Exception as e:
            print(e)