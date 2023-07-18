import mysql.connector
import socket
import json
import requests
import time
import oss2
from websocket import create_connection
from config import *
from mysql.connector.pooling import MySQLConnectionPool
from mysql.connector import connect
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest

class FunctionClient(object):
    def __init__(self, **params):
        """
        Create the request client instance.
        :param kwargs: The option of request connection.
            api_key: The public key applied from Binance.
            secret_key: The private key applied from Binance.
            server_url: The URL name like "https://api.binance.com".
        """
        self.larkMsgSymbol = ""

        if "larkMsgSymbol" in params:
            self.larkMsgSymbol = params["larkMsgSymbol"]

        self.larkAppID = FEISHU_APP_ID

        self.larkAppSecret = FEISHU_APP_SECRET

        self.mysqlConnect = {}
        if "connectMysql" in params and  params["connectMysql"]:
            self.mysqlConnect = mysql.connector.connect(**MYSQL_CONFIG)

        self.mysqlPoolConnect = {}
        if "connectMysqlPool" in params and  params["connectMysqlPool"]:
            self.mysqlPoolConnect = MySQLConnectionPool(pool_name = "mypool",pool_size = 30,**MYSQL_CONFIG)

        self.wsConnectionA = {}

        if "connectWsA" in params and  params["connectWsA"]:
            self.wsConnectionA = create_connection(WS_ADDRESS_A)



        self.wsConnectionB = {}

        if "connectWsB" in params and  params["connectWsB"]:
            self.wsConnectionB = create_connection(WS_ADDRESS_B)

        self.lastSendLarkTs = 0

        self.privateIP = self.get_private_ip()

        self.updateMachineStatusTs = 0

        oss_auth = oss2.Auth(ALIYUN_API_KEY, ALIYUN_API_SECRET)
        self.oss_bucket = oss2.Bucket(oss_auth, 'http://oss-cn-hongkong.aliyuncs.com', 'zuibite-api')

        self.serverName = self.getServerName()
    def send_lark_msg(self,content):
        global FEISHU_APP_ID,FEISHU_APP_SECRET
        try:
            header = {"Content-Type": "application/json"}

            body = {
                "app_id":self.larkAppID,
                "app_secret":self.larkAppSecret
            }
            url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"

            response = requests.request("POST", url, timeout=3, headers=header, data=json.dumps(body)).json()


            TEAM_ID = 'oc_d2fc6f3c0ff4d45811dfc774daec528c'
            url = "https://open.feishu.cn/open-apis/message/v4/send/"
            Authorization = "Bearer "+response['tenant_access_token']
            header = {"Authorization": Authorization,"Content-Type":"application/json"}

            sendText = "【"+self.larkMsgSymbol+"】"+content+"【"+self.privateIP+"】"

            body = {
                "chat_id":TEAM_ID,
                "msg_type":"text",
               "content":{
                    "text":sendText
                }
            }
            data = bytes(json.dumps(body), encoding='utf8')
            response = requests.request("POST", url, timeout=3, headers=header, data=data).json()

        except Exception as e:
            print(e)
            print("sendMsg")


    def send_lark_msg_limit_one_min(self,content):
        now = int(time.time())
        if now - self.lastSendLarkTs>60:
            self.lastSendLarkTs = now
            self.send_lark_msg(content)

    def turn_ts_to_time(self,initValue):
        if str(type(initValue))=="<class 'str'>":
            timeArray = time.strptime(initValue, "%Y-%m-%d %H:%M:%S")
            timestamp = time.mktime(timeArray)
            return timestamp
        else:
            if initValue>99999999999:
                initValue = int(initValue/1000)
            time_local = time.localtime(initValue)
            dt = time.strftime("%Y-%m-%d %H:%M:00",time_local)
            return dt

    def turn_ts_to_day_time(self,initValue):
        if str(type(initValue))=="<class 'str'>":
            timeArray = time.strptime(initValue, "%Y-%m-%d %H:%M:%S")
            timestamp = time.mktime(timeArray)
            return timestamp
        else:
            if initValue>99999999999:
                initValue = int(initValue/1000)
            time_local = time.localtime(initValue)
            dt = time.strftime("%Y-%m-%d 00:00:00",time_local)
            return dt

    def turn_ts_to_min(self,initValue):
        if initValue>99999999999:
            initValue = int(initValue/1000)
        time_local = time.localtime(initValue)
        dt = time.strftime("%M",time_local)
        return dt


    def generate_ts_with_min(self,min):
        now = int(time.time())
        time_local = time.localtime(now)
        dt = time.strftime("%Y-%m-%d %H:"+str(min)+":00",time_local)
        timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
        timestamp = int(time.mktime(timeArray))
        return timestamp


    def mysql_select(self,sql,params):
        res = ()
        normal = False
        try: 
           self.mysqlConnect.ping() 
        except Exception as e:      
           self.mysqlConnect=mysql.connector.connect(**MYSQL_CONFIG)
        while not normal:
            try:
                cursor=self.mysqlConnect.cursor()
                cursor.execute(sql,params)
                res = cursor.fetchall()
                normal = True
                cursor.close()
            except Exception as e:
                self.send_lark_msg("mysql ex,"+str(e))
                print("mysql error")
                print(sql)
                print(e)
                try: 
                   self.mysqlConnect.ping() 
                except Exception as e:      
                   self.mysqlConnect=mysql.connector.connect(**MYSQL_CONFIG)
                time.sleep(3)
        return res

    def mysql_commit(self,sql,params):
        normal = False
        try: 
           self.mysqlConnect.ping() 
        except Exception as e:      
           self.mysqlConnect=mysql.connector.connect(**MYSQL_CONFIG)
        while not normal:
            try:
                cursor=self.mysqlConnect.cursor()
                cursor.execute(sql,params)
                self.mysqlConnect.commit()
                normal = True
                cursor.close()
            except Exception as e:
                self.send_lark_msg("mysql ex,"+str(e))
                print("mysql error")
                print(sql)
                try: 
                   self.mysqlConnect.ping() 
                except Exception as e:      
                   self.mysqlConnect=mysql.connector.connect(**MYSQL_CONFIG)
                time.sleep(3)

    def mysql_pool_select(self,q,params):
        res = ()
        con = self.mysqlPoolConnect.get_connection()
        c = con.cursor()
        try:
            c.execute(q,params)
            res = c.fetchall()
            normal = True
        except Exception as e:
            print(e) 
            print(q) 
            print("doing error") 
            normal = False
        try:
            con.close()
        except Exception as e:
            print(q) 
            print(e) 
        return res

    def mysql_pool_commit(self,q,params):
        con = self.mysqlPoolConnect.get_connection()
        c = con.cursor()
        try:
            c.execute(q,params)
            con.commit()
            c.close()
            normal = True
        except Exception as e:
            self.send_lark_msg_limit_one_min(str(e))
            print(q) 
            print(e) 
            normal = False
        try:
            con.close()
        except Exception as e:
            print(q) 
            print(e) 
            
        return normal

    def get_private_ip(self):
        privateIP = ""
        try: 
            s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
            s.connect(('8.8.8.8',80)) 
            privateIP = s.getsockname()[0] 
        finally: 
            s.close()
        return privateIP


    def send_to_ws_a(self,msg):
        try:
            print(msg)
            self.wsConnectionA.send(msg);
        except Exception as e:
            print(e)
            try:
                self.wsConnectionA = create_connection(WS_ADDRESS_A)
                self.wsConnectionA.send(msg);
            except Exception as e:
                print(e)
                time.sleep(0.1)

    def get_from_ws_a(self,msg):
        result = {}
        try:
            self.wsConnectionA.send(msg);
            result =  self.wsConnectionA.recv()
            return result
        except Exception as e:
            print(e)
            try:
                self.wsConnectionA = create_connection(WS_ADDRESS_A)
                self.wsConnectionA.send(msg)
                result =  self.wsConnectionA.recv()
                return result
            except Exception as e:
                self.send_lark_msg_limit_one_min(str(e))

        return result


    def send_to_ws_b(self,msg):
        try:
            self.wsConnectionB.send(msg);
        except Exception as e:
            try:
                self.wsConnectionB = create_connection(WS_ADDRESS_B)
                self.wsConnectionB.send(msg);
            except Exception as e:
                time.sleep(0.1)

    def get_from_ws_b(self,msg):
        result = {}
        try:
            self.wsConnectionB.send(msg);
            result =  self.wsConnectionB.recv()
            return result
        except Exception as e:
            try:
                self.wsConnectionB = create_connection(WS_ADDRESS_B)
                self.wsConnectionB.send(msg)
                result =  self.wsConnectionB.recv()
                print(result)
                return result
            except Exception as e:
                print(e)
                self.send_lark_msg_limit_one_min(str(e))

        return result

    def get_aliyun_public_ip_arr_by_name(self,name):
        publicIPArr = []
        nowPage =1
        emptyReq =False
        while  not emptyReq:
            client =  AcsClient(ALIYUN_API_KEY, ALIYUN_API_SECRET,ALIYUN_POINT)
            client.add_endpoint(ALIYUN_POINT,'Ecs',"ecs."+ALIYUN_POINT+".aliyuncs.com")
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
                    if instanceInfoArr[i]["InstanceName"].find(name)>=0:
                        publicIPArr.append(instanceInfoArr[i]["PublicIpAddress"]["IpAddress"][0])

            nowPage = nowPage+1
        return publicIPArr



    def get_aliyun_private_ip_arr_by_name(self,name):
        privateIPArr = []
        nowPage =1
        emptyReq =False
        while  not emptyReq:
            client =  AcsClient(ALIYUN_API_KEY, ALIYUN_API_SECRET,ALIYUN_POINT)
            client.add_endpoint(ALIYUN_POINT,'Ecs',"ecs."+ALIYUN_POINT+".aliyuncs.com")
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
                    if instanceInfoArr[i]["InstanceName"].find(name)>=0:
                        privateIPArr.append(instanceInfoArr[i]["VpcAttributes"]["PrivateIpAddress"]["IpAddress"][0])

            nowPage = nowPage+1
        return privateIPArr


    def update_machine_status(self):
        now = int(time.time())
        if now - self.updateMachineStatusTs>60:
            self.updateMachineStatusTs = now
            try:
                url = "http://"+WEB_ADDRESS+":8888/update_machine_status"
                print(url)
                postDataObj = {'privateIP':self.privateIP,'symbol':self.larkMsgSymbol }
                response = requests.request("POST", url,timeout=(0.5,0.5),data=postDataObj)
            except Exception as e:
                print(e)

    def update_trade_status(self,status,runTime):
        try:
            url = "http://"+WEB_ADDRESS+":8888/update_trade_status"
            print(url)
            postDataObj = {'privateIP':self.privateIP,'status':status,"runTime":runTime}
            response = requests.request("POST", url,timeout=(0.5,0.5),data=postDataObj)
        except Exception as e:
            print(e)

    def cancel_binance_orders_by_web_server(self,symbol,key,secret):
        try:
            url = "http://"+WEB_ADDRESS+":8888/cancel_binance_orders"
            print(url)
            postDataObj = {'privateIP':self.privateIP,'symbol':symbol,'key':key,'secret':secret}
            response = requests.request("POST", url,timeout=(3,3),data=postDataObj)
            print(response)
        except Exception as e:
            print(e)

    def cancel_binance_order_by_web_server(self,symbol,key,secret,clientOrderId):
        try:
            url = "http://"+CANCEL_WEB_ADDRESS+":8888/cancel_binance_order"
            print(url)
            postDataObj = {'privateIP':self.privateIP,'symbol':symbol,'key':key,'secret':secret,'clientOrderId':clientOrderId}
            response = requests.request("POST", url,timeout=(3,3),data=postDataObj)
            print(response)
        except Exception as e:
            print(e)

    def open_take_binance_orders_by_web_server(self,symbol,direction,key,secret,price,openTime,positionValue,volMultiple):
        try:
            url = "http://172.24.207.1:8888/take_open"

            postDataObj = {'privateIP':self.privateIP,'volMultiple':volMultiple,'symbol':symbol,'direction':direction,'key':key,'secret':secret,'price':price,'openTime':openTime,'positionValue':positionValue}
            response = requests.request("POST", url,timeout=(3,3),data=postDataObj)
        except Exception as e:
            print(e)

    def end_open_by_web_server(self,symbol):
        try:
            url = "http://172.24.207.1:8888/end_open"

            postDataObj = {'privateIP':self.privateIP,'symbol':symbol}
            response = requests.request("POST", url,timeout=(3,3),data=postDataObj)
        except Exception as e:
            print(e)


    def get_percent_num(self,num, total):
        if total ==0:
            return 0
        else:
            return num / total *100;


    def oss_put_obj(self,obj,name):
        try:
            inputData= json.dumps(obj,ensure_ascii=False)
            ossResult = self.oss_bucket.put_object(name, inputData)
        except Exception as e:
            print(e)

    def oss_get_obj(self,name):
        try:
            object_stream = self.oss_bucket.get_object(name)
            readObj = object_stream.read()
            readObj = json.loads(str(readObj,'utf-8'))
            return readObj
        except Exception as e:
            print(e)

    def getServerName(self):
        serverName = ""
        privateIP = ""
        try: 
            s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
            s.connect(('8.8.8.8',80)) 
            privateIP = s.getsockname()[0] 
        finally: 
            s.close()
        nowPage =1
        emptyReq =False
        while serverName=="" and not emptyReq:
            client =  AcsClient(ALIYUN_API_KEY, ALIYUN_API_SECRET,ALIYUN_POINT)
            client.add_endpoint(ALIYUN_POINT,'Ecs',"ecs."+ALIYUN_POINT+".aliyuncs.com")
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
            for i in range(len(instanceInfoArr)):
                if instanceInfoArr[i]["VpcAttributes"]["PrivateIpAddress"]["IpAddress"][0]==privateIP:
                    serverName = instanceInfoArr[i]["InstanceName"]
            nowPage = nowPage+1
        return serverName

    def begin_trade_record(self,volMultiple,standardRate,symbol,klineArr,nowOpenRate,machineNumber,direction,myTradeType,longsConditionA,shortsConditionA,shortsConditionB,btcNowOpenRate,ethNowOpenRate,clientBeginPrice,clientEndPrice):
        try:
            url = "http://"+WEB_ADDRESS+":8888/begin_trade_record"

            postDataObj = {
            'volMultiple':volMultiple,
            'standardRate':standardRate,
            'symbol':symbol,
            'klineArr':json.dumps(klineArr),
            'nowOpenRate':nowOpenRate,
            'machineNumber':machineNumber,
            'direction':direction,
            'myTradeType':myTradeType,
            'longsConditionA':longsConditionA,
            'shortsConditionA':shortsConditionA,
            'shortsConditionB':shortsConditionB,
            'btcNowOpenRate':btcNowOpenRate,
            'ethNowOpenRate':ethNowOpenRate,
            'clientBeginPrice':clientBeginPrice,
            'clientEndPrice':clientEndPrice,
            'privateIP':self.privateIP,
            }
            print(postDataObj)
            postDataObj = postDataObj
            print(postDataObj)
            response = requests.request("POST", url,timeout=(3,3),data=postDataObj)
        except Exception as e:
            self.send_lark_msg_limit_one_min(str(e))
            print(e)
