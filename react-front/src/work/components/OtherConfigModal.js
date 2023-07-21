import React from 'react';
import {
    QuestionOutlined,
    EditOutlined
} from '@ant-design/icons';
import {
    Button,
    Upload,
    InputNumber,
    Radio,
    Slider,
    Tag,
    Input,
    Pagination,
    Collapse,
    Avatar,
    message,
    Select,
    Modal,
    Checkbox,
    Alert,
    Switch,
    Table
} from 'antd';
import {connect} from "react-redux";
import * as action from "../actions";
import {bindActionCreators} from "redux";
import {keyboardObj, realHotKeyConfigDefaultObj,keyboardFunArr,sortTypeObj} from '../constants/hotkey'
import {
    deepCopy,
    stateDefaultObj,
    supportKlineIntervalEnglish, supportKlineIntervalChinese, turnTsToTime
} from '../constants/commonFunction'
import {modifyOtherConfig} from "../actions";
import {publicServerURL} from "../constants/serverURL";

const audio = new Audio("https://zuibite-api.oss-cn-hongkong.aliyuncs.com/goals.mp3");
const { Option } = Select;
const { TextArea } = Input;
const { Panel } = Collapse;
const otherConfigTableColumns= [
    {
        title: '配置名',
        dataIndex: 'name',
        key: 'name',
    },
    {
        title: '配置值',
        dataIndex: 'value',
        key: 'value'
    },
    {
        title: '服务器端值',
        dataIndex: 'serverValue',
        key: 'serverValue'
    }
];
class OtherConfigModal extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            serverStateConfig: {},
        };
    }

    componentDidMount=() =>{
        this.getServerStateConfig()
    }


    restoreServerStateConfig= ()=>{
        let storage=window.localStorage;
        let maxLossLockTs = storage["maxLossLockTs"]?parseInt(storage["maxLossLockTs"]):0
        let nowTs = parseInt(new Date().getTime());
        if(nowTs< maxLossLockTs){

            message.error("单位时间最大亏损锁上锁中，解锁时间："+turnTsToTime(maxLossLockTs))
            return
        }
        const {serverStateConfig} = this.state;
        let keyCorrection = true
        for (let key in stateDefaultObj){
            if(!key in serverStateConfig){
                keyCorrection = false
            }
        }
        if(keyCorrection){
            message.success("成功恢复为服务端配置")
            storage["autoBuyBnbConfigArr"]=JSON.stringify(serverStateConfig["autoBuyBnbConfigArr"])
            storage["klineCountConfigArr"]=JSON.stringify(serverStateConfig["klineCountConfigArr"])
            storage["depthConfigArr"]=JSON.stringify(serverStateConfig["depthConfigArr"])
            storage["sortFrequencyTsConfigArr"]=JSON.stringify(serverStateConfig["sortFrequencyTsConfigArr"])
            storage["binanceAddressConfigArr"]=JSON.stringify(serverStateConfig["binanceAddressConfigArr"])
            storage["selectKlineIntervalConfigArr"]=JSON.stringify(serverStateConfig["selectKlineIntervalConfigArr"])
            storage["klineRowCountConfigArr"]=JSON.stringify(serverStateConfig["klineRowCountConfigArr"])
            storage["autoStopLossConfigArr"]=JSON.stringify(serverStateConfig["autoStopLossConfigArr"])
            storage["autoCancelStopLossConfigArr"]=JSON.stringify(serverStateConfig["autoCancelStopLossConfigArr"])
            storage["limitMaxPositionLockConfigArr"]=JSON.stringify(serverStateConfig["limitMaxPositionLockConfigArr"])
            storage["limitMaxLossLockConfigArr"]=JSON.stringify(serverStateConfig["limitMaxLossLockConfigArr"])
            storage["serverUpdateTsConfigArr"]=JSON.stringify(serverStateConfig["serverUpdateTsConfigArr"])
            storage["showProfitWithLeverConfigArr"]=JSON.stringify(serverStateConfig["showProfitWithLeverConfigArr"])
            storage["mindModeConfigArr"]=JSON.stringify(serverStateConfig["mindModeConfigArr"])
            storage["rocketLimitConfigArr"]=JSON.stringify(serverStateConfig["rocketLimitConfigArr"])
            storage["autoCancelOrderConfigArr"]=JSON.stringify(serverStateConfig["autoCancelOrderConfigArr"])
            storage["binanceRecommissionConfigArr"]=JSON.stringify(serverStateConfig["binanceRecommissionConfigArr"])
            storage["limitTimeMaxPositionConfigArr"]=JSON.stringify(serverStateConfig["limitTimeMaxPositionConfigArr"])
            storage["shieldLossSymbolConfigArr"]=JSON.stringify(serverStateConfig["shieldLossSymbolConfigArr"])
            this.props.modifyOtherConfig({
                ...this.props.otherConfig,
                ...this.state.serverStateConfig
            })
        }else{
            message.error("服务器数据与默认数据校正出错，无法直接恢复")
        }

    }

    restoreDefaultStateConfig = ()=>{
        let storage=window.localStorage;
        let maxLossLockTs = storage["maxLossLockTs"]?parseInt(storage["maxLossLockTs"]):0
        let nowTs = parseInt(new Date().getTime());
        if(nowTs< maxLossLockTs){

            message.error("单位时间最大亏损锁上锁中，解锁时间："+turnTsToTime(maxLossLockTs))
            return
        }
        message.success("成功恢复默认配置")
        storage["autoBuyBnbConfigArr"]=JSON.stringify(stateDefaultObj["autoBuyBnbConfigArr"])
        storage["klineCountConfigArr"]=JSON.stringify(stateDefaultObj["klineCountConfigArr"])
        storage["depthConfigArr"]=JSON.stringify(stateDefaultObj["depthConfigArr"])
        storage["sortFrequencyTsConfigArr"]=JSON.stringify(stateDefaultObj["sortFrequencyTsConfigArr"])
        storage["binanceAddressConfigArr"]=JSON.stringify(stateDefaultObj["binanceAddressConfigArr"])
        storage["selectKlineIntervalConfigArr"]=JSON.stringify(stateDefaultObj["selectKlineIntervalConfigArr"])
        storage["klineRowCountConfigArr"]=JSON.stringify(stateDefaultObj["klineRowCountConfigArr"])
        storage["autoStopLossConfigArr"]=JSON.stringify(stateDefaultObj["autoStopLossConfigArr"])
        storage["autoCancelStopLossConfigArr"]=JSON.stringify(stateDefaultObj["autoCancelStopLossConfigArr"])
        storage["limitMaxPositionLockConfigArr"]=JSON.stringify(stateDefaultObj["limitMaxPositionLockConfigArr"])
        storage["limitMaxLossLockConfigArr"]=JSON.stringify(stateDefaultObj["limitMaxLossLockConfigArr"])
        storage["serverUpdateTsConfigArr"]=JSON.stringify(stateDefaultObj["serverUpdateTsConfigArr"])
        storage["showProfitWithLeverConfigArr"]=JSON.stringify(stateDefaultObj["showProfitWithLeverConfigArr"])
        storage["mindModeConfigArr"]=JSON.stringify(stateDefaultObj["mindModeConfigArr"])
        storage["rocketLimitConfigArr"]=JSON.stringify(stateDefaultObj["rocketLimitConfigArr"])
        storage["autoCancelOrderConfigArr"]=JSON.stringify(stateDefaultObj["autoCancelOrderConfigArr"])
        storage["binanceRecommissionConfigArr"]=JSON.stringify(stateDefaultObj["binanceRecommissionConfigArr"])
        storage["limitTimeMaxPositionConfigArr"]=JSON.stringify(stateDefaultObj["limitTimeMaxPositionConfigArr"])
        storage["shieldLossSymbolConfigArr"]=JSON.stringify(stateDefaultObj["shieldLossSymbolConfigArr"])
        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            ...stateDefaultObj
        })
    }
    getServerStateConfig = ()=>{
        const {userInfo} = this.props
        let formData = new FormData();
        formData.append("accessToken",userInfo["accessToken"]);
        fetch(publicServerURL+"/get_state_config", {
            method:'POST',
            body:formData
        }).then((response)=>{
            if (response.ok) {
                return response.json();
            }
        }).then((response)=>{
            if(response['s']=="error"){
                message.error("服务器读取其他配置出错")
            }else{

                this.setState({
                    serverStateConfig: response['stateConfigObj']
                })
            }
        }).catch((error)=>{
            console.error(error)
        });
    }
    modifyStateConfig = ()=>{
        const {otherConfig} = this.props
        const {userInfo} = this.props
        let stateConfigObj = {
            "autoBuyBnbConfigArr":otherConfig.autoBuyBnbConfigArr,
            "klineCountConfigArr":otherConfig.klineCountConfigArr,
            "depthConfigArr":otherConfig.depthConfigArr,
            "sortFrequencyTsConfigArr":otherConfig.sortFrequencyTsConfigArr,
            "binanceAddressConfigArr": otherConfig.binanceAddressConfigArr,
            "selectKlineIntervalConfigArr":otherConfig.selectKlineIntervalConfigArr,
            "klineRowCountConfigArr":otherConfig.klineRowCountConfigArr,
            "autoStopLossConfigArr":otherConfig.autoStopLossConfigArr,
            "autoCancelStopLossConfigArr":otherConfig.autoCancelStopLossConfigArr,
            "limitMaxPositionLockConfigArr":otherConfig.limitMaxPositionLockConfigArr,
            "limitMaxLossLockConfigArr":otherConfig.limitMaxLossLockConfigArr,
            "showProfitWithLeverConfigArr":otherConfig.showProfitWithLeverConfigArr,
            "mindModeConfigArr":otherConfig.mindModeConfigArr,
            "rocketLimitConfigArr":otherConfig.rocketLimitConfigArr,
            "autoCancelOrderConfigArr":otherConfig.autoCancelOrderConfigArr,
            "binanceRecommissionConfigArr":otherConfig.binanceRecommissionConfigArr,
            "limitTimeMaxPositionConfigArr":otherConfig.limitTimeMaxPositionConfigArr,
            "shieldLossSymbolConfigArr":otherConfig.shieldLossSymbolConfigArr,
            "serverUpdateTsConfigArr":parseInt(new Date().getTime()),
        }
        let formData = new FormData();
        formData.append("accessToken",userInfo["accessToken"]);
        formData.append("stateConfigObj",JSON.stringify(stateConfigObj));
        fetch(publicServerURL+"/modify_state_config", {
            method:'POST',
            body:formData
        }).then((response)=>{
            if (response.ok) {
                return response.json();
            }
        }).then((response)=>{
            if(response['s']=="error"){
                message.error("保存其他配置到服务器失败，请稍后重试")
            }else{
                this.setState({
                    serverStateConfig:response['stateConfigObj']
                })
                message.success("保存其他配置到服务器成功")
            }
        }).catch((error)=>{
            console.error(error)
        });
    }


    onChangeKlineRowCountConfigArr = (e)=>{
        const {otherConfig} = this.props
        let newKlineRowCountConfigArr = deepCopy(otherConfig.klineRowCountConfigArr)
        let value = e.target.value
        newKlineRowCountConfigArr[0] = value
        let storage=window.localStorage;
        storage["klineRowCountConfigArr"]=JSON.stringify(newKlineRowCountConfigArr)
        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            klineRowCountConfigArr:newKlineRowCountConfigArr
        })
    }
    onChangeSelectKlineIntervalArr = (value,index)=>{
        const {otherConfig} = this.props
        let newSelectKlineIntervalArr = deepCopy(otherConfig.selectKlineIntervalConfigArr)
        newSelectKlineIntervalArr[index] = value
        let storage=window.localStorage;
        storage["selectKlineIntervalConfigArr"]=JSON.stringify(newSelectKlineIntervalArr)
        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            selectKlineIntervalConfigArr:newSelectKlineIntervalArr
        })
    }


    getSelectCoinShowKlineInterval = (index)=>{

        const {otherConfig} = this.props
        return <Select value={otherConfig.selectKlineIntervalConfigArr[index]} onChange={(value)=>{this.onChangeSelectKlineIntervalArr(value,index)}} style={{width:250}}>
            {
                supportKlineIntervalEnglish.map((item,i)=>{
                    return <Option  key={i} value={item}>
                        图{index+1}-{supportKlineIntervalChinese[i]}
                    </Option >
                })
            }

        </Select>
    }


    onChangeBinanceAddressConfigArr= (e)=>{
        const {otherConfig} = this.props
        let newBinanceAddressConfigArr = deepCopy(otherConfig.binanceAddressConfigArr)
        let value = e.target.value
        newBinanceAddressConfigArr[0] = value
        let storage=window.localStorage;
        storage["binanceAddressConfigArr"]=JSON.stringify(newBinanceAddressConfigArr)
        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            binanceAddressConfigArr:newBinanceAddressConfigArr
        })

    }

    onChangeBinanceRecommissionConfigArr= (value)=>{
        const {otherConfig} = this.props
        let newBinanceRecommissionConfigArr = deepCopy(otherConfig.binanceRecommissionConfigArr)
        newBinanceRecommissionConfigArr[0] = value
        let storage=window.localStorage;
        storage["binanceRecommissionConfigArr"]=JSON.stringify(newBinanceRecommissionConfigArr)
        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            binanceRecommissionConfigArr:newBinanceRecommissionConfigArr
        })

    }

    onChangeSortFrequencyTsConfigArr= (value)=>{
        const {otherConfig} = this.props
        let newSortFrequencyTsConfigArr = deepCopy(otherConfig.sortFrequencyTsConfigArr)
        if(isNaN(value)){
            message.error("请输入数字")
            return
        }
        newSortFrequencyTsConfigArr[0] = parseInt(value)
        let storage=window.localStorage;
        storage["sortFrequencyTsConfigArr"]=JSON.stringify(newSortFrequencyTsConfigArr)
        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            sortFrequencyTsConfigArr:newSortFrequencyTsConfigArr
        })
    }

    onChangeDepthChartSizeIndexConfigArr= (value)=>{
        const {otherConfig} = this.props
        let newDepthConfigArr= deepCopy(otherConfig.depthConfigArr)
        if(value=="error"){
            return
        }
        newDepthConfigArr[1] = value
        let storage=window.localStorage;
        storage["depthConfigArr"]=JSON.stringify(newDepthConfigArr)
        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            depthConfigArr:newDepthConfigArr
        })
    }

    onChangeKlineCountConfigArr = (value)=>{
        const {otherConfig} = this.props
        let newKlineCountConfigArr = deepCopy(otherConfig.klineCountConfigArr)
        if(parseInt(value)>96){
            message.error("K图数量不能大于96")
            return
        }
        newKlineCountConfigArr[0] = value
        let storage=window.localStorage;
        storage["klineCountConfigArr"]=JSON.stringify(newKlineCountConfigArr)
        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            klineCountConfigArr:newKlineCountConfigArr
        })
    }


    onChangeDepthCountConfigArr= (e)=>{
        const {otherConfig} = this.props
        let newDepthConfigArr = deepCopy(otherConfig.depthConfigArr)
        let value = e.target.value
        if(parseInt(value)>=50){
            message.error("深度图数量不能大于50")
            return
        }
        newDepthConfigArr[0] = value
        let storage=window.localStorage;
        storage["depthConfigArr"]=JSON.stringify(newDepthConfigArr)
        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            depthConfigArr:newDepthConfigArr
        })
    }

    onChangeRocketLimitConfigArr = (value,index)=>{
        const {otherConfig} = this.props
        let storage=window.localStorage;
        let newRocketLimitConfigArr = deepCopy(otherConfig.rocketLimitConfigArr)
        newRocketLimitConfigArr[index]=value
        storage["rocketLimitConfigArr"]=JSON.stringify(newRocketLimitConfigArr)
        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            rocketLimitConfigArr:newRocketLimitConfigArr
        })
    }
    onChangeAutoBuyBnbA= (value)=>{
        const {otherConfig} = this.props
        let storage=window.localStorage;
        let newAutoBuyBnbConfigArr = deepCopy(otherConfig.autoBuyBnbConfigArr)
        newAutoBuyBnbConfigArr[0]=parseInt(e.target.value)
        storage["autoBuyBnbConfigArr"]=JSON.stringify(newAutoBuyBnbConfigArr)
        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            autoBuyBnbConfigArr:newAutoBuyBnbConfigArr
        })
    }

    onChangeAutoBuyBnbB= (value)=>{
        const {otherConfig} = this.props
        if(isNaN(value)){
            message.error("请输入数字")
            return
        }
        let storage=window.localStorage;
        let newAutoBuyBnbConfigArr = deepCopy(otherConfig.autoBuyBnbConfigArr)
        newAutoBuyBnbConfigArr[1]=parseInt(e.target.value)
        storage["autoBuyBnbConfigArr"]=JSON.stringify(newAutoBuyBnbConfigArr)

        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            autoBuyBnbConfigArr:newAutoBuyBnbConfigArr
        })
    }

    onChangeAutoBuyBnbC = (checked)=>{
        const {otherConfig} = this.props
        let storage=window.localStorage;
        let newAutoBuyBnbConfigArr = deepCopy(otherConfig.autoBuyBnbConfigArr)
        if(checked){
            Modal.info({
                okText:"了解",
                title: "自动购买BNB请务必详细阅读了解后使用",
                content:
                    <div style={{width:"100%",textAlign:"left"}}>
                        <div>
                            自动购买BNB开启后，API必须具备万向划转和现货交易的权限<br/><br/>
                            且U本位合约USDT余额大于购买BNB价值的110%，即设置bnb低于50美金时候，自动购买100美金bnb，需要u本位合约存有大于110美金，才能生效，且购买后会将现货内的所有usdt都转移到usdt合约<br/><br/>
                            自动购买BNB的具体逻辑为:<br/><br/>
                            1.从U本位合约转移需要的金额到现货市价购买BNB<br/><br/>
                            2.现货购买BNB<br/><br/>
                            3.现货购买的BNB和余下的USDT转移回U本位合约<br/><br/>
                        </div>
                    </div>,
                onOk:()=>{}
            });
        }

        newAutoBuyBnbConfigArr[2]=checked
        storage["autoBuyBnbConfigArr"]=JSON.stringify(newAutoBuyBnbConfigArr)
        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            autoBuyBnbConfigArr:newAutoBuyBnbConfigArr
        })
    }

    onChangeAutoStopLossConfigChecked = (checked)=>{
        const {otherConfig} = this.props
        let newAutoStopLossConfigArr = deepCopy(otherConfig.autoStopLossConfigArr)
        if(checked){
            Modal.info({
                okText:"了解",
                title: "交易功能请务必详细阅读了解后使用",
                content:
                    <div style={{width:"100%",textAlign:"left"}}>
                        <div>
                            自动止损开启后，并不是下单成交后，服务器立即发出止损订单<br/><br/>
                            出于效率等多重因素考虑，自动止损的具体逻辑为:<br/><br/>
                            1.任何仓位发生增长变化的时候开始计时<br/><br/>
                            2.十秒内没有新仓位增长<br/><br/>
                            3.该仓位的止损订单价值不足仓位价值的99%（即如果您手动挂出止损订单，则不会有自动止损订单）<br/><br/>
                            4.在此期间浏览器没有刷新等退出页面的操作<br/><br/>
                            5.如果点击了仓位上的止损按钮，开启了自定义止损小窗口，则在开启窗口以及关闭窗口后的十秒内，都不会执行自动止损<br/><br/>
                            满足以上条件<br/><br/>
                            会自动取消该交易对所有止损订单并重新按照自动止损的规则挂出止损订单<br/><br/>
                            <strong>市场行情波动极速剧烈时，我们强烈建议您使用快捷键止损挂单，防止十秒未到，价格就突破止损价格的情况出现</strong><br/><br/>
                            请务必注意，无论是自动止损还是手动止损，都存在没有成功挂出的可能性，您需要人工识别是否重新挂单
                        </div>
                    </div>,
                onOk:()=>{}
            });
        }

        newAutoStopLossConfigArr[2] = checked
        let storage=window.localStorage;
        storage["autoStopLossConfigArr"]=JSON.stringify(newAutoStopLossConfigArr)

        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            autoStopLossConfigArr:newAutoStopLossConfigArr
        })
    }

    onChangeAutoCancelStopLossConfigChecked = (checked)=>{
        const {otherConfig} = this.props
        let newAutoCancelStopLossConfigArr = deepCopy(otherConfig.autoCancelStopLossConfigArr)
        newAutoCancelStopLossConfigArr[0] = checked
        let storage=window.localStorage;
        storage["autoCancelStopLossConfigArr"]=JSON.stringify(newAutoCancelStopLossConfigArr)

        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            autoCancelStopLossConfigArr:newAutoCancelStopLossConfigArr
        })
    }

    onChangeAutoStopLossConfigValue = (value,index)=>{
        const {otherConfig} = this.props
        let newAutoStopLossConfigArr = deepCopy(otherConfig.autoStopLossConfigArr)
        newAutoStopLossConfigArr[1][index] = value
        let storage=window.localStorage;
        storage["autoStopLossConfigArr"]=JSON.stringify(newAutoStopLossConfigArr)

        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            autoStopLossConfigArr:newAutoStopLossConfigArr
        })
    }

    onChangeAutoStopLossConfigType = (value)=>{
        const {otherConfig} = this.props
        let newAutoStopLossConfigArr = deepCopy(otherConfig.autoStopLossConfigArr)
        newAutoStopLossConfigArr[0] = value
        let storage=window.localStorage;
        storage["autoStopLossConfigArr"]=JSON.stringify(newAutoStopLossConfigArr)

        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            autoStopLossConfigArr:newAutoStopLossConfigArr
        })
    }

    getAutoStopLossParaInput = ()=>{
        const {otherConfig} = this.props

        let autoStopLossType = otherConfig.autoStopLossConfigArr[0]
        let stopLossSuffix = "分钟"
        if(autoStopLossType=="percent"){
            stopLossSuffix = "%"
        }else if(autoStopLossType=="money"){
            stopLossSuffix = "USD"
        }


        if(autoStopLossType=="batch"){
            return <div style={{display: "flex",flexDirection: "row",alignItems: "center"}}>
                <InputNumber controls={false}  min={0.01} max={50}  precision={2} style={{marginLeft:64,width: 150}} value={otherConfig.autoStopLossConfigArr[1][0]} onChange={(value)=>{this.onChangeAutoStopLossConfigValue(value,0)}} prefix={"起始比例"} addonAfter={"%"}/>
                <InputNumber controls={false} precision={2} style={{marginLeft:64,width: 180}} value={otherConfig.autoStopLossConfigArr[1][1]} onChange={(value)=>{this.onChangeAutoStopLossConfigValue(value,1)}} prefix={"每单变化比例"} addonAfter={"%"}/>
                <InputNumber controls={false}  min={2} max={10}  precision={0} style={{marginLeft:64,width: 150}} value={otherConfig.autoStopLossConfigArr[1][2]} onChange={(value)=>{this.onChangeAutoStopLossConfigValue(value,2)}} prefix={"止损单数"} addonAfter={"单"}/>
            </div>
        }else if(autoStopLossType=="time"){
            return <InputNumber controls={false} max={720000} min={1} precision={0}  style={{marginLeft:64,width: 200}} value={otherConfig.autoStopLossConfigArr[1][0]} onChange={(value)=>{this.onChangeAutoStopLossConfigValue(value,0)}} addonAfter={stopLossSuffix}/>
        }else{
            return <InputNumber controls={false} min={0.01} max={50} precision={2}  style={{marginLeft:64,width: 200}} value={otherConfig.autoStopLossConfigArr[1][0]} onChange={(value)=>{this.onChangeAutoStopLossConfigValue(value,0)}} addonAfter={stopLossSuffix}/>
        }
    }

    onChangeLimitMaxPositionAmountA= (value)=>{
        const {otherConfig} = this.props
        let newLimitMaxPositionLockConfigArr = deepCopy(otherConfig.limitMaxPositionLockConfigArr)
        newLimitMaxPositionLockConfigArr[0] = value
        let storage=window.localStorage;
        storage["limitMaxPositionLockConfigArr"]=JSON.stringify(newLimitMaxPositionLockConfigArr)
        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            limitMaxPositionLockConfigArr:newLimitMaxPositionLockConfigArr
        })
    }

    onChangeLimitMaxPositionAmountB= (value)=>{
        const {otherConfig} = this.props
        let newLimitMaxPositionLockConfigArr = deepCopy(otherConfig.limitMaxPositionLockConfigArr)
        newLimitMaxPositionLockConfigArr[1] = value
        let storage=window.localStorage;
        storage["limitMaxPositionLockConfigArr"]=JSON.stringify(newLimitMaxPositionLockConfigArr)
        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            limitMaxPositionLockConfigArr:newLimitMaxPositionLockConfigArr
        })
    }

    onChangMindModeChecked = (checked)=>{
        const {otherConfig} = this.props
        let newMindModeConfigArr = deepCopy(otherConfig.mindModeConfigArr)
        newMindModeConfigArr[0] = checked
        let storage=window.localStorage;
        storage["mindModeConfigArr"]=JSON.stringify(newMindModeConfigArr)
        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            mindModeConfigArr:newMindModeConfigArr
        })
    }

    onChangeLimitMaxPositionChecked = (checked)=>{
        const {otherConfig} = this.props
        let newLimitMaxPositionLockConfigArr = deepCopy(otherConfig.limitMaxPositionLockConfigArr)
        newLimitMaxPositionLockConfigArr[2] = checked
        let storage=window.localStorage;
        storage["limitMaxPositionLockConfigArr"]=JSON.stringify(newLimitMaxPositionLockConfigArr)
        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            limitMaxPositionLockConfigArr:newLimitMaxPositionLockConfigArr
        })
    }


    getStopLossServerValue = ()=>{
        const {serverStateConfig} = this.state
        const {otherConfig} = this.props
        let stopLossTypeNameObj ={
            "percent":"按比例",
            "time":"按时间",
            "money":"按金额",
            "batch":"分批"
        }
        if("autoStopLossConfigArr" in serverStateConfig)
        {
            let autoStopLossConfigArr= serverStateConfig["autoStopLossConfigArr"]
            if(autoStopLossConfigArr[0]!="batch") {
                return <div style={{display: "flex",flexDirection: "row",}}>
                    {stopLossTypeNameObj[serverStateConfig["autoStopLossConfigArr"][0]]}，{serverStateConfig["autoStopLossConfigArr"][1][0]}，<Switch checkedChildren="开启" unCheckedChildren="关闭" checked={serverStateConfig["autoStopLossConfigArr"][2]} />

                </div>
            }else{
                return <div style={{display: "flex",flexDirection: "row",}}>
                    {stopLossTypeNameObj[serverStateConfig["autoStopLossConfigArr"][0]]}，{serverStateConfig["autoStopLossConfigArr"][1][0]}，
                    {serverStateConfig["autoStopLossConfigArr"][1][1]}，{serverStateConfig["autoStopLossConfigArr"][1][2]}，
                    <Switch checkedChildren="开启" unCheckedChildren="关闭" checked={serverStateConfig["autoStopLossConfigArr"][2]} />

                </div>
            }

        }
    }

    onChangeLimitMaxLossLockTime = (value)=>{
        let storage=window.localStorage;
        let maxLossLockTs = storage["maxLossLockTs"]?parseInt(storage["maxLossLockTs"]):0
        let nowTs = parseInt(new Date().getTime());
        if(nowTs< maxLossLockTs){

            message.error("单位时间最大亏损锁上锁中，解锁时间："+turnTsToTime(maxLossLockTs))
            return
        }
        const {otherConfig} = this.props
        let newLimitMaxLossLockConfigArr = deepCopy(otherConfig.limitMaxLossLockConfigArr)
        newLimitMaxLossLockConfigArr[0] = value
        storage["limitMaxLossLockConfigArr"]=JSON.stringify(newLimitMaxLossLockConfigArr)
        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            limitMaxLossLockConfigArr:newLimitMaxLossLockConfigArr
        })
    }

    onChangeShieldLossSymbolTime = (value)=>{
        let storage=window.localStorage;

        const {otherConfig} = this.props
        let newShieldLossSymbolConfigArr = deepCopy(otherConfig.shieldLossSymbolConfigArr)
        newShieldLossSymbolConfigArr[0] = value
        storage["shieldLossSymbolConfigArr"]=JSON.stringify(newShieldLossSymbolConfigArr)
        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            shieldLossSymbolConfigArr:newShieldLossSymbolConfigArr
        })
    }

    onChangeShieldLossSymbolLockChecked= (checked)=>{
        let storage=window.localStorage;
        const {otherConfig} = this.props
        let newShieldLossSymbolConfigArr = deepCopy(otherConfig.shieldLossSymbolConfigArr)
        newShieldLossSymbolConfigArr[3] = checked

        storage["shieldLossSymbolConfigArr"]=JSON.stringify(newShieldLossSymbolConfigArr)
        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            shieldLossSymbolConfigArr:newShieldLossSymbolConfigArr
        })
    }


    onChangeLimitMaxLossLockChecked = (checked)=>{
        let storage=window.localStorage;
        let maxLossLockTs = storage["maxLossLockTs"]?parseInt(storage["maxLossLockTs"]):0
        let nowTs = parseInt(new Date().getTime());
        if(nowTs< maxLossLockTs){

            message.error("单位时间最大亏损锁上锁中，解锁时间："+turnTsToTime(maxLossLockTs))
            return
        }
        const {otherConfig} = this.props
        let newLimitMaxLossLockConfigArr = deepCopy(otherConfig.limitMaxLossLockConfigArr)
        newLimitMaxLossLockConfigArr[3] = checked

        storage["limitMaxLossLockConfigArr"]=JSON.stringify(newLimitMaxLossLockConfigArr)
        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            limitMaxLossLockConfigArr:newLimitMaxLossLockConfigArr
        })
    }

    onChangeLimitMaxLossLockMoney = (value)=>{
        let storage=window.localStorage;
        let maxLossLockTs = storage["maxLossLockTs"]?parseInt(storage["maxLossLockTs"]):0
        let nowTs = parseInt(new Date().getTime());
        if(nowTs< maxLossLockTs){

            message.error("单位时间最大亏损锁上锁中，解锁时间："+turnTsToTime(maxLossLockTs))
            return
        }
        const {otherConfig} = this.props
        let newLimitMaxLossLockConfigArr = deepCopy(otherConfig.limitMaxLossLockConfigArr)
        newLimitMaxLossLockConfigArr[1] = value

        storage["limitMaxLossLockConfigArr"]=JSON.stringify(newLimitMaxLossLockConfigArr)
        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            limitMaxLossLockConfigArr:newLimitMaxLossLockConfigArr
        })
    }

    onChangeShieldLossSymbolLockMoney = (value)=>{
        let storage=window.localStorage;
        const {otherConfig} = this.props
        let newShieldLossSymbolConfigArr = deepCopy(otherConfig.shieldLossSymbolConfigArr)
        newShieldLossSymbolConfigArr[1] = value

        storage["shieldLossSymbolConfigArr"]=JSON.stringify(newShieldLossSymbolConfigArr)
        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            shieldLossSymbolConfigArr:newShieldLossSymbolConfigArr
        })
    }

    onChangeShieldLossSymbolLockMins= (value)=>{
        let storage=window.localStorage;
        const {otherConfig} = this.props
        let newLimitShieldLossSymbolConfigArr = deepCopy(otherConfig.shieldLossSymbolConfigArr)
        newLimitShieldLossSymbolConfigArr[2] = value
        storage["shieldLossSymbolConfigArr"]=JSON.stringify(newLimitShieldLossSymbolConfigArr)
        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            shieldLossSymbolConfigArr:newLimitShieldLossSymbolConfigArr
        })
    }

    onChangeLimitMaxLossLockMins = (value)=>{
        let storage=window.localStorage;
        let maxLossLockTs = storage["maxLossLockTs"]?parseInt(storage["maxLossLockTs"]):0
        let nowTs = parseInt(new Date().getTime());
        if(nowTs< maxLossLockTs){

            message.error("单位时间最大亏损锁上锁中，解锁时间："+turnTsToTime(maxLossLockTs))
            return
        }
        const {otherConfig} = this.props
        let newLimitMaxLossLockConfigArr = deepCopy(otherConfig.limitMaxLossLockConfigArr)
        newLimitMaxLossLockConfigArr[2] = value
        storage["limitMaxLossLockConfigArr"]=JSON.stringify(newLimitMaxLossLockConfigArr)
        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            limitMaxLossLockConfigArr:newLimitMaxLossLockConfigArr
        })
    }

    onChangeAutoCancelOrderTs = (value)=>{
        let storage=window.localStorage;
        const {otherConfig} = this.props
        let newAutoCancelOrderConfigArr = deepCopy(otherConfig.autoCancelOrderConfigArr)
        newAutoCancelOrderConfigArr[0] = value
        storage["limitMaxLossLockConfigArr"]=JSON.stringify(newAutoCancelOrderConfigArr)
        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            autoCancelOrderConfigArr:newAutoCancelOrderConfigArr
        })
    }

    onChangeAutoCancelOrderChecked= (checked)=>{
        const {otherConfig} = this.props
        let newAutoCancelOrderConfigArr = deepCopy(otherConfig.autoCancelOrderConfigArr)
        newAutoCancelOrderConfigArr[1] = checked
        let storage=window.localStorage;
        storage["autoCancelOrderConfigArr"]=JSON.stringify(newAutoCancelOrderConfigArr)
        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            autoCancelOrderConfigArr:newAutoCancelOrderConfigArr
        })
    }


    onChangShowProfitWithLeverChecked= (checked)=>{
        const {otherConfig} = this.props
        let newShowProfitWithLeverConfigArr = deepCopy(otherConfig.showProfitWithLeverConfigArr)
        newShowProfitWithLeverConfigArr[0] = checked
        let storage=window.localStorage;
        storage["showProfitWithLeverConfigArr"]=JSON.stringify(newShowProfitWithLeverConfigArr)
        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            showProfitWithLeverConfigArr:newShowProfitWithLeverConfigArr
        })
    }

    onChangeDepthProfitChecked= (checked)=>{
        const {otherConfig} = this.props
        let newDepthConfigArr = deepCopy(otherConfig.depthConfigArr)
        newDepthConfigArr[2] = checked
        let storage=window.localStorage;
        storage["depthConfigArr"]=JSON.stringify(newDepthConfigArr)
        this.props.modifyOtherConfig({
            ...this.props.otherConfig,
            depthConfigArr:newDepthConfigArr
        })
    }

    explainModal = ()=>{
        Modal.info({
            okText:"了解",
            title:"其他配置帮助文档",
            content:
                <div style={{width:"100%",textAlign:"left"}}>
                    <Collapse accordion>
                        <Panel header="自动止损" key="1">
                            自动止损开启后，并不是下单成交后，服务器立即发出止损订单<br/><br/>
                            出于效率等多重因素考虑，自动止损的具体逻辑为:<br/><br/>
                            1.任何仓位发生增长变化的时候开始计时<br/><br/>
                            2.十秒内没有新仓位增长<br/><br/>
                            3.该仓位的止损订单价值不足仓位价值的99%（即如果您手动挂出止损订单，则不会有自动止损订单）<br/><br/>
                            4.在此期间浏览器没有刷新等退出页面的操作<br/><br/>
                            满足以上条件<br/><br/>
                            会自动取消该交易对所有止损订单并重新按照自动止损的规则挂出止损订单<br/><br/>
                            如您要了解各个止损类型和其参数的详细意义，请打开快捷键设置窗口，调增下方新增快捷键为止盈止损后阅读<br/><br/>
                            <strong>市场行情波动极速剧烈时，我们强烈建议您使用快捷键止损挂单，防止十秒未到，价格就突破止损价格的情况出现</strong><br/><br/>
                            请务必注意，无论是自动止损还是手动止损，都存在没有成功挂出的可能性，您需要人工识别是否重新挂单
                        </Panel>
                        <Panel header="自动取消止盈止损" key="2">
                            开启后会自动取消没有仓位的币种的所有止盈止损订单
                        </Panel>
                        <Panel header="自动取消快捷键挂单" key="3">
                            开启后会自动取消现在的时间-挂单发出时间>设定的秒数 的快捷键发出的，根据盘口深度计算的挂单，左侧逆势，右侧突破，以及图表的计划开仓不受影响<br/><br/>
                            请注意，该功能为本地端实现，如本地段网络问题，或者关闭浏览器，都将导致失效
                        </Panel>


                        <Panel header="自动购买BNB" key="4">
                            自动购买BNB开启后，API必须具备万向划转和现货交易的权限<br/><br/>
                            且U本位合约USDT余额大于购买BNB价值的110%，即设置bnb低于50美金时候，自动购买100美金bnb，需要u本位合约存有大于110美金，才能生效，且购买后会将现货内的所有usdt都转移到usdt合约<br/><br/>
                            自动购买BNB的具体逻辑为:<br/><br/>
                            1.从U本位合约转移需要的金额到现货市价购买BNB<br/><br/>
                            2.现货购买BNB<br/><br/>
                            3.现货购买的BNB和余下的USDT转移回U本位合约<br/><br/>
                        </Panel>

                        <Panel header="1分钟急速涨跌幅提示" key="5">
                            设置后，如果最近一条一分钟或上一条一分钟线涨幅或者跌幅超过设置的百分比数值，交易对会提权排序并且显示火箭图标<br/><br/>
                            跌幅设置不需要加负号，设置为0表示取消该项设置<br/><br/>
                        </Panel>
                        <Panel header="最大仓位锁" key="6">
                            仓位锁开启后，所有交易对仓位总额加所有同方向挂单大设置的于总仓位，或者单个交易对仓位总额加其所有同方向挂单大于该交易对设定的最大值，交易上锁则会开启<br/><br/>
                            当挂单被取消或总额下降，低于设定值，会自动解锁<br/><br/>
                            上锁时，将无法新开仓，止盈止损，平仓和取消挂单操作不受影响<br/><br/>
                            请注意，仓位锁是指当前仓位大于等于设置的额度才上锁，并无法保证开仓仓位一定小于等于仓位锁设置的额度<br/><br/>
                            例如您设置了仓位锁为5000美金，当前仓位价值为4999美金，您单笔投注价值10000美金，则您仍可以开出14999美金的仓位
                        </Panel>
                        <Panel header="亏损冷静锁" key="7">
                            亏损锁用户设定的单位时间内，用户亏损金额大于设定值，交易上锁会自动开启<br/><br/>
                            时间到期后，会继续判断单位时间内亏损金额是否大于设定值，如是，则继续续期，在上锁期间，无法对亏损冷静锁配置进行任何修改<br/><br/>
                            从上锁时候开始算起，超出用户设定的时间间隔，会自动解锁<br/><br/>
                            建议上锁的等待时间不要小于单位亏损计算时间，因为如果解锁后，单位时间亏损值还是大于设定值，那么还是会继续上锁<br/><br/>
                            打个比方，在2022-11-19晚上8点，您设置了24小时亏损超过500 USD就停止15分钟<br/><br/>
                            在20：45分到20：50分您亏损了500U，那么实际上您的等待时间不是15分钟，而是24小时，这是因为15分钟到期后，24小时亏损额依然大于设定值<br/><br/>
                            更合理的设定是 设置了15分钟亏损超过500 USD就停止15分钟<br/><br/>
                            上锁时，将无法新开仓，止盈止损，平仓和取消挂单操作不受影响<br/><br/>
                        </Panel>
                        <Panel header="仓位收益率乘以杠杆" key="8">
                            即下方仓位收益率显示的时候是否要乘以当前交易对的杠杆<br/><br/>
                            选择否的时候，将以币种基准价格的涨跌幅度作为收益率显示
                        </Panel>
                        <Panel header="排序刷新时间" key="9">
                            排序刷新时间指的是下方K线图多少毫秒，会按照规则重新排序<br/><br/>
                            排序是于本地端处理<br/><br/>
                            过低的排序刷新时间既会导致机器功耗增加，更重要的是会导致使用体验不佳，请自行决策<br/><br/>
                            我们建议使用3~5秒的自动刷新时间，以及遇到极端情况的时候，使用手动强制刷新（默认小键盘0）
                        </Panel>
                        <Panel header="选中币种Kline图" key="10">
                            通过此可以调节选中币种最上方三个K线图的时间间隔
                        </Panel>
                        <Panel header="K线图线条数" key="11">
                            K线图条数指的是下方K线图一共有多少条线，最高为96条
                        </Panel>
                        <Panel header="深度图配置" key="12">
                            第一个开关开启后，深度图会在具有该交易对仓位的时候，自动转化为距离仓位成本价百分比的模式，其余两个配置主要是外观，以适配一些显示器
                        </Panel>
                        <Panel header="K线图数" key="13">
                            K线图数会影响下方K线图一行有几张
                        </Panel>
                        <Panel header="专注模式" key="14">
                            开启之后，将隐藏所有的收益率，收益及账号信息，让您免受收益数字跳动的干扰，专心于交易
                        </Panel>
                        <Panel header="币安手续费返佣比例" key="15">
                            您的币安手续费返佣比例，如果没有请输入0，该值会影响统计数据中的手续费和净利润
                        </Panel>
                        <Panel header="币安网页地址" key="16">
                            币安网页设置会影响按o（默认）打开选中币种的币安交易网页，币安网址的前缀
                        </Panel>
                    </Collapse>
                </div>,
            onOk:()=>{}
        });
    }
    getOtherConfigModal=()=>{
        const {serverStateConfig} = this.state;
        const {shieldLossSymbolConfigArr,mindModeConfigArr,autoStopLossConfigArr,autoCancelStopLossConfigArr,limitMaxLossLockConfigArr,showProfitWithLeverConfigArr,rocketLimitConfigArr,autoCancelOrderConfigArr,binanceRecommissionConfigArr} = this.props.otherConfig;
        const {otherConfig} = this.props


        const stopLossTypeArr=[{"name":"比例止损","value":"percent"},{"name":"金额止损","value":"money"},{"name":"时间止损","value":"time"},{"name":"分批止损","value":"batch"}]
        let titleStyle = {display: "flex",flexDirection: "row",alignItems: "center"}
        const otherConfigTableDataArr = [
            {
                "name":"设置自动止损",
                "value":<div style={{display: "flex",flexDirection: "row",alignItems: "center"}}>
                    <Select value={autoStopLossConfigArr[0]} onChange={(value)=>{this.onChangeAutoStopLossConfigType(value)}} style={{width:250}}>
                        {
                            stopLossTypeArr.map((item,i)=>{
                                return <Option  key={i} value={item["value"]}>
                                    {item["name"]}
                                </Option >
                            })
                        }

                    </Select>
                    {this.getAutoStopLossParaInput()}
                    <Switch checkedChildren="开启" unCheckedChildren="关闭" style={{marginLeft:64}} checked={autoStopLossConfigArr[2]} onChange={this.onChangeAutoStopLossConfigChecked} />
                </div>,
                "serverValue":this.getStopLossServerValue()
            },
            {
                "name":"自动取消盘口型挂单",
                "value":<div style={{display: "flex",flexDirection: "row",alignItems:"center"}}>
                    <div  >
                        <InputNumber  controls={false}  min={1} max={100000000} precision={0} prefix={"超过"} addonAfter={"秒"} style={{width: 250}} value={autoCancelOrderConfigArr[0]} onChange={this.onChangeAutoCancelOrderTs}/>
                    </div>
                    <div style={{marginLeft:64}} >
                        <Switch checkedChildren="开启" unCheckedChildren="关闭" checked={autoCancelOrderConfigArr[1]} onChange={this.onChangeAutoCancelOrderChecked} />
                    </div>
                </div>,
                "serverValue":("autoCancelOrderConfigArr" in serverStateConfig)&&<div style={{display: "flex",flexDirection: "row",}}>{serverStateConfig["autoCancelOrderConfigArr"][0]}，<Switch checkedChildren="开启" unCheckedChildren="关闭"checked={serverStateConfig["autoCancelOrderConfigArr"][1]} /></div>
            },
            {
                "name":"自动取消止盈止损",
                "value":<Switch checkedChildren="开启" unCheckedChildren="关闭"  checked={autoCancelStopLossConfigArr[0]} onChange={this.onChangeAutoCancelStopLossConfigChecked} />,
                "serverValue":("autoCancelStopLossConfigArr" in serverStateConfig)&&<Switch checkedChildren="开启" unCheckedChildren="关闭" checked={serverStateConfig["autoCancelStopLossConfigArr"][0]} />
            },

            {
                "name":"急速涨跌幅提示",
                "value":<div style={{display: "flex",flexDirection: "row",alignItems:"center"}}>
                    <InputNumber controls={false}  min={0} max={5} precision={0} addonAfter={"分钟"} style={{width: 250}} value={otherConfig.rocketLimitConfigArr[0]} onChange={(value)=>{this.onChangeRocketLimitConfigArr(value,0)}}/>
                    <InputNumber controls={false}  min={0} max={100} precision={2} prefix={"涨幅"} addonAfter={"%"} style={{marginLeft:64,width: 250}} value={otherConfig.rocketLimitConfigArr[1]} onChange={(value)=>{this.onChangeRocketLimitConfigArr(value,1)}}/>
                    <InputNumber controls={false}  min={0} max={100} precision={2} prefix={"跌幅"} addonAfter={"%"} style={{marginLeft:64,width: 250}} value={otherConfig.rocketLimitConfigArr[2]} onChange={(value)=>{this.onChangeRocketLimitConfigArr(value,2)}}/>
                    <a onClick={()=>{audio.play()}} style={{marginLeft:64,width: 250}}> 测试声音</a>
                </div>,
                "serverValue":("rocketLimitConfigArr" in serverStateConfig)&&<div style={{display: "flex",flexDirection: "row",}}>{serverStateConfig["rocketLimitConfigArr"][0]}，{serverStateConfig["rocketLimitConfigArr"][1]}， {serverStateConfig["rocketLimitConfigArr"][2]}</div>
            },
            {
                "name":"自动购买BNB",
                "value":<div style={{display: "flex",flexDirection: "row",alignItems:"center"}}>

                    <InputNumber controls={false}  min={10} precision={0} prefix={"BNB价值低于"} addonAfter={"USD"} style={{width: 250}} value={otherConfig.autoBuyBnbConfigArr[0]} onChange={this.onChangeAutoBuyBnbA}/>
                    <InputNumber controls={false} precision={0} min={15} precision={0}  prefix={"自动购买"} addonAfter={"USD的BNB"} style={{marginLeft:64,width: 250}} value={otherConfig.autoBuyBnbConfigArr[1]} onChange={this.onChangeAutoBuyBnbB}/>
                    <Switch checkedChildren="开启" unCheckedChildren="关闭" style={{marginLeft:64}} checked={otherConfig.autoBuyBnbConfigArr[2]} onChange={this.onChangeAutoBuyBnbC} />
                </div>,
                "serverValue":("autoBuyBnbConfigArr" in serverStateConfig)&&<div style={{display: "flex",flexDirection: "row",}}>{serverStateConfig["autoBuyBnbConfigArr"][0]}，{serverStateConfig["autoBuyBnbConfigArr"][1]}，<Switch checkedChildren="开启" unCheckedChildren="关闭"checked={serverStateConfig["autoBuyBnbConfigArr"][2]} /></div>
            },
            {
                "name":"最大总仓位锁",
                "value":<div style={{display: "flex",flexDirection: "row",alignItems:"center"}}>
                    <InputNumber style={{width: 250}} controls={false}  precision={0} max={100000000} min={1} prefix={"总仓位大于"} addonAfter={"USD上锁"} value={otherConfig.limitMaxPositionLockConfigArr[0]} onChange={this.onChangeLimitMaxPositionAmountA}/>
                    <InputNumber style={{marginLeft:64,width: 250}} controls={false}  precision={0} max={100000000} min={1} prefix={"单币种仓位大于"} addonAfter={"USD上锁"} value={otherConfig.limitMaxPositionLockConfigArr[1]} onChange={this.onChangeLimitMaxPositionAmountB}/>
                    <Switch checkedChildren="开启" unCheckedChildren="关闭" style={{marginLeft:64}} checked={otherConfig.limitMaxPositionLockConfigArr[2]} onChange={this.onChangeLimitMaxPositionChecked} /></div>,
                "serverValue":("limitMaxPositionLockConfigArr" in serverStateConfig)&&
                    <div style={{display: "flex",flexDirection: "row",}}>{serverStateConfig["limitMaxPositionLockConfigArr"][0]}，{serverStateConfig["limitMaxPositionLockConfigArr"][1]}，
                        <Switch checkedChildren="开启" unCheckedChildren="关闭"checked={serverStateConfig["limitMaxPositionLockConfigArr"][2]} />
                    </div>
            },
            {
                "name":"亏损冷静锁",
                "value":<div style={{display: "flex",flexDirection: "row",alignItems:"center"}}>
                    <div>
                        <Select value={limitMaxLossLockConfigArr[0]} onChange={(value)=>{this.onChangeLimitMaxLossLockTime(value)}} style={{width:250}}>
                            <Option  key={0} value={"15m"}>15分钟内</Option >
                            <Option  key={1} value={"30m"}>30分钟内</Option >
                            <Option  key={2} value={"1h"}>1小时内</Option >
                            <Option  key={3} value={"4h"}>4小时内</Option >
                            <Option  key={4} value={"oneDay"}>24小时内</Option >
                            <Option  key={4} value={"today"}>今天</Option >
                        </Select>
                    </div>

                    <div style={{marginLeft:64}} >
                        <InputNumber  controls={false}  min={1} max={100000000} precision={0} prefix={"亏损金额超过"} addonAfter={"USD"} style={{width: 250}} value={limitMaxLossLockConfigArr[1]} onChange={this.onChangeLimitMaxLossLockMoney}/>
                    </div>

                    <div style={{marginLeft:64}} >
                        <InputNumber  controls={false}  min={1} max={100000000} precision={0} prefix={"暂停"} addonAfter={"分钟"} style={{width: 250}} value={limitMaxLossLockConfigArr[2]} onChange={this.onChangeLimitMaxLossLockMins}/>
                    </div>
                    <div style={{marginLeft:64}} >
                        <Switch checkedChildren="开启" unCheckedChildren="关闭" checked={limitMaxLossLockConfigArr[3]} onChange={this.onChangeLimitMaxLossLockChecked} />
                    </div>
                </div>,
                "serverValue":("limitMaxLossLockConfigArr" in serverStateConfig)&&<div style={{display: "flex",flexDirection: "row",}}>{serverStateConfig["limitMaxLossLockConfigArr"][0]}，{serverStateConfig["limitMaxLossLockConfigArr"][1]}，{serverStateConfig["limitMaxLossLockConfigArr"][2]}，<Switch checkedChildren="开启" unCheckedChildren="关闭"checked={serverStateConfig["limitMaxLossLockConfigArr"][3]} /></div>
            },
            {
                "name":"交易对亏损屏蔽",
                "value":<div style={{display: "flex",flexDirection: "row",alignItems:"center"}}>
                    <div>
                        <Select value={shieldLossSymbolConfigArr[0]} onChange={(value)=>{this.onChangeShieldLossSymbolTime(value)}} style={{width:250}}>
                            <Option  key={0} value={"15m"}>15分钟内</Option >
                            <Option  key={1} value={"30m"}>30分钟内</Option >
                            <Option  key={2} value={"1h"}>1小时内</Option >
                            <Option  key={3} value={"4h"}>4小时内</Option >
                            <Option  key={4} value={"oneDay"}>24小时内</Option >
                            <Option  key={4} value={"today"}>今天</Option >
                        </Select>
                    </div>

                    <div style={{marginLeft:64}} >
                        <InputNumber  controls={false}  min={1} max={100000000} precision={0} prefix={"亏损金额超过"} addonAfter={"USD"} style={{width: 250}} value={shieldLossSymbolConfigArr[1]} onChange={this.onChangeShieldLossSymbolLockMoney}/>
                    </div>

                    <div style={{marginLeft:64}} >
                        <InputNumber  controls={false}  min={1} max={100000000} precision={0} prefix={"暂停"} addonAfter={"分钟"} style={{width: 250}} value={shieldLossSymbolConfigArr[2]} onChange={this.onChangeShieldLossSymbolLockMins}/>
                    </div>
                    <div style={{marginLeft:64}} >
                        <Switch checkedChildren="开启" unCheckedChildren="关闭" checked={shieldLossSymbolConfigArr[3]} onChange={this.onChangeShieldLossSymbolLockChecked} />
                    </div>
                </div>,
                "serverValue":("shieldLossSymbolConfigArr" in serverStateConfig)&&<div style={{display: "flex",flexDirection: "row",}}>{serverStateConfig["shieldLossSymbolConfigArr"][0]}，{serverStateConfig["shieldLossSymbolConfigArr"][1]}，{serverStateConfig["shieldLossSymbolConfigArr"][2]}，<Switch checkedChildren="开启" unCheckedChildren="关闭"checked={serverStateConfig["shieldLossSymbolConfigArr"][3]} /></div>
            },
            {
                "name":"深度图配置",
                "value":<div style={{display: "flex",flexDirection: "row",alignItems:"center"}}>
                    <InputNumber controls={false}  min={0} max={2} precision={2} prefix={"大小系数"} addonAfter={"（>0且<2）"} style={{width: 250}} value={otherConfig.depthConfigArr[1]} onChange={this.onChangeDepthChartSizeIndexConfigArr}/>
                    <InputNumber controls={false} precision={0} prefix={"数量"} suffix={"（<=50）"} style={{marginLeft:64,width: 250}} value={otherConfig.depthConfigArr[0]} onChange={this.onChangeDepthCountConfigArr}/>
                    <Switch style={{marginLeft:64}} checkedChildren="收益率化" unCheckedChildren="关闭" checked={otherConfig.depthConfigArr[2]} onChange={this.onChangeDepthProfitChecked} />
                </div>,
                "serverValue":("depthConfigArr" in serverStateConfig)&&<div style={{display: "flex",flexDirection: "row",}}>{serverStateConfig["depthConfigArr"][1]}，{serverStateConfig["depthConfigArr"][0]}，<Switch checkedChildren="开启" unCheckedChildren="关闭"checked={serverStateConfig["depthConfigArr"][2]} /></div>
            },

            {
                "name":"仓位收益率乘以杠杆",
                "value":<div >
                    <Switch checkedChildren="开启" unCheckedChildren="关闭" checked={showProfitWithLeverConfigArr[0]} onChange={this.onChangShowProfitWithLeverChecked} />
                </div>,
                "serverValue":("showProfitWithLeverConfigArr" in serverStateConfig)&&<Switch checkedChildren="是" unCheckedChildren="否" checked={serverStateConfig["showProfitWithLeverConfigArr"][0]}  />
            },
            {
                "name":"排序刷新时间",
                "value":<InputNumber controls={false} precision={0}  style={{width: 250}} value={otherConfig.sortFrequencyTsConfigArr[0]} onChange={this.onChangeSortFrequencyTsConfigArr} addonAfter="毫秒（1000=1秒）"/>,
                "serverValue":("sortFrequencyTsConfigArr" in serverStateConfig)&&serverStateConfig["sortFrequencyTsConfigArr"][0]
            },

            {
                "name":"选中币种Kline图",
                "value":
                    <div style={{display: "flex",flexDirection: "row",alignItems:"center"}}>
                        {this.getSelectCoinShowKlineInterval(0)}
                        <div style={{marginLeft:64,marginTop:4}}></div> {this.getSelectCoinShowKlineInterval(1)}
                        <div style={{marginLeft:64,marginTop:4}}></div> {this.getSelectCoinShowKlineInterval(2)}
                    </div>,
                "serverValue":("selectKlineIntervalConfigArr" in serverStateConfig)&&
                    <div style={{display: "flex",flexDirection: "row",}}>
                        {serverStateConfig["selectKlineIntervalConfigArr"][0]}， {serverStateConfig["selectKlineIntervalConfigArr"][1]}， {serverStateConfig["selectKlineIntervalConfigArr"][2]}
                    </div>
            },
            {
                "name":"K线图线条数",
                "value":<InputNumber max={96} min={1} precision={0} addonAfter={"（<=96）"} style={{width: 250}} onBlur={this.props.wsSendFun} value={otherConfig.klineCountConfigArr[0]} onChange={this.onChangeKlineCountConfigArr}/>,
                "serverValue":("klineCountConfigArr" in serverStateConfig)&&serverStateConfig["klineCountConfigArr"][0]
            },

            {
                "name":"K线图数",
                "value":<Radio.Group optionType="button" buttonStyle="solid" value={otherConfig.klineRowCountConfigArr[0]} onChange={this.onChangeKlineRowCountConfigArr}>
                    <Radio.Button value={1}>2图</Radio.Button>
                    <Radio.Button value={3}>3图</Radio.Button>
                    <Radio.Button value={4}>4图</Radio.Button>
                    <Radio.Button value={5}>5图</Radio.Button>
                    <Radio.Button value={6}>6图</Radio.Button>
                    <Radio.Button value={7}>7图</Radio.Button>
                    <Radio.Button value={8}>8图</Radio.Button>
                    <Radio.Button value={9}>9图</Radio.Button>
                    <Radio.Button value={10}>10图</Radio.Button>
                </Radio.Group>,
                "serverValue":("klineRowCountConfigArr" in serverStateConfig)&&serverStateConfig["klineRowCountConfigArr"][0]
            },
            {
                "name":"专注模式",
                "value":<div >
                    <Switch checkedChildren="开启" unCheckedChildren="关闭" checked={mindModeConfigArr[0]} onChange={this.onChangMindModeChecked} />
                </div>,
                "serverValue":("mindModeConfigArr" in serverStateConfig)&&<Switch checkedChildren="是" unCheckedChildren="否" checked={serverStateConfig["mindModeConfigArr"][0]}  />
            },
            {
                "name":"币安手续费返佣比例",
                "value":<InputNumber  controls={false}  min={0} max={250} precision={0} prefix={"手续费返佣百分比"} addonAfter={"%"} style={{width: 200}} value={binanceRecommissionConfigArr[0]} onChange={this.onChangeBinanceRecommissionConfigArr}/>,
                "serverValue":("binanceAddressConfigArr" in serverStateConfig)&&serverStateConfig["binanceAddressConfigArr"][0]
            },
            {
                "name":"币安网页地址",
                "value":<Input style={{width: 250}} value={otherConfig.binanceAddressConfigArr[0]} onChange={this.onChangeBinanceAddressConfigArr}/>,
                "serverValue":("binanceAddressConfigArr" in serverStateConfig)&&serverStateConfig["binanceAddressConfigArr"][0]
            }
        ]
        return (
            <Modal width={1600} destroyOnClose={true} title="其他配置修改（修改即时生效，本地保存，需云端保存恢复请手动处理）" visible={this.props.otherConfigModalVisible}
                   onCancel={() => {
                       // this.modifyStateConfig()
                       this.props.cancelOtherConfigModal()
                   }} footer={[
                null
            ]}>

                    <div style={{width:1600,padding:32}}>
                        <Table size={"small"} dataSource={otherConfigTableDataArr} columns={otherConfigTableColumns}
                               pagination={false}/>
                    </div>
                    <div style={{
                        display: "flex",
                        flexDirection: "row",
                        justifyContent: "center",
                        alignItems: "center",width:1600,padding:0}}>
                        <div style={{marginLeft:64}}>
                            <Button type={"primary"} style={{textDecoration:"underline",marginTop:32}} onClick={()=>{this.modifyStateConfig()}}>保存当前配置到服务器</Button>

                        </div>
                        <div style={{marginLeft:64}}>
                            <Button style={{textDecoration:"underline",marginTop:32}} onClick={()=>{this.restoreServerStateConfig()}}>恢复为服务端其他配置</Button>

                        </div>
                        <div style={{marginLeft:64}}>
                            <Button style={{textDecoration:"underline",marginTop:32}} onClick={()=>{this.restoreDefaultStateConfig()}}>恢复系统默认其他配置</Button>

                        </div>
                        <div style={{paddingTop:34,marginLeft:64}}>
                            <a onClick={()=>{this.explainModal()}} style={{textDecoration:"underline"}}>使用前请点此阅读详细文档，确保您完全理解该功能的逻辑和风险</a>

                        </div>
                    </div>

            </Modal>
        )




    }

    render() {
        if(this.props.otherConfigModalVisible){
            return this.getOtherConfigModal()
        }else{
            return <div></div>
        }


    }
}
const mapStateToProps = (state) => {
    return ({
        otherConfig:state.otherConfig,
        userInfo:state.userInfo,

    });
};
const mapDispatchToProps  = (dispatch, ownProps) => {
    return bindActionCreators({
        updateIfUpdateChatModalView:action.updateIfUpdateChatModalView,
        updateChat:action.updateChat,
        changeUserInfo:action.changeUserInfo,
        modifyOtherConfig:action.modifyOtherConfig
    }, dispatch);
};
export default connect(mapStateToProps,mapDispatchToProps)(OtherConfigModal);
