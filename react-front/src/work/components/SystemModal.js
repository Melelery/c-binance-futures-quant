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


class SystemModal extends React.Component {
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



    render() {
        if(this.props.systemModalVisible){
            let showChatArr = deepCopy(this.props.systemArr)
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
                    <div id={"chatView"} style={{width:"100%",height:600,overflowY: "auto"}}>
                        {
                            showChatArr.map((item,i)=>{
                                return this.getChatRow(item["n"],item["t"],item["c"],item["a"],i)
                            })
                        }
                    </div>


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
        systemModalVisible:state.chat.systemModalVisible,
        systemArr:state.chat.systemArr,
        userInfo:state.userInfo,

    });
};
const mapDispatchToProps  = (dispatch, ownProps) => {
    return bindActionCreators({
        modifyChatArr:action.modifyChatArr
    }, dispatch);
};
export default connect(mapStateToProps,mapDispatchToProps)(SystemModal);
