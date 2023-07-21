import React  from 'react';
import { Timeline,Button,InputNumber,Radio,Slider,Tag,Input,Pagination,Collapse,Avatar,message,Select,Modal,Checkbox,Alert,Switch } from 'antd';
import {coinArr,coinChineseObj} from "../constants/coinType";
import {realHotKeyConfigDefaultObj} from "../constants/commonFunction";
import {connect} from "react-redux";
import * as action from "../actions";
import { PhoneOutlined, KeyOutlined,SmileOutlined,HeartOutlined  } from '@ant-design/icons';
import {bindActionCreators} from "redux";
import {serverURL} from "../constants/serverURL";
import {login} from "../actions";
import {getCookie} from "../constants/cookie"
const { Option } = Select;
const followCoin = [];
for (let i = 0; i < coinArr.length; i++) {
    followCoin.push(<Option key={coinArr[i]}><img style={{marginBottom:2,marginRight:2}} width={15} alt="example" src={"https://yuntuimao.oss-cn-shenzhen.aliyuncs.com/btc/"+coinArr[i]+"Icon.png?x-oss-process=style/slogan"} />{coinChineseObj[coinArr[i]]+"("+coinArr[i]+")"}</Option>);
}

class LoginModal extends React.Component {
    constructor(props) {
        super(props);
        let loginInfoKey =[]
        let loginInfo={}
        try{
            loginInfo= JSON.parse(getCookie("loginInfo"));
            loginInfoKey = Object.keys(loginInfo);
        } catch(err) {
            console.error("cookie err");
        }
        let account = ""
        let password= ""
        let status="register"
        if ( loginInfoKey.length >0) {

            account=loginInfo.account
            password=loginInfo.password
            status="login"
        }
        console.info(account)
        this.state = {
            type: props.type ,
            visible: props.visible ,
            status:status,
            name:"",
            account:account,
            password:password,
            playCoin:"BTC",
            playTime:'20年',
            code:"",
            lastSendCodeTime :0,
            playType:"现货",
            personalType:"投资者",
            articleTitle:<span>注册 <a onClick={()=>{this.switchStatus("login")}} style = {{marginLeft:8,marginBottom:6,fontSize:12,width:"100%"}}> 已有帐号，点击登录</a></span>,
            followCoin:["BTC","ETH"]
        };
    }

   playTimeChange=(value)=> {
        this.setState({
            playTime:value
        });
    }
    playTypeChange=(value)=> {
        this.setState({
            playType:value
        });
    }
    personalTypeChange  = (value) =>{
        this.setState({
            personalType:value
        });
    }
    componentDidMount = ()=>{
        this.setState({complete:false});
    }
    switchStatus = (status) =>{
        console.error(status)
        if (status === "register"){
            this.setState({
                status:"register",
                articleTitle:<span>注册 <a onClick={()=>{this.switchStatus("login")}} style = {{marginLeft:8,marginBottom:6,fontSize:12,width:"100%"}}> 已有帐号，点击登录</a></span>
            });
        }else if (status === "modifyPassword"){
            this.setState({
                status:"modifyPassword",
                articleTitle:<span>修改密码 <a onClick={()=>{this.switchStatus("login")}} style = {{marginLeft:8,marginBottom:6,fontSize:10,}}>返回登录</a></span>
            });
        } else{
            this.setState({
                status:"login",
                articleTitle:<span>登录 <a onClick={()=>{this.switchStatus("modifyPassword")}} style = {{marginLeft:8,marginBottom:6,fontSize:10,}}>忘记密码</a></span>
            });
        }
    }

    onChangeName = (e) =>{
        this.setState({
            name:e.target.value
        });
    }
    onChangeCode = (e) =>{
        this.setState({
            code:e.target.value
        });
    }
    onChangeAccount = (e) =>{
        this.setState({
            account:e.target.value
        });
    }
    onChangePassword = (e) =>{
        this.setState({
            password:e.target.value
        });
    }

