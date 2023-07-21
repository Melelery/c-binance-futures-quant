import React from 'react';
import {
    CloseOutlined,
    EditOutlined
} from '@ant-design/icons';
import { Button,Upload,InputNumber,Radio,Slider,Tag,Input,Pagination,Collapse,Avatar,message,Select,Modal,Checkbox,Alert,Switch } from 'antd';
import {coinArr,coinChineseObj} from "../constants/coinType";
import {connect} from "react-redux";
import * as action from "../actions";
import {bindActionCreators} from "redux";
import {addSelectTypeArr,addSelectTypeObj,keyboardObj, realHotKeyConfigDefaultObj,keyboardFunArr,sortTypeObj} from '../constants/hotkey'
import {deepCopy} from '../constants/commonFunction'
const { Option } = Select;
const { TextArea } = Input;
import {publicServerURL} from "../constants/serverURL";

class HotKeyModal extends React.Component {
    constructor(props) {
        super(props);
        let storage=window.localStorage;
        let addSelectType = storage["addSelectType"]?storage["addSelectType"]:"all"
        let addConfigParaArr = storage["addConfigParaArr"]?JSON.parse(storage["addConfigParaArr"]):[]
        let addConfigFunIndex = storage["addConfigFunIndex"]?parseInt(storage["addConfigFunIndex"]):0
        this.state = {
            modifyConfigKey:"",
            modifyHotKeyConfigModalVisible:false,
            modifyConfigParaArr:[],
            addConfigKeyCodeChange:false,
            addConfigKeyCode:"",
            addConfigFunIndex:addConfigFunIndex,
            addConfigParaArr:[],
            addSelectType:addSelectType

        };
    }

    componentDidMount=() =>{
        document.addEventListener("keydown", this.onKeyDown)
    }


    onKeyDown = (e) => {
        if(this.state.addConfigKeyCodeChange){
            const {userInfo} = this.props;
            let hotKeyConfigObj = userInfo["hotKeyConfigObj"]
            if(hotKeyConfigObj[e.keyCode]){
                message.error("该按键已绑定其他功能，如需绑定请先删除")
                return
            }
            let keyName = ""
            Object.keys(keyboardObj).forEach((key) => {
                if(e.keyCode==key){
                    keyName = key

                }
            })
            if(keyName==""){
                message.error("F1~F12，以及windows功能键无法设置为快捷键，注意输入法应切换为英文输入法")
                return
            }
            message.info("成功输入: "+keyboardObj[e.keyCode])
            this.setState({
                addConfigKeyCode:e.keyCode
            })
        }

    }

    onblurConfigKeyCode = ()=>{
        this.setState({
            addConfigKeyCodeChange:false
        })
    }

    onfocusConfigKeyCode = ()=>{
        message.info("请直接输入需要绑定的按键，无需删除",10)
        this.setState({
            addConfigKeyCodeChange:true
        })
    }
    onChangeParaInput = (value,index)=>{
        const {addConfigFunIndex} = this.state
        let newAddConfigParaArr = deepCopy(this.state.addConfigParaArr)
        newAddConfigParaArr[index] = value
        this.setState({
            addConfigParaArr:newAddConfigParaArr
        })
    }

    onChangeAddConfigFun = (value) => {
        let newAddConfigParaArr = []
        for(let a=0;a<keyboardFunArr[value]["paraRuleArr"].length;a++){
            newAddConfigParaArr.push("")
        }
        let storage=window.localStorage;
        storage["addConfigFunIndex"] =value
        storage["addConfigParaArr"] =JSON.stringify(newAddConfigParaArr)
        this.setState({
            addConfigParaArr:newAddConfigParaArr,
            addConfigFunIndex: value
        });
    }

    deleteConfig = (keyName)=>{
        const {userInfo} = this.props
        let hotKeyConfigObj = userInfo["hotKeyConfigObj"]
        let newHotKeyConfigObj = deepCopy(hotKeyConfigObj)
        if(newHotKeyConfigObj[keyName]) {
            delete newHotKeyConfigObj[keyName]
        }
        this.modifyHotKey(newHotKeyConfigObj)
    }

