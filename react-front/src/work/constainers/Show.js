import React, { Component } from 'react';
import * as action from "../actions";
import {bindActionCreators} from "redux";
import {connect} from "react-redux";

import {
    message,
    Table,
    Timeline ,
    Tag,
    Collapse,
    Select,
    Modal,
    Alert,
    Divider
} from 'antd';
import { DollarOutlined,QuestionCircleOutlined,CheckOutlined} from '@ant-design/icons';
import {withRouter} from "react-router";

import {deepCopy,formatTime,turnTsToTime} from "../constants/commonFunction";
import ReactECharts from 'echarts-for-react';

import TweenOne from 'rc-tween-one';
import Children from 'rc-tween-one/lib/plugin/ChildrenPlugin';

TweenOne.plugins.push(Children);

const darkWordColor="#8c8c8c"
const { Option } = Select;
const positionColumns = [
    {
        title: '交易对',
        dataIndex: 'symbol',
        key: 'symbol',
    },
    {
        title: '价值',
        dataIndex: 'value',
        key: 'value',
    },
    {
        title: '成本价',
        dataIndex: 'entryPrice',
        key: 'entryPrice',
    },
    {
        title: '方向',
        dataIndex: 'direction',
        key: 'direction',
    }
]

let historyTableColumns = [
    {
        title: '交易对',
        dataIndex: 'symbol',
        key: 'symbol',
    },
    {
        title: '昨日利润',
        dataIndex: 'yesterdayProfit',
        key: 'yesterdayProfit',
        sorter: (a, b) => a.yesterdayProfit - b.yesterdayProfit,
    },
    {
        title: '昨日BNB',
        dataIndex: 'yesterdayVol',
        key: 'yesterdayVol',
        sorter: (a, b) => a.yesterdayVol - b.yesterdayVol,
    },
    {
        title: '昨日手续费',
        dataIndex: 'yesterdayCommission',
        key: 'yesterdayCommission',
        sorter: (a, b) => a.yesterdayCommission - b.yesterdayCommission,
    },
    {
        title: '周利润',
        dataIndex: 'weekProfit',
        key: 'weekProfit',
        sorter: (a, b) => a.weekProfit - b.weekProfit,
    },
    {
        title: '周BNB',
        dataIndex: 'weekVol',
        key: 'weekVol',
        sorter: (a, b) => a.weekVol - b.weekVol,
    },
    {
        title: '周手续费',
        dataIndex: 'weekCommission',
        key: 'weekCommission',
        sorter: (a, b) => a.weekCommission - b.weekCommission,
    },
    {
        title: '月利润',
        dataIndex: 'monthProfit',
        key: 'monthProfit',
        sorter: (a, b) => a.monthProfit - b.monthProfit,
    },
    {
        title: '月BNB',
        dataIndex: 'monthVol',
        key: 'monthVol',
        sorter: (a, b) => a.monthVol - b.monthVol,
    },
    {
        title: '月手续费',
        dataIndex: 'monthCommission',
        key: 'monthCommission',
        sorter: (a, b) => a.monthCommission - b.monthCommission,
    },    {
        title: '总利润',
        dataIndex: 'allProfit',
        key: 'allProfit',
        sorter: (a, b) => a.allProfit - b.allProfit,
    },
    {
        title: '总BNB',
        dataIndex: 'allVol',
        key: 'allVol',
        sorter: (a, b) => a.allVol - b.allVol,
    },
    {
        title: '总手续费',
        dataIndex: 'allCommission',
        key: 'allCommission',
        sorter: (a, b) => a.allCommission - b.allCommission,
    },]


let bigLossTradesRecordColumns = [
    {
        title: '时间',
        dataIndex: 'time',
        key: 'time',
    },
    {
        title: '交易对',
        dataIndex: 'symbol',
        key: 'symbol'
    },
    {
        title: '方向',
        dataIndex: 'direction',
        key: 'direction'
    },
    {
        title: '收益金额',
        dataIndex: 'profit',
        key: 'profit',
        sorter: (a, b) => a.profit - b.profit,
    },
    {
        title: '收益占余额比例',
        dataIndex: 'profitPercentByBalance',
        key: 'profitPercentByBalance',
        sorter: (a, b) => parseFloat(a.profitPercentByBalance) - parseFloat(b.profitPercentByBalance),
    }
]



