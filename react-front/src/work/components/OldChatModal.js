import React from 'react';
import {LinkOutlined,PictureOutlined,SearchOutlined, SmileOutlined} from '@ant-design/icons';
import { Upload,InputNumber,Radio,Slider,Tag,Input,Pagination,Collapse,Avatar,message,Select,Modal,Checkbox,Alert,Switch } from 'antd';
import {coinArr,coinChineseObj} from "../constants/coinType";
import {connect} from "react-redux";
import * as action from "../actions";
import {bindActionCreators} from "redux";
import {subServerURL,serverURL} from "../constants/serverURL";
import {
    deepCopy,
    isVIP, isWeixinVerity
} from '../constants/commonFunction'
import ImgModal from "../components/ImgModal"
import ChatImgUpload from "../components/ChatImgUpload";
import Button from "./Button"
import PFIcon from "./PFIcon";
const { Option } = Select;
const { TextArea } = Input;
const followCoin = [];

const LIGHT_WORDS_COLOR="#8c8c8c"
const MID_WORDS_COLOR="#595959"
const WEIGHT_WORDS_COLOR="#262626"

const LIGHT_BACKGROUND_COLOR="#f9f9f9"
const MID_BACKGROUND_COLOR="#f1f1f1"
const WEIGHT_BACKGROUND_COLOR="#e3e3e3"

const CHAT_TAG_ARR =[
    "综合",
    "VIP",
    "数据",
    "资讯",
    "BUG",
    "建议"
]
for (let i = 0; i < coinArr.length; i++) {
    followCoin.push(<Option key={coinArr[i]}><img style={{marginBottom:2,marginRight:2}} width={15} alt="example" src={"https://yuntuimao.oss-cn-shenzhen.aliyuncs.com/btc/"+coinArr[i]+"Icon.png?x-oss-process=style/slogan"} />{coinChineseObj[coinArr[i]]+"("+coinArr[i]+")"}</Option>);
}