    modifyHotKey = (newHotKeyConfigObj)=>{
        const {userInfo} = this.props

        let formData = new FormData();
        formData.append("accessToken",userInfo["accessToken"]);
        formData.append("newHotKeyConfigObj",JSON.stringify(newHotKeyConfigObj));
        fetch(publicServerURL+"/modify_hot_key", {
            method:'POST',
            body:formData
        }).then((response)=>{
            if (response.ok) {
                return response.json();
            }
        }).then((response)=>{
            if(response['s']=="error"){
                message.error("更改快捷键设置保存失败，请稍后再试")
            }else{
                this.props.changeUserInfo({
                    ...userInfo,
                    hotKeyConfigObj:JSON.parse(response['newHotKeyConfigObj'])
                })

                message.success("更改快捷键设置保存成功")
            }
        }).catch((error)=>{
            console.error(error)
        });
    }
    reDefaultConfig = ()=>{
        let newHotKeyConfigObj = deepCopy(realHotKeyConfigDefaultObj)
        this.modifyHotKey(newHotKeyConfigObj)
    }

    getHotKeyChinese = (hotKeyIndex,key)=>{
        const {userInfo} = this.props;
        let chineseStr = keyboardFunArr[hotKeyIndex]["chinese"]
        let hotKeyConfigObj = userInfo["hotKeyConfigObj"][key]
        let funIndex = hotKeyConfigObj["index"]

        hotKeyConfigObj["paraArr"].map((item,i)=>{
            let paraChinese = ""
            if(keyboardFunArr[funIndex]["paraRuleArr"][i]["type"]=="select"){
                for(let a=0;a<keyboardFunArr[funIndex]["paraRuleArr"][i]["value"].length;a++){
                    if(keyboardFunArr[funIndex]["paraRuleArr"][i]["value"][a]["value"]==item){
                        chineseStr = chineseStr.replace("para",keyboardFunArr[funIndex]["paraRuleArr"][i]["value"][a]["name"])
                    }
                }
            }else{

                chineseStr = chineseStr.replace("para",(hotKeyIndex==5)?sortTypeObj[item]:item)
            }
        })
        return chineseStr
    }

    getConfigContent = ()=>{
        const {userInfo} = this.props;
        let hotKeyConfigObj = userInfo["hotKeyConfigObj"]
        let hotKeyToActionNameArr = []
        let content = []
        for(let key in hotKeyConfigObj){
            let hotKeyIndex = hotKeyConfigObj[key]["index"]
            content.push(<div style={{marginTop:16,width:750,display: "flex",flexDirection: "row"}}>
                <div style={{width:150}}>
                    {keyboardObj[key]}
                </div>
                <div style={{width:500}}>
                    {this.getHotKeyChinese(hotKeyIndex,key)}
                </div>
                <div style={{marginLeft:32,width:150}}>
                    <a style={{color:"#aaa"}} onClick={()=>{
                        if(hotKeyConfigObj[key]["paraArr"].length==0){
                            message.error("该按键下功能没有参数，如需修改功能请删除后重新添加")
                        }else{
                            this.setState({
                                modifyConfigParaArr:hotKeyConfigObj[key]["paraArr"],
                                modifyConfigKey:key.toString(),
                                modifyHotKeyConfigModalVisible:true
                            })}}}>
                        <EditOutlined />
                    </a>
                    <a style={{marginLeft:32,color:"#aaa"}} onClick={()=>{this.deleteConfig(key)}}>
                        <CloseOutlined />
                    </a>
                </div>
            </div>)
        }
        return content.map((item,i)=>{
            return item
        })
    }
    getAddConfigChineseContent = (item)=>{
        let chineseStr = item["chinese"]
        item['paraRuleArr'].map((item,i)=>{
            chineseStr = chineseStr.replace("para","【参数"+(i+1)+"】")
        })
        return chineseStr
    }

    reDefaultConfig = ()=>{
        let newHotKeyConfigObj = deepCopy(realHotKeyConfigDefaultObj)
        this.modifyHotKey(newHotKeyConfigObj)
    }

    onChangeParaSelect = (value,index)=>{
        const {addConfigFunIndex} = this.state
        let newAddConfigParaArr = deepCopy(this.state.addConfigParaArr)
        newAddConfigParaArr[index] = value

        this.setState({
            addConfigParaArr:newAddConfigParaArr
        })
    }