const HISTORY_TABLE_TYPE_OBJ = {
    "fromLastInvestor":"参与者变化后",
    "lastOneDay":"最近一天",
    "lastSevenDays":"最近七天",
    "lastOneMonth":"最近一个月",
    "all":"全部",
}

const HISTORY_TABLE_TYPE_ARR = ["fromLastInvestor","lastOneDay","lastSevenDays","lastOneMonth","all"]
const DAY_INCOME_TABLE_TYPE_ARR = ["bar","line"]
const DAY_INCOME_TABLE_CHINESE_TYPE_ARR = ["分段柱形图","总和折线图"]
class Show extends Component {
    constructor(props) {
        super(props);
        let timestamp = Date.parse(new Date());
        let storage=window.localStorage;
        let dayIncomeTableType = storage["dayIncomeTableType"]?storage["dayIncomeTableType"]:"bar"
        this.state = {
            dayIncomeTableType:dayIncomeTableType,//bar or line
            nowBalance:0,
            allPositionValue:0,
            allProfit:0,
            allCommission:0,

            timeArr:[],
            balanceArr:[],
            priceArr:[],
            minPrice:0,
            minBalance:0,
            positionValueArr:[],
            minPositionValue:0,

            allPosition:0,
            historyTableArr:[],
            historyTableUpdateTime:0,
            oneDayProfit:0,
            oneDayVol:0,
            investPercentObjArr:[],
            tradeServerObj : {
                "updateTs":0,
                "updateTime":"",
                "status":"运行中"
            },
            bigLossTradesRecordArr:[],
            historyTableType:"fromLastInvestor", //fromLastInvestor,lastOneDay,lastSevenDays,lastOneMonth,all
            lastMinTime:"",
            historyInvestorIndex:1,
            historyInvestorTableData:[],
            nowBalanceAnimation: null,
            allProfitAnimation:null,
            oneDayVolAnimation:null,
            allPositionValueAnimation:null,
            allInitValue:0,
            dayIncomeTimeArr:[],
            dayIncomeValueBarArr:[],

            dayIncomeValueLineArr:[],
            dayIncomeUpdateTime:"-",
            isRouteVisible:false,
            positionArr:[]
        }

    }
    getHistoryTableData = (historyInvestorIndex)=>{
        let nowTs = parseInt(new Date().getTime()) - 60000
        let lastMinTime = turnTsToTime(nowTs,"1m")
        console.error(lastMinTime)
        let url ="https://zuibite-api.oss-cn-hongkong.aliyuncs.com/investor/"+lastMinTime+".json?"+Math.random()
        let request = new XMLHttpRequest();
        request.open("get", url);/*设置请求方法与路径*/
        request.setRequestHeader("Cache-Control","no-cache");
        request.setRequestHeader("Access-Control-Allow-Origin","*");
        request.setRequestHeader("Access-Control-Allow-Methods","get,post,put,delete");
        request.send(null);/*不发送数据到服务器*/
        request.onload =()=> {
            let response = JSON.parse(request.responseText);
            let historyInvestorTableData = response["history"][historyInvestorIndex]["userData"]
            console.info(response)
            this.setState({
                historyInvestorTableData:historyInvestorTableData,

            })
        }
    }
    getQuantData = ()=>{
        let nowTs = parseInt(new Date().getTime()) - 60000
        let lastMinTime = turnTsToTime(nowTs,"1m")
        let url ="https://zuibite-api.oss-cn-hongkong.aliyuncs.com/cQuant/"+lastMinTime+".json?"+Math.random()
        let request = new XMLHttpRequest();
        request.open("get", url);/*设置请求方法与路径*/
        request.setRequestHeader("Cache-Control","no-cache");
        request.setRequestHeader("Access-Control-Allow-Origin","*");
        request.setRequestHeader("Access-Control-Allow-Methods","get,post,put,delete");
        request.send(null);/*不发送数据到服务器*/
        request.onload =()=> {
            let response = JSON.parse(request.responseText);
            let bigLossTradesRecordArr = []
            for(let a=0;a<response["bigLossTradeArr"].length;a++){
                bigLossTradesRecordArr.push({
                    "symbol":response["bigLossTradeArr"][a][0],
                    "time":response["bigLossTradeArr"][a][1],
                    "profit":response["bigLossTradeArr"][a][2],
                    "profitPercentByBalance":response["bigLossTradeArr"][a][3],
                    "priceRate":response["bigLossTradeArr"][a][4]+"%",
                    "direction":response["bigLossTradeArr"][a][5]=="shorts"?"做空":"做多",
                })
            }

            let secondOpenObjArr = response["secondOpenObjArr"]

            let historyTableArr = []

            let allProfit = response["todayProfit"]
            for(let key in secondOpenObjArr["p"]){

                historyTableArr.push({
                    "symbol":key=="all"?"全部":key,
                    "yesterdayProfit":(secondOpenObjArr["p"][key][0]).toFixed(6),
                    "yesterdayVol":(secondOpenObjArr["v"][key][0]).toFixed(6),
                    "yesterdayCommission":(secondOpenObjArr["c"][key][0]).toFixed(6),

                    "weekProfit":(secondOpenObjArr["p"][key][1]).toFixed(3),
                    "weekVol":(secondOpenObjArr["v"][key][1]).toFixed(3),
                    "weekCommission":(secondOpenObjArr["c"][key][1]).toFixed(3),

                    "monthProfit":(secondOpenObjArr["p"][key][2]).toFixed(3),
                    "monthVol":(secondOpenObjArr["v"][key][2]).toFixed(3),
                    "monthCommission":(secondOpenObjArr["c"][key][2]).toFixed(3),

                    "allProfit":(secondOpenObjArr["p"][key][3]).toFixed(3),
                    "allVol":(secondOpenObjArr["v"][key][3]).toFixed(3),
                    "allCommission":(secondOpenObjArr["c"][key][3]).toFixed(3),
                })
                if (key=="all"){
                    allProfit = allProfit+(secondOpenObjArr["p"][key][3])
                }
            }




            let nowTs = parseInt(new Date().getTime())


            let statusObj = {
                "stopByAccountBalanceValue":"亏损停机",
                "run":<CheckOutlined style={{color:"green"}}/>,
                "bug":"系统意外崩溃",
                "maintain":"维护中"
            }
            let normal = false
            console.info(nowTs-response['systemUpdateTs']*1000)
            if(nowTs-response['systemUpdateTs']*1000<5*60*1000){
                normal = true
            }else{

                response['systemStatus'] = "bug"
            }

            let tradeServerObj = {
                "normal":normal,
                "updateTs":response['systemUpdateTs'],
                "updateTime":turnTsToTime(response['systemUpdateTs']),
                "status":statusObj[response['systemStatus']],
                "runTime":response['runTime']
            }

            let investPercentObjArr = response["investPercentObjArr"]
            let lastChangeTs = 0
            let allInitValue = 0


            let positionArr =  response["positionArr"]
            if(this.state.timeArr.length==0){
                this.getPositionRecord()
            }

            this.setState({
                positionArr:positionArr,
                allInitValue:allInitValue,
                allProfit:allProfit,
                historyTableUpdateTime:turnTsToTime(secondOpenObjArr["t"]),
                allPositionValue: response["allPositionValue"],
                lastMinTime:lastMinTime,
                investPercentObjArr:investPercentObjArr,
                tradeServerObj:tradeServerObj,
                nowBalance: response["accountBalanceValue"],
                bigLossTradesRecordArr:bigLossTradesRecordArr,
                oneDayVol:response["oneDayVol"],
                oneDayProfit:response["oneDayProfit"],
                historyTableArr:historyTableArr,

                nowBalanceAnimation: {
                    Children: {
                        value: parseInt(response["accountBalanceValue"]),
                        formatMoney:true,
                        floatLength: 0
                    },
                    duration: 1000,
                },
                allProfitAnimation: {
                    Children: {
                        value: parseInt(allProfit),
                        formatMoney:true,
                        floatLength: 0
                    },
                    duration: 1000,
                },
                allPositionValueAnimation: {
                    Children: {
                        value: parseInt(response["allPositionValue"]),
                        formatMoney:true,
                        floatLength: 0
                    },
                    duration: 1000,
                },
                oneDayVolAnimation: {
                    Children: {
                        value: parseInt(response["oneDayVol"]),
                        formatMoney:true,
                        floatLength: 0
                    },
                    duration: 1000,
                },
            })
        }
    }