    findConnectMsg =(data)=>{
        let storage=window.localStorage;
        let readChatArr = []
        if(storage["chat"]){
            readChatArr = storage["chat"].split("-")
        }
        for(let a=0;a<data.length;a++){
            if(this.props.userInfo.name!=""&&data[a][10]!=""&&data[a][10]==this.props.userInfo.name){
                let showMsg = true
                for(let b =0;b<readChatArr.length;b++){
                    if(parseInt(readChatArr[b])==data[a][0]){
                        showMsg = false
                    }
                }
                if(showMsg){
                    // message.info(data[a][9]+"@了你，说"+data[a][2])
                    Modal.info({
                        okText:"知道了",
                        title: data[a][9]+"@了你",
                        content:
                            <div style={{width:"100%",maxHeight:document.body.clientHeight*0.8,overflowY: "scroll"}}>
                                {data[a][2]}
                            </div>,
                        onOk:()=>{}
                    });
                    readChatArr.push(data[a][0].toString())
                    if(readChatArr.length>50){
                        readChatArr.shift()
                    }
                    let readChatStr = readChatArr.join("-")

                    storage["chat"] = readChatStr
                }

            }
        }
    }

    submitLogin= ()=>{
        const {status,account,password,name,playCoin,playTime,playType,isMobile} = this.state;
        let result =this.props.login({account:account,password:password}).then((result)=>{
            if(result){
                this.props.loginModalCancel();
                this.props.doingAfterLogin();
                this.findConnectMsg(this.props.chat)
            }
        });
    }
    submitModifyPassword = ()=>{
        const {account,password,code} = this.state;
        this.props.modifyPassword({code:code,account:account,password:password}).then((result)=>{
            if (result){
                this.props.loginModalCancel();
            }

        });
    }
    submitRegister= ()=>{
        const {status,account,password,name,playCoin,playTime,playType,code,isMobile,personalType,followCoin} = this.state;


        this.props.register({account:account,password:password,name:name}).then((result)=>{
            if (result){
                this.props.loginModalCancel();
            }

        });

    }
    getBorder= (coin)=>{
        let select =false
        this.state.followCoin.map((item,i)=>{
            if(item == coin){
                select = true
            }
        });
        return select;
    }
    changeFollowCoinSelect = (coin)=>{
        let select =false
        let tempFollowCoin = this.state.followCoin
        let deleteIndex = 0
        tempFollowCoin.map((item,i)=>{
            if(item == coin){
                select = true;
                deleteIndex = i;
            }
        });
        if (select){
            if(tempFollowCoin.length==1){
                message.error("必须选择最少一个币种");
                return;
            }

            tempFollowCoin.splice(deleteIndex, 1);
        }else{
            if(tempFollowCoin.length<5){
                tempFollowCoin.push(coin);
            }else{
                message.error("最多选择五个币种");
                return;
            }

        }
        this.setState({
            followCoin:tempFollowCoin
        });
    }
    getFollowUI = ()=>{
        let thisCoinArr = coinArr;
        let lengthArr = []
        for(let i =0;i<coinArr.length%3;i++) {
            thisCoinArr.push("NO");
        }
        for(let i =0;i<parseInt(coinArr.length/3);i++) {
            lengthArr.push("");
        }
        return lengthArr.map((item,i)=>{
            return(
                <div key={i} style={{width:"100%",marginTop:8,marginBottom:8,display: "flex",flexDirection:"row"}}>
                    <div style = {{width:"33.3%",textAlign:"center"}}>
                        <div onClick={()=>{this.changeFollowCoinSelect(coinArr[i*3])}} style = {{padding:1,border:this.getBorder(coinArr[i*3])?"3px solid #a8071a":"1px solid #f5f5f5",width:"90%",marginLeft:"5%",borderRadius:5}}>
                            <img style={{marginBottom:2,marginRight:2}} width={15} alt="example" src={"https://yuntuimao.oss-cn-shenzhen.aliyuncs.com/btc/"+coinArr[i*3]+"Icon.png?x-oss-process=style/slogan"} />
                            {coinChineseObj[coinArr[i*3]]}
                        </div>
                    </div>
                    <div style = {{display:thisCoinArr[i*3+1]=="NO"&&"none",width:"33.3%",textAlign:"center"}}>
                        <div  onClick={()=>{this.changeFollowCoinSelect(coinArr[i*3+1])}}  style = {{padding:1,border:this.getBorder(coinArr[i*3+1])?"3px solid #a8071a":"1px solid #f5f5f5",width:"90%",marginLeft:"5%",borderRadius:5}}>
                            <img style={{marginBottom:2,marginRight:2}} width={15} alt="example" src={"https://yuntuimao.oss-cn-shenzhen.aliyuncs.com/btc/"+coinArr[i*3+1]+"Icon.png?x-oss-process=style/slogan"} />
                            {coinChineseObj[coinArr[i*3+1]]}
                        </div>
                    </div>
                    <div style = {{display:thisCoinArr[i*3+2]=="NO"&&"none",width:"33.3%",textAlign:"center"}}>
                        <div  onClick={()=>{this.changeFollowCoinSelect(coinArr[i*3+2])}}  style = {{padding:1,border:this.getBorder(coinArr[i*3+2])?"3px solid #a8071a":"1px solid #f5f5f5",width:"90%",marginLeft:"5%",borderRadius:5}}>
                            <img style={{marginBottom:2,marginRight:2}} width={15} alt="example" src={"https://yuntuimao.oss-cn-shenzhen.aliyuncs.com/btc/"+coinArr[i*3+2]+"Icon.png?x-oss-process=style/slogan"} />
                            {coinChineseObj[coinArr[i*3+2]]}
                        </div>
                    </div>
                </div>);
        });
    }
    changePlayCoinSelect = (coin)=>{

        this.setState({
            playCoin:coin
        });
    }
    getPlayCoinBorder= (coin)=>{
        if(this.state.playCoin==coin) {
            return true;
        }
        return false;
    }