    getParaInput=()=>{
        const {addConfigFunIndex} = this.state;
        return keyboardFunArr[addConfigFunIndex]["paraRuleArr"].map((item,i)=>{
            if(item["type"]=="select"){

                return (
                    <div style={{marginTop:16}}>
                        参数{i+1}:
                        <Select value={this.state.addConfigParaArr[i]} onChange={(value)=>{this.onChangeParaSelect(value,i)}} style={{width:400,marginLeft:16}}>
                            {
                                item["value"].map((item,i)=>{
                                    return <Option  key={i} value={item["value"]}>
                                        {item["name"]}
                                    </Option >
                                })
                            }

                        </Select>
                        <span style={{marginLeft:16}}> {item["explain"]}</span>
                    </div>
                )}else{
                return (
                    <div style={{display: "flex",flexDirection: "row",alignItems: "center",marginTop:16}}>
                        参数{i+1}:
                        <InputNumber controls={false} min={item["rule"]["min"]} max={item["rule"]["max"]} precision={item["rule"]["precision"]} addonAfter={item["rule"]["addonAfter"]} style={{width:400,marginLeft:16}} value={this.state.addConfigParaArr[i]}
                               onChange={(value)=>{this.onChangeParaInput(value,i)}} />
                        <span style={{marginLeft:16}}>{item["explain"]}</span>
                    </div>
                )
            }
        })

    }

    bindKeyboardToFun = ()=>{
        const {addConfigKeyCode,addConfigFunIndex,addConfigParaArr} = this.state;
        const {userInfo} = this.props
        let hotKeyConfigObj = userInfo["hotKeyConfigObj"]
        let newHotKeyConfigObj = deepCopy(hotKeyConfigObj)
        if(addConfigKeyCode==""){
            message.error("请输入按键")
            return
        }
        if(keyboardFunArr[addConfigFunIndex]["paraRuleArr"].length!=addConfigParaArr.length){
            message.error("还有参数没有设置")
            return
        }

        for(let a=0;a<addConfigParaArr.length;a++){
            if(keyboardFunArr[addConfigFunIndex]["paraRuleArr"][a]["type"]=="input"){
                if(!keyboardFunArr[addConfigFunIndex]["paraRuleArr"][a]["value"](addConfigParaArr[a])){
                    let newAddConfigParaArr = deepCopy(addConfigParaArr)
                    newAddConfigParaArr[a]=""
                    this.setState({
                        addConfigParaArr:newAddConfigParaArr
                    })
                    return
                }
            }
        }


        if(newHotKeyConfigObj[addConfigKeyCode]){
            message.error("该按键已绑定其他功能，如需绑定请先删除")
            return
        }
        newHotKeyConfigObj[addConfigKeyCode] = {"index":addConfigFunIndex,"paraArr":addConfigParaArr}
        this.modifyHotKey(newHotKeyConfigObj)
        this.setState({
            addConfigKeyCode:"",
            addConfigFunIndex:0,
            addConfigParaArr:[]
        })
    }

    onChangeAddSelectType = (value)=>{

        let newAddConfigFunIndex = keyboardFunArr.find((item,i)=>{
            if(item["type"]==value||value=="all") {
                return true
            }
            else{
                return false
            }

        })["index"]
        let storage=window.localStorage;
        storage["addSelectType"]=value
        storage["addConfigFunIndex"]=newAddConfigFunIndex
        this.setState({
            addSelectType:value,
            addConfigFunIndex:newAddConfigFunIndex
        })
    }
    getAddConfigContent = ()=>{
        const {addConfigFunIndex,addSelectType} = this.state

        return (
            <div>
                <div style={{marginTop:32,width:1600,display: "flex",flexDirection: "row",alignItems: "center",flexWrap: "wrap"}}>
                    <Input defaultValue={"【按键】"} style={{ width: 100}} value={keyboardObj[this.state.addConfigKeyCode]}
                           onBlur={this.onblurConfigKeyCode} onFocus={this.onfocusConfigKeyCode}/>
                    <Select value={addSelectType} onChange={this.onChangeAddSelectType} style={{width:200,marginLeft:16}}>
                        {
                            addSelectTypeArr.map((item,i)=>{

                                return <Option  key={i} value={item}>
                                    {addSelectTypeObj[item]}
                                </Option >

                            })
                        }

                    </Select>
                    <Select value={this.state.addConfigFunIndex} onChange={this.onChangeAddConfigFun} style={{width:1200,marginLeft:16}}>
                        {
                            keyboardFunArr.map((item,i)=>{
                                if(item["type"]==addSelectType||addSelectType=="all"){
                                    return <Option  key={i} value={item["index"]}>
                                        {this.getAddConfigChineseContent(item)}
                                    </Option >
                                }

                            })
                        }

                    </Select>


                </div>
                <div style={{padding:16}}>
                    {this.getParaInput()}
                </div>
                <div style={{padding:16,marginTop:16,width:1500,fontSize:16}}>
                    {keyboardFunArr[addConfigFunIndex]["explain"]}
                </div>
                <div style={{marginTop:16}}>
                    <Button style={{width:1500}} type={"primary"} onClick={this.bindKeyboardToFun}>
                        绑定该按键为该功能按键
                    </Button>
                </div>
            </div>



        )
    }