    componentDidMount = () => {
        console.error("componentDidMount")
        let storage=window.localStorage;
        this.getDayIncomeData()
        this.getQuantData()
        this.getPositionRecord()
        setInterval(()=>{this.getDayIncomeData()},15*60000);
        setInterval(()=>{
            let nowTs = parseInt(new Date().getTime()) - 60000
            let lastMinTime = turnTsToTime(nowTs,"1m")
            if(lastMinTime!=this.state.lastMinTime){

                this.getQuantData()
                this.getPositionRecord()
            }

        },3000);
    }

    getDayIncomeData = ()=>{
        let nowTs = parseInt(new Date().getTime()) - 60000
        let url ="https://zuibite-api.oss-cn-hongkong.aliyuncs.com/cQuant_day_income/data.json?"+Math.random()
        let request = new XMLHttpRequest();
        request.open("get", url);/*设置请求方法与路径*/
        request.setRequestHeader("Cache-Control","no-cache");
        request.setRequestHeader("Access-Control-Allow-Origin","*");
        request.setRequestHeader("Access-Control-Allow-Methods","get,post,put,delete");
        request.send(null);/*不发送数据到服务器*/
        request.onload =()=> {
            let response = JSON.parse(request.responseText);
            let dayIncomeResponseArr = response["data"]
            let dayIncomeUpdateTime = turnTsToTime(response["ts"])
            let dayIncomeTimeArr = []
            let dayIncomeValueBarArr = []
            let dayIncomeValueLineArr = []
            let allIncomeValue = 0
            for(let a=0;a<dayIncomeResponseArr.length;a++){
                dayIncomeTimeArr.push(dayIncomeResponseArr[a][0])
                dayIncomeValueBarArr.push(dayIncomeResponseArr[a][1])
                allIncomeValue = allIncomeValue+dayIncomeResponseArr[a][1]
                dayIncomeValueLineArr.push(allIncomeValue)
            }

            this.setState({
                dayIncomeUpdateTime:dayIncomeUpdateTime,
                dayIncomeTimeArr:dayIncomeTimeArr,
                dayIncomeValueBarArr:dayIncomeValueBarArr,
                dayIncomeValueLineArr:dayIncomeValueLineArr
            })
        }
    }
    getPositionRecord = ()=>{
        let nowTs = parseInt(new Date().getTime()) - 60000
        let url ="https://zuibite-api.oss-cn-hongkong.aliyuncs.com/cQuant_change/"+this.state.historyTableType+"Arr.json?"+Math.random()
        let request = new XMLHttpRequest();
        request.open("get", url);/*设置请求方法与路径*/
        request.setRequestHeader("Cache-Control","no-cache");
        request.setRequestHeader("Access-Control-Allow-Origin","*");
        request.setRequestHeader("Access-Control-Allow-Methods","get,post,put,delete");
        request.send(null);/*不发送数据到服务器*/
        request.onload =()=> {
            let response = JSON.parse(request.responseText);
            let positionRecordObjArr = response
            let timeArr = []
            let balanceArr = []
            let positionValueArr = []
            let minBalance = 99999999
            let minPositionValue = 99999999
            let nowTs = 0
            let nowBalance = 0
            let nowPosition = 0
            for(let a=0;a<positionRecordObjArr.length;a++){
                nowTs = nowTs+positionRecordObjArr[a][2]
                nowBalance = nowBalance+positionRecordObjArr[a][1]
                nowPosition = nowPosition+positionRecordObjArr[a][0]
                let thisTime = turnTsToTime(nowTs)
                let thisBalance = nowBalance
                let thisPositionValue = nowPosition

                timeArr.push(thisTime)
                balanceArr.push(thisBalance)
                positionValueArr.push(thisPositionValue)

                if(thisBalance<minBalance){
                    minBalance = thisBalance
                }

                if(thisPositionValue<minPositionValue){
                    minPositionValue = thisPositionValue
                }

            }

            this.setState({
                timeArr:timeArr,
                balanceArr:balanceArr,
                minBalance:minBalance,
                positionValueArr:positionValueArr,
                minPositionValue:minPositionValue
            })
        }
    }