    isChinese = (s)=>
    {
        var patrn= /[\u4E00-\u9FA5]|[\uFE30-\uFFA0]/gi;
        if (!patrn.exec(s))
        {
            return false;
        }else{
            return true;
        }
    }
    checkChinese = ()=>{
        if(!this.isChinese(this.state.name)){
            message.error("仅支持中文昵称");
        }
    }
    getPlayCoinUI = ()=>{
        let thisCoinArr = [];
        Object.assign(thisCoinArr, coinArr)
        let lengthArr = []
        for(let i =0;i<coinArr.length%3;i++) {
            thisCoinArr.push("NO");
        }

        for(let i =0;i<parseInt(coinArr.length/3);i++) {
            lengthArr.push("");
        }
        return lengthArr.map((item,i)=>{
            return(
                <div key={i} style={{width:"100%",marginTop:8,marginBottom:8,display: "flex",flexDirection:"row"}}>
                    <div style = {{width:"33.3%",textAlign:"center"}}>
                        <div onClick={()=>{this.changePlayCoinSelect(coinArr[i*3])}} style = {{padding:1,border:this.getPlayCoinBorder(coinArr[i*3])?"3px solid #a8071a":"1px solid #f5f5f5",width:"90%",marginLeft:"5%",borderRadius:5}}>
                            <img style={{marginBottom:2,marginRight:2}} width={15} alt="example" src={"https://yuntuimao.oss-cn-shenzhen.aliyuncs.com/btc/"+coinArr[i*3]+"Icon.png?x-oss-process=style/slogan"} />
                            {coinChineseObj[coinArr[i*3]]}
                        </div>
                    </div>
                    <div style = {{display:thisCoinArr[i*3+1]=="NO"&&"none",width:"33.3%",textAlign:"center"}}>
                        <div  onClick={()=>{this.changePlayCoinSelect(coinArr[i*3+1])}}  style = {{padding:1,border:this.getPlayCoinBorder(coinArr[i*3+1])?"3px solid #a8071a":"1px solid #f5f5f5",width:"90%",marginLeft:"5%",borderRadius:5}}>
                            <img style={{marginBottom:2,marginRight:2}} width={15} alt="example" src={"https://yuntuimao.oss-cn-shenzhen.aliyuncs.com/btc/"+coinArr[i*3+1]+"Icon.png?x-oss-process=style/slogan"} />
                            {coinChineseObj[coinArr[i*3+1]]}
                        </div>
                    </div>
                    <div style = {{display:thisCoinArr[i*3+2]=="NO"&&"none",width:"33.3%",textAlign:"center"}}>
                        <div  onClick={()=>{this.changePlayCoinSelect(coinArr[i*3+2])}}  style = {{padding:1,border:this.getPlayCoinBorder(coinArr[i*3+2])?"3px solid #a8071a":"1px solid #f5f5f5",width:"90%",marginLeft:"5%",borderRadius:5}}>
                            <img style={{marginBottom:2,marginRight:2}} width={15} alt="example" src={"https://yuntuimao.oss-cn-shenzhen.aliyuncs.com/btc/"+coinArr[i*3+2]+"Icon.png?x-oss-process=style/slogan"} />
                            {coinChineseObj[coinArr[i*3+2]]}
                        </div>
                    </div>
                </div>);
        });
    }
    getVerityCode = ()=>{
        let formData = new FormData();
        formData.append("phone", this.state.account);
        let response = fetch(serverURL+"/send_verity_code", {
            method:'POST',
            body:formData
        }).then((response)=>{
            if (response.ok) {
                return response.json();
            }
        }).then((response)=>{
            if (response['status'] =="success") {
                message.success('发送成功');
            } else if (response['status'] =="phoneLengthError") {
                message.success('手机号码格式错误');
            }  else if (response['status'] =="sendTimeLimit") {
                message.success('发送间隔过短');
            }  else {
                message.error('发送太频繁');
            }
            return false;
        }).catch((error)=>{
            message.error('网络错误');
        });
        this.setState({
            lastSendCodeTime:59
        })
        let timer = setInterval(()=>{
            let thisLastSendCodeTime = this.state.lastSendCodeTime-1
            this.setState({
                lastSendCodeTime:thisLastSendCodeTime
            })
            if(thisLastSendCodeTime==0){
                clearInterval(timer);
            }
        },1000);
    }
    loginAndRegister = ()=>{

        const {status,account,password,name,playCoin,playTime,playType,isMobile,personalType} = this.state;
        if(!this.props.visible){

            return;
        }
        if(this.props.webAPP){
            return <Install type={"page"}/>
        }
        let loginInfo={}
        let loginInfoKey=[]
        try{
            loginInfo= JSON.parse(getCookie("loginInfo"));
            loginInfoKey = Object.keys(loginInfo);
        } catch(err) {
            console.error("cookie err");
        }
        if(status === "login") {
            return (
                <div style={{width:1000,padding:16,display:"flex",flexDirection:"column",justifyContent:"center",alignItems:"center"}}>

                    <div style = {{display:"flex",flexDirection:"column",justifyContent:"center",alignItems:"center"}}>
                        <img alt="logo" width={isMobile?"120":"120"}  src={"https://yuntuimao.oss-cn-shenzhen.aliyuncs.com/logo.png"} />
                    </div>
                    <div  style = {{display:"flex",flexDirection:"column",justifyContent:"center",alignItems:"center",textAlign:"center"}}>
                        <p style = {{marginTop:24,color:"#aaa",fontSize:16}}>{"最交易-专业的合约交易工具"}</p>



                    </div>

                    <div id={"area"} style={{ width:"40%",position: 'relative',marginTop:24,display:"flex",flexDirection:"column",justifyContent:"center",alignItems:"center"}}>
                        {loginInfoKey.length>0?<Input style = {{width:"100%",color:"#aaa"}} value={this.state.account} onChange={this.onChangeAccount} prefix={<HeartOutlined style={{ color: 'rgba(0,0,0,.25)' }}/>} />
                        :<Input style = {{width:"100%",color:"#aaa"}} placeholder="请输入您的账号"   onChange={this.onChangeAccount} prefix={<HeartOutlined style={{ color: 'rgba(0,0,0,.25)' }}/>} />}

                        {loginInfoKey.length>0?<Input style = {{width:"100%",marginTop:16,color:"#aaa"}} value={this.state.password} onChange={this.onChangePassword} prefix={<KeyOutlined style={{ color: 'rgba(0,0,0,.25)' }}/>}  />:
                            <Input style = {{width:"100%",marginTop:16,color:"#aaa"}} placeholder="请输入您的密码" onChange={this.onChangePassword} prefix={<KeyOutlined style={{ color: 'rgba(0,0,0,.25)' }}/>}  />}
                        <Button style={{width:"100%",marginTop:32}} type={"primary"}  onClick={()=>{this.submitLogin()}}>登录</Button>
                        <Button style={{width:"100%",marginTop:16}}  onClick={()=>{this.switchStatus("register")}}>还没帐号，马上注册</Button>
                    </div>
                    <div id={"area"} style={{ width:"100%",position: 'relative',marginTop:32,display:"flex",flexDirection:"column",justifyContent:"center",alignItems:"center"}}>
                        <Timeline>
                            <Timeline.Item>创新性的透视全合约币种 - 全市场低于100毫秒延迟排序</Timeline.Item>
                            <Timeline.Item>极速按键开关仓，可设置按键，只做maker，只挂买一卖一，分散挂单等</Timeline.Item>
                            <Timeline.Item>自动止损止盈挂单，一键按用户设定规则止损止盈挂单</Timeline.Item>
                            <Timeline.Item>多账号同时交易，光速切换</Timeline.Item>
                            <Timeline.Item>...</Timeline.Item>
                        </Timeline>
                    </div>
                </div>
            );
        } else if(status === "modifyPassword") {
            let height = document.body.clientHeight*0.6-60;
            return (
                <div style={{padding:16,height:height,overflowY: "scroll"}}>
                    <div id={"area"} style={{ position: 'relative',width:"100%",marginTop:8,display:"flex",flexDirection:"column",justifyContent:"center",alignItems:"center"}}>
                        <Input style = {{width:"100%",marginTop:16,color:"#aaa"}} placeholder="请输入您的账号"   onChange={this.onChangeAccount} prefix={<HeartOutlined style={{ color: 'rgba(0,0,0,.25)' }}/>} />
                        <p  style = {{fontSize:10,marginTop:8}}>*非大陆用户，不想泄露手机号的用户，可以选择付费方案，并且联系微信zuibite或者Email 到zuibite@hotmail.com，我们会帮助您实现隐秘账号 </p>
                        <div style = {{width:"100%",marginTop:4,display:"flex",flexDirection:"row"}}>
                            <Input style = {{width:"50%",color:"#aaa"}} placeholder="四位验证码"   onChange={this.onChangeCode}/>
                            {
                                this.state.lastSendCodeTime!=0?<span disabled style = {{marginLeft:16}}>{this.state.lastSendCodeTime+"秒后获取"}</span>:
                                    <Button width={100} marginLeft={16} type={"wModal"} words={"获取验证码"} onFun={()=>{this.getVerityCode()}}/>
                                    // <span onClick={()=>{this.getVerityCode();}}style = {{marginLeft:16}}>{"获取验证码"}</span>
                            }
                        </div>
                        <Input style = {{width:"100%",marginTop:16,color:"#aaa"}} placeholder="请输入4~20位的新密码" onChange={this.onChangePassword} prefix={<KeyOutlined style={{ color: 'rgba(0,0,0,.25)' }}/>}  />
                        <Button marginTop={32} type={"modal"} words={"修改密码"} onFun={()=>{this.submitModifyPassword()}}/>
                        {/*<span onClick={this.submitModifyPassword} type="primary" style = {{width:"100%",marginTop:32}}>修改密码</span>*/}
                    </div>
                </div>
            );
        }else {
            let height = document.body.clientHeight*0.8;
            return (
                <div style={{width:1000,padding:16,display:"flex",flexDirection:"column",justifyContent:"center",alignItems:"center"}}>

                    <div style = {{display:"flex",flexDirection:"column",justifyContent:"center",alignItems:"center"}}>
                        <img alt="logo" width={isMobile?"120":"120"}  src={"https://yuntuimao.oss-cn-shenzhen.aliyuncs.com/logo.png"} />
                    </div>
                    <div  style = {{display:"flex",flexDirection:"column",justifyContent:"center",alignItems:"center",textAlign:"center"}}>
                        <p style = {{marginTop:24,color:"#aaa",fontSize:16}}>{"最交易-专业的合约交易工具"}</p>



                    </div>
                    <div id={"area"} style={{ width:"40%",position: 'relative',marginTop:24,display:"flex",flexDirection:"column",justifyContent:"center",alignItems:"center"}}>
                        <Input style = {{color:"#aaa"}} placeholder="请输入1~20位昵称"   onChange={this.onChangeName} prefix={<Avatar src={"https://joeschmoe.io/api/v1/"+this.state.name} /> } />
                        <Input style = {{marginTop:16,color:"#aaa"}} placeholder="请输入4~20位账号"   onChange={this.onChangeAccount} prefix={<HeartOutlined style={{ color: 'rgba(0,0,0,.25)' }}/> } />
                        <Input style = {{marginTop:16,color:"#aaa"}} placeholder="请输入4~20位的密码" onChange={this.onChangePassword} prefix={<KeyOutlined style={{ color: 'rgba(0,0,0,.25)' }}/> }  />
                        <Button style={{width:"100%",marginTop:32}} type={"primary"}  onClick={()=>{this.submitRegister()}}>注册</Button>
                        <Button style={{width:"100%",marginTop:16}}  onClick={()=>{this.switchStatus("login")}}>已有账号，登录</Button>


                    </div>
                    <div id={"area"} style={{ width:"100%",position: 'relative',marginTop:32,display:"flex",flexDirection:"column",justifyContent:"center",alignItems:"center"}}>
                        <Timeline>
                            <Timeline.Item>创新性的透视全合约币种 - 全市场低于100毫秒延迟排序</Timeline.Item>
                            <Timeline.Item>极速按键开关仓，可设置按键，只做maker，只挂买一卖一，分散挂单等</Timeline.Item>
                            <Timeline.Item>自动止损止盈挂单，一键按用户设定规则止损止盈挂单</Timeline.Item>
                            <Timeline.Item>多账号同时交易，光速切换</Timeline.Item>
                            <Timeline.Item>...</Timeline.Item>
                        </Timeline>
                    </div>
                </div>
            );
        }
    }
    render() {
        if(this.props.visible){
            if (this.state.type=='modal'){
                return (
                    <Modal
                        title={this.state.articleTitle}
                        visible={this.props.visible}
                        onCancel={this.props.loginModalCancel}
                        footer={[null]}
                    >
                        {this.loginAndRegister()}
                    </Modal>
                );
            }else{
                return(
                    <div style={{
                        display: "flex",
                        flexDirection: "column",
                        justifyContent: "center",
                        alignItems: "center",
                        minHeight: document.body.clientHeight,
                        backgroundColor: "#f0f0f0",
                        width: "100%",
                        height: "100%",
                        padding:32
                    }}>
                        {this.loginAndRegister()}
                    </div>
                );
            }
        }else{
            return(<div></div>)
        }


    }
}
const mapStateToProps = (state) => {
    return ({
        chat:state.chat['chat'],
        webAPP:state.setting['webAPP'],
        userInfo:state.userInfo,
        msg:state.msg
    });
};
const mapDispatchToProps  = (dispatch, ownProps) => {
    return bindActionCreators({
        login: action.login,
        register: action.register,
        modifyPassword:action.modifyPassword
    }, dispatch);
};
export default connect(mapStateToProps,mapDispatchToProps)(LoginModal);