    getHotKeyConfigModal=()=>{
        return (
            <Modal width={1600} destroyOnClose={true} title="快捷键设置（云端保存）" visible={this.props.hotKeyConfigModalVisible}
                   onCancel={this.props.cancelHotKeyConfigModal} footer={[
                null
            ]}>
                <div style={{
                    width:1600,
                    paddingLeft: 32,
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "center",paddingBottom:32,
                }}>
                    <div style={{marginTop:0,display: "flex", flexDirection: "row",alignItems:"center"}}>
                        <div style={{marginLeft:48}}>鼠标操作 - 鼠标左键点击币种切换选中币种 ，鼠标双击唤出选中币种的透视图</div>
                    </div>
                    <div style={{marginTop:16,marginLeft:48}}>键盘操作 - <a onClick={this.reDefaultConfig}>恢复键盘快捷键默认设置</a></div>
                    <div style={{
                        marginTop:16,
                        paddingLeft:50,
                        width:1600,
                        display: "flex",
                        flexDirection: "row",paddingBottom:32,flexWrap: "wrap",
                    }}>
                        {this.getConfigContent()}
                    </div>
                    {this.getAddConfigContent()}
                </div>
            </Modal>
        )
    }
    onChangeModifyParaSelect = (value,index,modifyConfigFunIndex)=>{
        let newModifyConfigParaArr = deepCopy(this.state.modifyConfigParaArr)
        if(newModifyConfigParaArr.length<keyboardFunArr[modifyConfigFunIndex]["paraRuleArr"].length){
            newModifyConfigParaArr = []
            for(let a=0;a<keyboardFunArr[modifyConfigFunIndex]["paraRuleArr"].length;a++){
                newModifyConfigParaArr.push("")
            }
        }
        newModifyConfigParaArr[index] = value

        this.setState({
            modifyConfigParaArr:newModifyConfigParaArr
        })
    }

    onChangeModifyParaInput = (value,index,modifyConfigFunIndex)=>{
        if(keyboardFunArr[modifyConfigFunIndex]["paraRuleArr"][index]["type"]=="input"&&!keyboardFunArr[modifyConfigFunIndex]["paraRuleArr"][index]["value"](value)){
            if(value.length==0){
                let newModifyConfigParaArr = deepCopy(this.state.modifyConfigParaArr)
                newModifyConfigParaArr[index]=""
                this.setState({
                    modifyConfigParaArr:newModifyConfigParaArr
                })
            }

            return
        }

        let newModifyConfigParaArr = deepCopy(this.state.modifyConfigParaArr)
        newModifyConfigParaArr[index] = value
        this.state.modifyConfigParaArr = newModifyConfigParaArr

        this.setState({
            modifyConfigParaArr:newModifyConfigParaArr
        })
    }
    getModifyParaInput=(modifyConfigFunIndex)=>{
        let modifyConfigParaArr = this.state.modifyConfigParaArr

        return keyboardFunArr[modifyConfigFunIndex]["paraRuleArr"].map((item,i)=>{
            if(item["type"]=="select"){

                return (
                    <div style={{marginTop:16}}>
                        参数{i+1}:
                        <Select value={modifyConfigParaArr[i]} onChange={(value)=>{this.onChangeModifyParaSelect(value,i,modifyConfigFunIndex)}} style={{width:400,marginLeft:16}}>
                            {
                                item["value"].map((item,i)=>{
                                    return <Option  key={i} value={item["value"]}>
                                        {item["name"]}
                                    </Option >
                                })
                            }

                        </Select>
                        <div style={{marginTop:16}}>{item["explain"]}</div>
                    </div>
                )}else{
                return (
                    <div style={{marginTop:16,display: "flex", flexDirection: "column"}}>
                        <div style={{display: "flex", flexDirection: "row",alignItems:"center"}}>
                            参数{i+1}:
                            <InputNumber controls={false} min={item["rule"]["min"]} max={item["rule"]["max"]} precision={item["rule"]["precision"]} addonAfter={item["rule"]["addonAfter"]}   style={{width:400,marginLeft:16}} value={modifyConfigParaArr[i]}
                                   onChange={(value)=>{this.onChangeModifyParaInput(value,i,modifyConfigFunIndex)}} />
                        </div>
                        <div style={{marginTop:16}}>{item["explain"]}</div>
                    </div>
                )
            }
        })

    }