    getPeriodAnnualizedStyle = (periodAnnualized)=>{
        if(periodAnnualized>0){
            return <span style={{color:"green"}}>+{periodAnnualized} %</span>
        }else{
            return <span style={{color:"red"}}>{periodAnnualized} %</span>
        }
    }
    render() {
        let balanceOption = {
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['value']
            },
            xAxis: {
                type: 'category',
                data: this.state.timeArr
            },
            yAxis: {
                type: 'value',
                min:this.state.minBalance
            },
            series: [
                {
                    data: this.state.balanceArr,
                    type: 'line'
                }
            ]


        };

        let positionAmtOption = {
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['value']
            },
            xAxis: {
                type: 'category',
                data: this.state.timeArr
            },
            yAxis: {
                type: 'value',
                min: this.state.minPositionValue,
            },
            series: [
                {
                    data: this.state.positionValueArr,
                    type: 'line'
                }
            ]


        };

        let dayIncomeBarOption= {
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['value']
            },
            xAxis: {
                type: 'category',
                data: this.state.dayIncomeTimeArr
            },
            yAxis: {
                type: 'value',
                // min: this.state.dayIncomeValueArr,
            },
            series: [
                {
                    data: this.state.dayIncomeValueBarArr,
                    type: 'bar'
                }
            ]


        };

        let dayIncomeLineOption= {
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['value']
            },
            xAxis: {
                type: 'category',
                data: this.state.dayIncomeTimeArr
            },
            yAxis: {
                type: 'value',
                // min: this.state.dayIncomeValueArr,
            },
            series: [
                {
                    data: this.state.dayIncomeValueLineArr,
                    type: 'line'
                }
            ]


        };
        return <div style={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            color: darkWordColor,
            minHeight: document.body.clientHeight,
            backgroundColor: "rgb(240, 240, 240)",
            minWidth:1600 ,
            minHight:6000 ,
            height: "100%",
            padding: 0
        }}>

                <div style={{ padding: 0,backgroundColor: "#f5f5f5",width:"100%",display: "flex", flexDirection: "column",alignItems: "center",justifyContent: "center"}}>
                    <div style={{width:"90%",marginTop:64}}>
                        <span style={{fontSize:48,marginLeft:8,color:this.state.oneDayProfit>0?"#ff4d4f":"#13c2c2"}}><strong>C</strong></span>
                        <span style={{fontSize:48,marginLeft:8,color:this.state.oneDayProfit>0?"#ff7a45":"#36cfc9"}}><strong>QUANT</strong></span>
                        {/*<span style={{fontSize:16,marginLeft:16,paddingBottom:16,color:"#737373"}}><Tag style={{marginBottom:8}} color={this.state.oneDayProfit>0?"red":"green"}>V2</Tag></span>*/}


                        <span style={{marginLeft:128,marginTop:8,color:this.state.oneDayProfit>0?"red":"green",fontSize:16}}>