class ChatModal extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            userHistoryModalVisible:false,
            chatWords:'',
            fileList:[],
            topicTag:0,
            userHistoryChat:[]
        };
    }

    showImgModal = (imgUrl) =>{
        this.props.modalShow()
        this.setState({
            imgUrl:imgUrl
        })
    }

    changeFileList = (fileList)=>{

        this.setState({
            fileList:fileList
        })
    }
    getSendImgModalContent = ()=>{
        const {fileList} = this.state;
        return(
            <div style={{padding:16,marginTop:32,display:"flex",flexDirection:"column",justifyContent:"center",alignItems:"center"}}>
                {fileList.length!=0&&<Avatar
                    size={128}
                    src={"https://yuntuimao.oss-cn-shenzhen.aliyuncs.com/"+fileList[0]['url']+"?"+parseInt(Math.random()*(10000000000+1),10)}
                    shape="square"
                />}
                <ChatImgUpload changeFileList={this.changeFileList}/>
            </div>
        )
    }
    changeChatWords = (e)=>{
        if (e.target.value.length>200){
            message.error("超过字数限制")
            return;
        }
        this.setState({
            chatWords:e.target.value
        });
    }
    sendIsVIP = ()=>{
        let timestamp = Date.parse(new Date())/1000;
        if(this.props.userInfo.VIPTime==undefined||this.props.userInfo.VIPTime=="" ){
            return false
        }
        let userVIPTime = parseInt(this.props.userInfo.VIPTime)
        let timeDifferent = userVIPTime-timestamp
        if(timeDifferent<0){
            return "0"
        }else{
            return "1"
        }
    }

    showToUserRule =()=>{
        Modal.info({
            okText:"知道了",
            title: '如何在聊天界面@人',
            content:
                <div style={{width:"100%",maxHeight:document.body.clientHeight*0.7,overflowY: "scroll",textAlign:"left"}}>
                    如果您要@人，以@最比特为例，需填写@最比特@，请用两个@符号把对方账号名称抱住(๑•̀ㅂ•́)و✧，不要有空格或者其他符号，同时每次发送最多仅能@一个人<br/><br/>
                </div>,
        });
    }

    getUserHistoryChat = (userID)=>{
        if(!isVIP(this.props.userInfo.VIPTime)){
            message.info("VIP用户可以查看所有用户的200条历史发言")
            return
        }
        let formData = new FormData();
        formData.append("userID", userID);
        fetch(subServerURL+"/read_user_history_chat_arr", {
            method:'POST',
            body:formData,
            charset:"utf-8"
        }).then((response)=>{
            if (response.ok) {
                return response.json();
            }
        }).then((response)=>{
            if(response['s'] =="s") {
                this.setState({
                    userHistoryChat:response['d'],
                    userHistoryModalVisible:true
                })
                this.reUserHistoryChat()
            }else{
                message.error("3秒内只能请求一次");
            }
        });
    }
    sendMsg = () =>{
        const {userInfo,showLoginModalVisible} = this.props;
        if ( this.props.userInfo.account.length <1) {
            showLoginModalVisible()
            return;
        }
        if(this.state.chatWords.length<1){
            message.error("请输入您的消息");
            return;
        }
        if(this.state.chatWords.length>500){
            message.error("请勿多于500字")
            return;
        }
        let toUserName=""
        let splitChatWordsArr = this.state.chatWords.split("@")
        if(splitChatWordsArr.length ==3){
            toUserName = splitChatWordsArr[1]
        }else if (splitChatWordsArr.length !=1){
            this.showToUserRule()
            return;
        }

        let formData = new FormData();
        formData.append("account", userInfo.account);
        formData.append("password",userInfo.password);
        formData.append("content",this.state.chatWords);
        formData.append("topicTag",this.state.topicTag);
        formData.append("toUserName",toUserName);
        fetch(serverURL+"/insert_chat", {
            method:'POST',
            body:formData,
            charset:"utf-8"
        }).then((response)=>{
            if (response.ok) {
                return response.json();
            }
        }).then((response)=>{
            if(response['s'] =="s") {
                this.setState({
                    chatWords:""
                })
                message.success("发送成功");
                this.loadNewChat()
            }else if(response['s'] =="r"){
                message.error("不允许短时间内发送相同内容");
            }else{
                message.error("发送间隔最低为3秒");
            }
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
    getCompleteChat = ()=>{
        let request = new XMLHttpRequest();

        request.open("get", "http://download.zuibite.pro/chat/0.json");/*设置请求方法与路径*/
        request.setRequestHeader("Cache-Control","no-cache");
        request.setRequestHeader("Access-Control-Allow-Origin","*");
        request.setRequestHeader("Access-Control-Allow-Methods","get,post,put,delete");
        request.send(null);/*不发送数据到服务器*/
        request.onload =()=> {
            if (request.status == 200) {
                let data = JSON.parse(request.responseText);
                this.findConnectMsg(data)
                this.props.updateChat(data,-1)
            }

        }
    }
    loadNewChat=()=>{
        const {chat} = this.props;
        if(chat.length<1){
            this.getCompleteChat()
        }else{
            let formData = new FormData();
            formData.append("nowChatID", chat[chat.length-1][0]);
            fetch(serverURL+"/get_chat", {
                method:'POST',
                body:formData,
                charset:"utf-8"
            }).then((response)=>{
                if (response.ok) {
                    return response.json();
                }
            }).then((response)=>{
                let reponseChat = response['d']
                let newArr = deepCopy(chat)
                let needFindConnectMsg = false
                for(let a=0;a<reponseChat.length;a++){
                    let ifInsert = true
                    for(let b=0;b<chat.length;b++){
                        if(reponseChat[a][0]==chat[b][0]){
                            ifInsert = false
                        }
                    }
                    if(ifInsert){
                        let  timestamp = parseInt(new Date().getTime());
                        this.props.updateNewChat({
                            "id":reponseChat[a][0],
                            "account":reponseChat[a][1],
                            "name":reponseChat[a][9],
                            "avatar":reponseChat[a][8],
                            "time":timestamp,
                            "words":reponseChat[a][2],
                        })
                        needFindConnectMsg = true
                        newArr.push(reponseChat[a])
                    }
                }
                if(needFindConnectMsg){
                    this.reSetChat()
                    this.findConnectMsg(newArr)
                }
                if(newArr.length>500){
                    newArr = newArr.slice(newArr.length-500)
                }
                this.props.updateChat(newArr,response['w'])
            });
        }

    }
    sendPic = () =>{
        const {fileList} = this.state;
        const {userInfo,showLoginModalVisible} = this.props;
        if(fileList.length>0){

            if ( this.props.userInfo.account.length <1) {
                showLoginModalVisible()
                return;
            }
            let formData = new FormData();
            formData.append("account", userInfo.account);
            formData.append("password",userInfo.password);
            formData.append("content","img"+fileList[0]['url']);
            formData.append("topicTag",this.state.topicTag);
            formData.append("toUserName","");
            fetch(serverURL+"/insert_chat", {
                method:'POST',
                body:formData,
                charset:"utf-8"
            }).then((response)=>{
                if (response.ok) {
                    return response.json();
                }
            }).then((response)=>{
                if(response['s'] =="s") {
                    this.props.sendImgModalCancel()
                    this.setState({
                        chatWords:"",
                        fileList:[]
                    })
                    message.success("发送成功");
                    this.loadNewChat()
                }else if(response['s'] =="r"){
                    message.error("不允许短时间内发送相同内容");
                }else{
                    message.error("发送间隔最低为3秒");
                }
            });
        }

    }

    openSendPicModal=()=>{
        if(!isWeixinVerity(this.props.userInfo.articleTime)){
            message.info("为防止广告和方便管理，如果要发送图片，请先点击最上方进入个人中心进行微信认证。")
            return
        }
        this.props.sendImgModalShow()
    }

    changeTopicTag = (topicTag) =>{
        if(topicTag==1&&isVIP(!isVIP(this.props.userInfo.VIPTime))){
            message.error("请点击最上方进入个人中心开通VIP后可浏览")
            return
        }
        this.reSetChat()
        this.setState({
            topicTag:topicTag
        })
    }
    getChatFooter= ()=>{
        const {topicTag} = this.state;
        let thisPath = window.location.hash
        if(thisPath=='#/freeUser')
        {
            return <div style={{width:"100%",textAlign:"center"}}>
                此页面不支持发言
            </div>
        }
        return (
            <div style={{width:"100%",display:"flex",flexDirection:"column",justifyContent: "center",alignItems:"center"}}>
                <div style={{width:"100%",display: "flex",flexDirection:"row"}}>
                    <div onClick={()=>{this.changeTopicTag(0)}} style={{width:"16.667%",textAlign:"center"}}>
                        {topicTag==0?<strong>综合</strong>:<span style={{color:"#939393"}}>综合</span>}
                    </div>
                    <div onClick={()=>{this.changeTopicTag(1)}} style={{width:"16.667%",textAlign:"center"}}>
                        {topicTag==1?<strong>VIP</strong>:<span style={{color:"#939393"}}>VIP</span>}
                    </div>
                    <div onClick={()=>{this.changeTopicTag(2)}} style={{width:"16.667%",textAlign:"center"}}>
                        {topicTag==2?<strong>数据</strong>:<span style={{color:"#939393"}}>数据</span>}
                    </div>
                    <div onClick={()=>{this.changeTopicTag(3)}} style={{width:"16.667%",textAlign:"center"}}>
                        {topicTag==3?<strong>资讯</strong>:<span style={{color:"#939393"}}>资讯</span>}
                    </div>
                    <div onClick={()=>{this.changeTopicTag(4)}} style={{width:"16.667%",textAlign:"center"}}>
                        {topicTag==4?<strong>BUG</strong>:<span style={{color:"#939393"}}>BUG</span>}
                    </div>
                    <div onClick={()=>{this.changeTopicTag(5)}} style={{width:"16.667%",textAlign:"center"}}>
                        {topicTag==5?<strong>建议</strong>:<span style={{color:"#939393"}}>建议</span>}
                    </div>
                </div>
                <div className={"my-divider"}  style={{height:1,width:"100%",marginBottom:8,marginTop:8}}/>
                <div style={{width:"100%",display: "flex",flexDirection:"row"}}>
                    {/*<Icon style={{marginRight:4}} style={{fontSize:30}} type="picture" theme="twoTone" />*/}
                    <PictureOutlined   style={{marginRight:8,fontSize:26,marginTop:4}} onClick={this.openSendPicModal} />
                    <SmileOutlined   style={{marginRight:8,fontSize:26,marginTop:4}} onClick={this.props.showEmojiModal} />
                    {/*<Input id={"chatInput"} autocomplete="off" value ={this.state.chatWords} onChange ={this.changeChatWords} size={"small"} style={{marginRight:8,marginLeft:8}}/>*/}
                    <TextArea
                        value ={this.state.chatWords} onChange ={this.changeChatWords}
                        placeholder="说说你的看法吧"
                        autoSize={{ marginRight:8,marginLeft:8,minRows: 1, maxRows: 10 }}
                    />

                    <div onClick={this.sendMsg} style={{width:80,display: "flex",flexDirection:"row",alignItems:"center", justifyContent: "center",textAlign: "center",border: "1px solid #f0f0f0",borderRadius:5, marginLeft:8}}>发送</div>
                </div>
            </div>
        )
    }

    getChatWidth = (words,isRead) =>{
        let width = document.body.clientWidth;
        let extraWidth = 0
        if(isRead){
            extraWidth = 30
        }
        if(width>350){
            if(words.length>15){
                return 240+extraWidth
            }else{
                return 15+words.length*15+extraWidth
            }
        }else{
            if(words.length>13){
                return 210+extraWidth
            }else{
                return 15+words.length*15+extraWidth
            }
        }
    }

    addZeroT = (value) => {

        if(value.toString().length>=2){
            return value.toString();
        }else{
            return "0"+value.toString();
        }
    }
    formatChatDate = (now)=> {
        var hour=(now.getHours()).toString();
        if(hour.length<2){
            hour = "0"+hour;
        }
        var minute=(now.getMinutes()).toString();
        if(minute.length<2){
            minute = "0"+minute;
        }
        var second=(now.getSeconds()).toString();
        if(second.length<2){
            second = "0"+second;
        }
        return <span style={{fontSize:10,color:"#aaa"}}>{hour+":"+minute+":"+second}</span>
    }
    getSelectWords = (chatPageType,name)=>{
        if(chatPageType == this.props.chatPageType){
            return (
                <div style={{textAlign:"center",alignItems:"center",justifyContent: "center",marginLeft:"7.5%",width: "85%", borderBottomWidth:10,display: "flex",flexDirection:"column", fontWeight: "bolder ", color: MID_WORDS_COLOR}}>
                    {name}
                </div>
            );
        }else{
            return(
                <div style={{textAlign:"center",marginLeft:"7.5%",width: "85%",  fontWeight: "bolder ", color: LIGHT_WORDS_COLOR}}>
                    {name}
                </div>
            );
        }
    }
    sortNumber = (a, b) => {
        return parseFloat(a.time)- parseFloat(b.time) ;
    }

    getWordStyle = (words,readConnect,darkOrLight="light")=>{

        if(words.length==5&&words.indexOf("pic")==0&&parseInt(words.substring(3))){
            let picNumber = parseInt(words.substring(3))
            let picAddress=""
            if (picNumber<52){
                picAddress =picNumber+".png"
            }else if (picNumber>=73){
                picAddress =picNumber+".gif"
            }else{
                picAddress =picNumber+".jpg"
            }
            return(
                <div style={{height:126,display:"block",marginTop: 0, padding:8}}>
                    {picNumber>=73?<img src={"https://yuntuimao.oss-cn-shenzhen.aliyuncs.com/btc/emoji/"+picAddress} />:<img src={"https://yuntuimao.oss-cn-shenzhen.aliyuncs.com/btc/emoji/"+picAddress+"?x-oss-process=style/255"} />}
                </div>
            )
        }else if(words.indexOf("imgbtc_history/")==0){
            let picAddress = words.substring(3)
            return(
                <div onClick={()=>{this.showImgModal("https://yuntuimao.oss-cn-shenzhen.aliyuncs.com/"+picAddress+"")}} style={{maxWidth:document.body.clientWidth*0.7,height:126,marginTop: 0, padding:8,overflowX:"scroll"}}>
                    <div style={{width:1000,height:126}}>
                        {<img src={"https://yuntuimao.oss-cn-shenzhen.aliyuncs.com/"+picAddress+"?x-oss-process=style/255"} />}
                    </div>

                </div>
            )
        }

        else{
            let showWordsStyle = words
            let isRead = false
            if(showWordsStyle.indexOf("@")>=0){
                let showWordsStyleArr = showWordsStyle.split("@")
                if(readConnect==0){
                    showWordsStyle= <span>{showWordsStyleArr[0]}<span style={{color:"#9f9f9f",marginLeft:4,marginRight:4}}><LinkOutlined/>{showWordsStyleArr[1]}</span>{showWordsStyleArr[2]}</span>
                }else{
                    isRead = true
                    showWordsStyle= <span>{showWordsStyleArr[0]}
                        <span style={{color:"#9f9f9f",marginLeft:4,marginRight:4}}><LinkOutlined/>{showWordsStyleArr[1]}</span>
                        {showWordsStyleArr[2]}
                        <a style={{color:"#aaa",fontSize:10,marginLeft:8}}>已读</a>
                    </span>
                }


            }
            return  <div style={{color:darkOrLight=="dark"&&"#f5f5f5",marginLeft:32,width:this.getChatWidth(words,isRead),display:"block",marginTop: 0, borderRadius: 5,background: darkOrLight=="dark"?"#262626":"#fafafa",padding:8}}>
                                           <span>
                {showWordsStyle}

                                           </span></div>
        }

    }

    getSendImgModalFootStyle=()=>{
        return(
            <div style={{width:"100%",display: "flex",flexDirection:"column"}}>
                <div style={{width:"100%",display: "flex",flexDirection:"row"}}>
                    <Button type={"modal"} words={"发送"} onFun={()=>{this.sendPic()}}/>
                </div>
                <div style={{marginTop:8,width:"100%",display: "flex",flexDirection:"row"}}>
                    <Button type={"wModal"} words={"返回 zuibite.com"} onFun={()=>{this.props.sendImgModalCancel()}}/>
                </div>
            </div>)
    }

    getRegisterTime = (registerTime)=>{
        return <i style={{fontSize:10,color:"#aaa"}} color="magenta"> {parseInt((this.props.timestamp/1000 - registerTime )/86400)+"天"}</i>
    }
    getTap = (userTagStr)=>{
        if(userTagStr!=""){
            let tagNameArr = [<i style={{fontSize:10,marginRight:8,color:"#ff7a45"}} color="magenta">合伙人</i>, <i style={{fontSize:10,marginRight:8,color:"#ffc53d"}} color="red">VIP</i>, <i style={{fontSize:10,marginRight:8,color:"#40a9ff"}} color="blue">创建者</i>, <i style={{fontSize:10,marginRight:8,color:"#ff4d4f"}} color="cyan">官方</i>, <i style={{fontSize:10,marginRight:8,color:"#f759ab"}} color="volcano">PDT</i>]
            let userTagArr = userTagStr.split("|")
            return userTagArr.map((item,i)=>{
                return tagNameArr[parseInt(item)]
            })
        }
    }
    httpString=(s) =>{
        var reg = /(http:\/\/|https:\/\/)((\w|=|\?|\.|\/|&|-)+)/g;
        var reg= /(https?|http|ftp|file):\/\/[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]/g;
        s = s.match(reg);
        return(s)
    }

    isStandalone=()=> {
        return navigator.standalone || (window.matchMedia('(display-mode: standalone)').matches);
    }

    withDraw=(withdrawUserID) =>{
        let formData = new FormData();
        formData.append("account", this.props.userInfo.account);
        formData.append("password",this.props.userInfo.password);
        formData.append("withdrawUserID",withdrawUserID);
        fetch(serverURL+"/withdraw_chat", {
            method:'POST',
            body:formData,
            charset:"utf-8"
        }).then((response)=>{
            if (response.ok) {
                return response.json();
            }
        }).then((response)=>{
            if(response['s'] =="s") {
                this.props.sendImgModalCancel()
                this.setState({
                    chatWords:"",
                    fileList:[]
                })
                message.success("撤回成功");
            }
        });
    }
    getWithdrawStyle = (withdrawUserID)=>{
        if(this.props.userInfo.account=="15521391695"){
            return <div  style={{color:"#aaa",marginTop:8,paddingLeft:32,fontSize:12}}>
                <a onClick={()=>{this.withDraw(withdrawUserID)}}>撤回</a>
            </div>
        }
    }

    getTopicTagStyle=(topicTag)=>{
        if(topicTag!=0){
            return(
                <div style={{marginTop:8,paddingLeft:32,fontSize:12}} >
                    <span style={{fontSize:8,color:"#aaa"}}>{CHAT_TAG_ARR[topicTag]}</span>
                </div>
            )
        }
    }
    getLinkStyle =(word)=>{
        let linkArr = this.httpString(word)
        if(linkArr!==null){
            let address = linkArr[0]
            if((navigator.userAgent.indexOf("Html5Plus") > -1)){
                return(
                    <div style={{marginTop:8,paddingLeft:32,fontSize:12}} onClick={()=>{window.plus.runtime.openURL(address )}} >
                        <a>相关链接</a>
                    </div>
                )
            }
            return (
                <div style={{marginTop:8,paddingLeft:32,fontSize:12}}>
                    <a href={address} target="_blank">
                        <a>相关链接</a>
                    </a>
                </div>

            )
        }
    }

    reSetChat = () =>{
        let timer = setInterval(()=>{
                let boxElement=document.getElementById("chatView");
                if(boxElement != null){
                    boxElement.scrollTop=1000000;

                    clearInterval(timer);
                }
            }
            ,100);
    }
    reUserHistoryChat = () =>{
        let timer = setInterval(()=>{
                let boxElement=document.getElementById("userHistoryView");
                if(boxElement != null){
                    boxElement.scrollTop=0;

                    clearInterval(timer);
                }
            }
            ,100);
    }
    getChat = () =>{
        const {chat} = this.props;
        let height = document.body.clientHeight*0.8;
        let width = document.body.clientWidth>1200?520:"100%";
        let showChat =chat.slice(chat.length-200)
        return(
            <div  style={{ height:height,width: width}}>
                <Modal
                    visible={this.props.sendImgModalVisible}
                    onCancel={this.props.sendImgModalCancel}
                    style={{width:"100%"}}
                    closable = {false}
                    destroyOnClose={true}
                    footer={this.getSendImgModalFootStyle()}
                >
                    <div style={{display:!this.props.sendImgModalVisible&&"none",width:"100%",maxHeight:document.body.clientHeight*0.8,overflowY: "auto"}}>
                        {this.getSendImgModalContent()}
                    </div>
                    <div style={{marginLeft:"10%",width:"80%",marginBottom:16}}>
                        请不要发送
                        <strong style={{marginLeft:4,color:"red"}}>涉及政治，色情的截图<br/></strong>
                    </div>
                </Modal>
                <div style={{backgroundColor:this.props.titleColor,display: "flex",flexDirection:"row",alignItems:"center", justifyContent: "center"}}>
                    <div style={{textAlign:"center", height: 36,display: "flex",flexDirection:"row",alignItems:"center", justifyContent: "left"}}>
                        <div style={{marginTop:-6,width:36}}>
                            <Avatar
                                src={"https://yuntuimao.oss-cn-shenzhen.aliyuncs.com/whiteLogo.png"}
                                alt="Han Solo"
                                size={18}
                            />
                        </div>
                        <div style={{marginLeft:8,marginTop:10,height: 36,display: "flex",flexDirection:"column",alignItems:"left", justifyContent: "left", textAlign: "left"}}>
                            <div >
                                <strong  style={{fontSize:16,marginLeft:8,color:"#f0f0f0"}}>
                                    最 比 特
                                </strong>
                                <span  style={{color:"#f0f0f0",marginLeft:16,fontSize:14}} ><SearchOutlined tyle={{color:"#f0f0f0",marginRight:8}}/>
                                    <span style={{marginLeft:8}}>www.zuibite.com</span>
                                </span>
                            </div>
                        </div>
                    </div>

                </div>
                {/*<div style={{backgroundColor:MID_BACKGROUND_COLOR,fontSize:10,width:width,color:"#aaa",textAlign:"center"}}>VIP消息会广播，广告带单会封号！<a onClick={this.report}>举报</a></div>*/}
                <div className={"chatView"} id={"chatView"} abindex="0" hidefocus="true" onTouchStart ={()=>{this.props.updateIfUpdateChatModalView(false)}} style={{height:height-60,overflowY: "scroll", width: "100%",padding:24}}>

                    {

                        showChat.map((item,i)=>{
                            if(item[11]==1){
                                if(this.state.topicTag==0||this.state.topicTag==item[7])
                                    return(
                                        <div  key={i} style={{marginTop: 32,marginBottom: 16, width: "100%",textAlign:"left"}}>
                                            <div style={{marginBottom:4,width: "100%", display: "flex", flexDirection:"row"}}>
                                            <span onClick={()=>{this.getUserHistoryChat(item[1])}}><Avatar
                                                src={"https://yuntuimao.oss-cn-shenzhen.aliyuncs.com/" + (item[8].length>2?"btc_history/avatar/"+(item[8])+"?x-oss-process=style/200":"btc/avatar/"+(item[8]) + ".png"+"?x-oss-process=style/200")}
                                                alt="Han Solo"
                                                size={40}
                                                style={{marginTop: -6}}
                                            /></span>
                                                <div style={{marginTop: -8,display: "flex", flexDirection:"column",textAlign:"left"}}>
                                                    <div style={{marginLeft: 16,display: "flex",flexDirection:"row",justifyContent: "left",alignItems:"center"}}>
                                                        <div><span style={{marginTop: -8, fontSize: 14}}>{item[9]}
                                                    </span></div>
                                                        <div style={{marginLeft:12}}>{this.getTap(item[5])} </div>
                                                        <div style={{marginLeft:0}}>{this.getRegisterTime(parseInt(item[4]))} </div>
                                                    </div>
                                                    <div style={{marginLeft: 16, fontSize: 12,marginTop: 0,display: "flex",flexDirection:"row",justifyContent: "left",alignItems:"center"}}>
                                                        {this.formatChatDate(new Date(parseInt(item[3])*1000))}
                                                    </div>
                                                </div>
                                            </div>
                                            {
                                                this.getWithdrawStyle(item[1])

                                            }
                                            {
                                                item[7]==1&&!isVIP(this.props.userInfo.VIPTime)?this.getWordStyle("这是一条VIP才可以看到的消息",item[12],"dark") : item[7]==1&&isVIP(this.props.userInfo.VIPTime)?this.getWordStyle(item[2],item[12],"dark"):this.getWordStyle(item[2],item[12])

                                            }
                                            {
                                                this.getLinkStyle(item[2])

                                            }
                                            {
                                                this.getTopicTagStyle(item[7])

                                            }
                                        </div>
                                    );
                            }

                        })
                    }

                </div>
            </div>
        );

    }

    userHistoryModalCancel =()=>{
        this.setState({
            userHistoryModalVisible:false
        })
    }

    getUserHistoryModalContent=()=>{
        const {userHistoryChat} = this.state;
        let height = document.body.clientHeight*0.8;
        return(
            <div className={"userHistoryView"} id={"userHistoryView"} abindex="0" hidefocus="true" style={{height:height-60,overflowY: "scroll", width: "100%",padding:24}}>

                {
                    userHistoryChat.map((item,i)=>{
                        return(
                            <div  key={i} style={{marginTop: 32,marginBottom: 16, width: "100%",textAlign:"left"}}>
                                <div style={{marginBottom:4,width: "100%", display: "flex", flexDirection:"row"}}>
                                        <span ><Avatar
                                            src={"https://yuntuimao.oss-cn-shenzhen.aliyuncs.com/" + (item[6].length>2?"btc_history/avatar/"+(item[6])+"?x-oss-process=style/200":"btc/avatar/"+(item[6]) + ".png"+"?x-oss-process=style/200")}
                                            alt="Han Solo"
                                            size={40}
                                            style={{marginTop: -6}}
                                        /></span>
                                    <div style={{marginTop: -8,display: "flex", flexDirection:"column",textAlign:"left"}}>
                                        <div style={{marginLeft: 16,display: "flex",flexDirection:"row",justifyContent: "left",alignItems:"center"}}>
                                            <div><strong style={{marginTop: -8, fontSize: 14}}>{item[7]}
                                            </strong></div>
                                            <div style={{marginLeft:12}}>{this.getTap(item[3])} </div>
                                            <div style={{marginLeft:0}}>{this.getRegisterTime(parseInt(item[2]))} </div>
                                        </div>
                                        <div style={{marginLeft: 16, fontSize: 12,marginTop: 0,display: "flex",flexDirection:"row",justifyContent: "left",alignItems:"center"}}>
                                            {this.formatChatDate(new Date(parseInt(item[1])*1000))}
                                        </div>
                                    </div>
                                </div>
                                {
                                    this.getWordStyle(item[0],item[10])

                                }
                                {
                                    this.getLinkStyle(item[0])

                                }
                                {
                                    this.getTopicTagStyle(item[5])

                                }
                            </div>
                        );
                    })
                }

            </div>
        )
    }

    getUserHistoryFooter=()=>{
        return (
            <div style={{width:"100%",display:"flex",flexDirection:"column",justifyContent: "center",alignItems:"center"}}>
                <Button type={"wModal"} words={"返回最比特聊天"} onFun={this.userHistoryModalCancel}/>
            </div>
        )
    }
    render() {
        if(this.props.chatModalVisible){
            return(
                <div>
                    <Modal
                        visible={this.props.chatModalVisible}
                        onCancel={this.chatModalCancel}
                        style={{width:"50%",background: "rgba(0,0,0,.7)"}}
                        closable = {false}
                        footer={[
                            this.getChatFooter()
                        ]}
                    >
                        <ImgModal imgUrl={this.state.imgUrl} imgModalVisible={this.props.imgModalVisible} imgModalCancel={this.props.modalCancel}/>
                        {this.getChat()}
                    </Modal>
                    <Modal
                        visible={this.state.userHistoryModalVisible}
                        onCancel={this.userHistoryModalCancel}
                        closable = {true}
                        zIndex={9999}
                        footer={[
                            this.getUserHistoryFooter()
                        ]}
                    >

                        {this.getUserHistoryModalContent()}
                    </Modal>
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
    }, dispatch);
};
export default connect(mapStateToProps,mapDispatchToProps)(ChatModal);