    modifyHotkeyPara = ()=>{
        const {userInfo} = this.props
        const {modifyConfigParaArr,modifyConfigKey}  = this.state
        let hotKeyConfigObj = userInfo["hotKeyConfigObj"]
        let newHotKeyConfigObj = deepCopy(hotKeyConfigObj)
        let funIndex = newHotKeyConfigObj[modifyConfigKey]["index"]
        console.info(modifyConfigKey)
        console.info(keyboardFunArr[funIndex])
        if(keyboardFunArr[funIndex]["paraRuleArr"].length!=modifyConfigParaArr.length){
            message.error("还有参数没有设置")
            return
        }

        for(let a=0;a<modifyConfigParaArr.length;a++){
            if(keyboardFunArr[funIndex]["paraRuleArr"][a]["type"]=="input"){
                if(!keyboardFunArr[funIndex]["paraRuleArr"][a]["value"](modifyConfigParaArr[a])){
                    let newAddConfigParaArr = deepCopy(modifyConfigParaArr)
                    newAddConfigParaArr[a]=""
                    this.setState({
                        modifyConfigParaArr:newAddConfigParaArr
                    })
                    return
                }
            }
        }

        newHotKeyConfigObj[modifyConfigKey] = {"index":newHotKeyConfigObj[modifyConfigKey]["index"],"paraArr":modifyConfigParaArr}
        this.modifyHotKey(newHotKeyConfigObj)
        this.setState({
            modifyConfigKey:"",
            modifyConfigParaArr:[]
        })
    }
    getModifyHotKeyParaModal=()=>{
        const {userInfo} = this.props;
        const {modifyConfigKey} = this.state;
        if(this.state.modifyHotKeyConfigModalVisible){
            if(modifyConfigKey!=""){
                let hotKeyConfigObj = userInfo["hotKeyConfigObj"]
                let modifyConfigFunIndex = hotKeyConfigObj[modifyConfigKey]["index"]


                return (
                    <Modal width={1056} destroyOnClose={true} title= {"修改"+keyboardObj[modifyConfigKey]+"功能"} visible={this.state.modifyHotKeyConfigModalVisible}
                           onCancel={()=>{this.setState({modifyHotKeyConfigModalVisible:false})}} footer={[
                        null
                    ]}>
                        <div style={{width:1056,display: "flex",
                            flexDirection: "column",
                            justifyContent: "center",
                            alignItems: "center"}}>
                            <div style={{marginTop:32,width:600,display: "flex",flexDirection: "row",alignItems: "center",flexWrap: "wrap"}}>
                                <div style={{marginLeft:16}}>
                                    {this.getModifyParaInput(modifyConfigFunIndex,hotKeyConfigObj[modifyConfigKey]["paraArr"])}
                                </div>

                            </div>
                            <div style={{padding:16,marginTop:16,width:1000}}>
                                <strong>{keyboardFunArr[modifyConfigFunIndex]["explain"]}</strong>
                            </div>

                            <div style={{marginTop:16}}>
                                <Button style={{width:600}} type={"primary"} onClick={()=>{this.modifyHotkeyPara()}}>
                                    确认修改该按键功能参数
                                </Button>
                            </div>
                        </div>
                    </Modal>
                )
            }
        }


    }
    render() {
        if(this.props.hotKeyConfigModalVisible){
            return(
                <div>
                    {this.getHotKeyConfigModal()}
                    {this.getModifyHotKeyParaModal()}
                </div>

            )
        }else{
            return <div></div>
        }


    }
}
const mapStateToProps = (state) => {
    return ({
        titleColor:state.setting['titleColor'],
        depthColor:state.setting['depthColor'],
        midColor:state.setting['midColor'],
        chat:state.chat['chat'],
        systemInfo:state.chat['systemInfo'],
        weibo :state.chat['weibo'],
        userInfo:state.userInfo,
        updateNewChat:action.updateNewChat,
        timestamp:state.setting['timestamp']
    });
};
const mapDispatchToProps  = (dispatch, ownProps) => {
    return bindActionCreators({
        updateIfUpdateChatModalView:action.updateIfUpdateChatModalView,
        updateChat:action.updateChat,
        changeUserInfo:action.changeUserInfo
    }, dispatch);
};
export default connect(mapStateToProps,mapDispatchToProps)(HotKeyModal);