<Tag color={this.state.oneDayProfit>0?"#f50":"#87d068"}> 24H {this.state.oneDayProfit>0?"+"+this.state.oneDayProfit:this.state.oneDayProfit } USD </Tag>
                            </span>
                        <span style={{fontSize:14,marginLeft:64,color:"#737373"}}>{
                            this.state.lastMinTime==""?"数据读取中，如无显示请联系负责人":turnTsToTime(turnTsToTime(this.state.lastMinTime),"other")
                        }</span>


                    </div>

                <div style={{color:"#919191",marginTop:88,width:"90%",display: "flex", flexDirection: "row",alignItems:"center"}}>
                    <div style={{borderRadius:10,width:220,padding:24,backgroundColor:"#ececec"}}>
                        总价值
                        <div style={{marginTop:4,display: "flex", flexDirection: "row",alignItems:"baseline"}}>
                            <strong style={{color:"#000000",fontSize:26,marginRight:8}}>
                                <TweenOne
                                    animation={this.state.nowBalanceAnimation}
                                    style={{ fontSize: 26, marginBottom: 0 }}
                                >
                                    0
                                </TweenOne>
                            </strong> USD
                        </div>
                    </div>

                    <div style={{marginLeft:64,borderRadius:10,width:220,padding:24,backgroundColor:"#ececec"}}>
                        当前持仓价值
                        <div style={{marginTop:4,display: "flex", flexDirection: "row",alignItems:"baseline"}}>
                            <strong style={{color:"#000000",fontSize:26,marginRight:8}}>
                                <TweenOne
                                    animation={this.state.allPositionValueAnimation}
                                    style={{ fontSize: 26, marginBottom: 0 }}
                                >
                                    0
                                </TweenOne>
                            </strong> USD
                        </div>

                    </div>
                    <div style={{marginLeft:64,borderRadius:10,width:220,padding:24,backgroundColor:"#ececec"}}>
                        24小时手续费
                        <div style={{marginTop:4,display: "flex", flexDirection: "row",alignItems:"baseline"}}>
                            <strong style={{color:"#000000",fontSize:26,marginRight:8}}>
                                {/*{this.state.nowBalance.toFixed(0)}*/}
                                <TweenOne
                                    animation={this.state.oneDayVolAnimation}
                                    style={{ fontSize: 26, marginBottom: 0 }}
                                >
                                    0
                                </TweenOne>
                            </strong> USD
                        </div>

                    </div>
                    <div style={{marginLeft:64,borderRadius:10,width:275,padding:24,backgroundColor:"#ececec"}}>
                        发布至今净利润
                        <div style={{marginTop:4,display: "flex", flexDirection: "row",alignItems:"baseline"}}>
                            <strong style={{color:"#000000",fontSize:26,marginRight:8}}>
                                {/*{this.state.nowBalance.toFixed(0)}*/}
                                <TweenOne
                                    animation={this.state.allProfitAnimation}
                                    style={{ fontSize: 26, marginBottom: 0 }}
                                >
                                    0
                                </TweenOne>
                            </strong> USD
                        </div>
                    </div>
                    <div style={{marginLeft:64,borderRadius:10,width:300,padding:24,backgroundColor:"#ececec"}}>
                        系统状态
                        <div style={{marginTop:4}}>{
                            this.state.tradeServerObj["normal"]?

                                <div>
                                    <strong style={{marginTop:8,color:"#000000",fontSize:26,marginRight:8}}>{this.state.tradeServerObj["status"]}</strong>
                                    近一分钟检索全币种 {this.state.tradeServerObj["runTime"]} 次
                                </div>:
                                <div>
                                    <strong style={{marginTop:8,color:"#000000",fontSize:26,marginRight:12}}>{this.state.tradeServerObj["status"]}</strong>
                                    {this.state.tradeServerObj["updateTime"]}
                                </div>
                        }</div>
                    </div>
                </div>

                    {/*<div style={{marginTop:88,width:"90%"}}>*/}

                    {/*    <Divider >*/}
                    {/*        仓位*/}
                    {/*    </Divider>*/}

                    {/*    <Table style={{marginTop:32}} showSorterTooltip={false} dataSource={this.state.positionArr} columns={positionColumns}*/}
                    {/*           pagination={false} />*/}

                    {/*</div>*/}

                <div style={{marginTop:88,width:"90%"}}>

                    <Divider >
                        余额和持仓价值
                    </Divider>
                    <div style={{marginTop:32,width:"100%"}}>
                        <Alert style={{marginTop:32}} message={"2023-07-20 05:00:00 开始记录，每分钟更新一次"} type="warning" />

                    </div>
                    <div style={{marginTop:64,width:"90%"}}>
                        <Select onChange={(value)=>{
                            this.state.historyTableType = value
                            this.getPositionRecord()
                            this.setState({
                            historyTableType:value
                        })}} value={this.state.historyTableType} style={{width:200,marginLeft:16}}>
                        {
                            HISTORY_TABLE_TYPE_ARR.map((item,i)=>{
                                return <Option  key={i} value={item}>
                                    {HISTORY_TABLE_TYPE_OBJ[item]}
                                </Option >
                            })
                        }

                        </Select>

                    </div>
                    <ReactECharts
                        option={balanceOption}
                        notMerge={false}
                    />

                    <ReactECharts
                        style={{marginTop:32}}
                        option={positionAmtOption}
                        notMerge={false}
                    />

                </div>
                    <div style={{marginTop:88,width:"90%"}}>

                        <Divider >
                            净利润日变化
                        </Divider>
                        <Alert style={{marginTop:32}} message={"更新于："+this.state.dayIncomeUpdateTime+"，净利润包含了订单利润，资金费率和手续费"} type="warning" />
                        <div style={{marginTop:64,width:"90%"}}>
                            <Select onChange={(value)=>{
                                this.getPositionRecord()
                                let storage=window.localStorage;
                                storage["dayIncomeTableType"] = value
                                this.setState({
                                    dayIncomeTableType:value
                                })}} value={this.state.dayIncomeTableType} style={{width:200,marginLeft:16}}>
                                {
                                    DAY_INCOME_TABLE_TYPE_ARR.map((item,i)=>{
                                        return <Option  key={i} value={item}>
                                            {DAY_INCOME_TABLE_CHINESE_TYPE_ARR[i]}
                                        </Option >
                                    })
                                }

                            </Select>

                        </div>
                        <ReactECharts
                            option={this.state.dayIncomeTableType=="line"?dayIncomeLineOption:dayIncomeBarOption}
                            notMerge={false}
                        />


                    </div>
                {this.state.bigLossTradesRecordArr.length==0?<div style={{marginTop:88,width:"90%"}}>
                        <Alert style={{marginTop:32}} message={"当前暂未读取到大额亏损交易，该数据自2023年5月19日开始记录"} type="warning" />
                    </div>
                    :<div style={{marginTop:88,width:"90%"}}>

                        <Divider >
                            交易展示
                        </Divider>

                        <Alert style={{marginTop:32}} message={"2023-5-19 12:00:00 开始记录，检索规则为亏损大于 50 USD，该数据存在5分钟的延迟"} type="warning" />
                        <Table style={{marginTop:32}} showSorterTooltip={false} dataSource={this.state.bigLossTradesRecordArr} columns={bigLossTradesRecordColumns}
                               pagination={10} showSizeChanger ={false}/>
                    </div>}


                <div style={{marginTop:88,width:"90%"}}>

                    <Divider >
                        历史数据
                    </Divider>
                    <Alert style={{marginTop:32}} message={"更新于："+this.state.historyTableUpdateTime+"，利润为净利润，即算上手续费和资金费率后的利润，手续费为负代表付出手续费，手续费为正代表收取手续费"} type="warning" />

                    <Table style={{marginTop:32}} showSorterTooltip={false} dataSource={this.state.historyTableArr} columns={historyTableColumns}
                            pagination={false} />

                </div>


            </div>}
        </div>
    }
}
const mapStateToProps = (state) => {
    return ({
        chat:state.chat,
        userInfo:state.userInfo,
        otherConfig:state.otherConfig,
        timestamp:state.setting['timestamp'],
    });
};
const mapDispatchToProps  = (dispatch, ownProps) => {
    return bindActionCreators({
        modifyChatArr:action.modifyChatArr,
        switchSubPage:action.switchSubPage,
        changeUserInfo:action.changeUserInfo
    }, dispatch);
};
export default withRouter(connect(mapStateToProps,mapDispatchToProps)(Show));
