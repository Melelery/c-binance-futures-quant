import React from 'react';
import {SendOutlined,PictureOutlined,SearchOutlined, SmileOutlined} from '@ant-design/icons';
import { Divider,InputNumber,Radio,Slider,Tag,Input,Pagination,Collapse,Avatar,message,Select,Modal,Checkbox,Alert,Switch } from 'antd';
import {coinArr,coinChineseObj} from "../constants/coinType";
import {connect} from "react-redux";
import * as action from "../actions";
import {bindActionCreators} from "redux";
import LoginModal from "./LoginModal";
import {publicServerURL} from "../constants/serverURL";
import {deepCopy} from "../constants/commonFunction";
const { TextArea } = Input;

class ChatModal extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            sendContent:""
        };
    }
    componentDidMount=() =>{
        this.reSetChat()
        this.props.modifyChatArr({
            ...this.props.chat,
            "unreadCount":0
        })
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
    getChatRow = (name,time,content,chatType,index)=>{
        if(chatType=="c"){
            return (
                <div key={index} style={{width:"100%"}}>
                    <div style={{fontSize:16,display: "flex", flexDirection: "row",alignItems:"center"}}>
                        <div> <Avatar size={36} src={"https://joeschmoe.io/api/v1/"+name} /></div>
                        <div style={{marginLeft:16}}>{name}</div>
                        <div style={{fontSize:12,marginLeft:16}}>{time}</div>
                    </div>
                    <div style={{paddingLeft:32,marginTop:12}}>
                        {content}
                    </div>
                    <Divider/>
                </div>
            )
        }else if (chatType=="r"){
            return (
                <div key={index} style={{width:"100%"}}>
                    <div style={{fontSize:14,display: "flex", flexDirection: "row",alignItems:"center"}}>
                        <div style={{marginLeft:16}}>{time}</div>
                        <div style={{marginLeft:16}}>{name}</div>
                        <div style={{marginLeft:16}}><strong>{content}</strong></div>
                    </div>
                    <Divider/>
                </div>
            )
        }

    }

    onChangeSendContent = (e)=>{
        this.setState({
            sendContent:e.target.value
        })
    }

    sendMsg = ()=>{
        const {userInfo} = this.props;
        if(this.state.sendContent.length<3){
            message.error("至少输入三个字符")
            return
        }
        let formData = new FormData();
        formData.append("accessToken",userInfo["accessToken"]);
        formData.append("name",userInfo["name"]);
        formData.append("content",this.state.sendContent);
        formData.append("chatType","c");
        fetch(publicServerURL+"/new_chat", {
            method:'POST',
            body:formData
        }).then((response)=>{
            if (response.ok) {
                return response.json();
            }
        }).then((response)=>{
            if(response['s']=="ok") {
                message.success("发送成功")
                this.setState({
                    sendContent:""
                })
            }else{
                message.success("3秒内不允许发送两次消息")
            }
        }).catch((error)=>{

            console.error(error)
        });
    }

    getChatOrLogin = ()=>{
        const {userInfo} = this.props;
        if(userInfo["account"].length<=0){
            return <a onClick={()=>{window.open(address, '_blank')}}>请点击此处登录或者注册后进行聊天</a>
        }else{
            return <div style={{width:"100%"}}>

                <div style={{width:"100%",fontSize:16,display: "flex", flexDirection: "row",alignItems:"center"}}>
                    <div style={{width:"90%"}}>

                        <TextArea value={this.state.sendContent} maxLength={200} onBlur={this.props.onBlurFun}  onFocus={this.props.onFocusFun} onChange={(e)=>{this.onChangeSendContent(e)}} rows={2} />
                    </div>
                    <div style={{width:"10%"}}>
                        <a  onClick={this.sendMsg}>
                            <SendOutlined  style={{color:"#00558c",fontSize:26,marginLeft:16}}/>

                        </a>
                    </div>
                </div>
                {this.props.chatModalInput&&<strong>*聊天窗输入信息的时候所有快捷键都会失效</strong>}
            </div>
        }
    }
    render() {
        if(this.props.chatModalVisible){
            let showChatArr = deepCopy(this.props.chatArr)
            return(
                <div style={{
                    padding:16,
                    border:"1px solid #b8c7cc",
                    borderRadius:10,
                    zIndex:99999,
                    width:600,
                    height:600,
                    backgroundColor:"white",
                    position:"fixed",
                    top:document.body.clientHeight-600-57,
                    left:document.body.clientWidth-620}}>
                    <div id={"chatView"} style={{width:"100%",height:500,overflowY: "auto"}}>
                        {
                            showChatArr.map((item,i)=>{
                                return this.getChatRow(item["n"],item["t"],item["c"],item["a"],i)
                            })
                        }
                    </div>

                    {this.getChatOrLogin()}

                </div>

            )
        }else{
            return <div></div>
        }


    }
}
const mapStateToProps = (state) => {
    return ({
        chat:state.chat,
        chatModalVisible:state.chat.chatModalVisible,
        chatArr:state.chat.chatArr,
        userInfo:state.userInfo,

    });
};
const mapDispatchToProps  = (dispatch, ownProps) => {
    return bindActionCreators({
        modifyChatArr:action.modifyChatArr
    }, dispatch);
};
export default connect(mapStateToProps,mapDispatchToProps)(ChatModal);
