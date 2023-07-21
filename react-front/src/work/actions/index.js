import {publicServerURL, serverURL} from "../constants/serverURL";
import {message} from "antd";
import {
    MODIFY_CHAT_ARR,
    CHANGE_TITLE_COLOR,
    UPDATE_MARKET_MODAL_VISIBLE,
    UPDATE_IF_UPDATE_SYSTEM_MODAL_VIEW,
    CLEAR_SYSTEM_UNREAD_NUMBER,
    UPDATE_SYSTEM_UNREAD_NUMBER,
    CHANGE_BIG_DATA_COIN,
    CHANGE_FUNDS_COIN,
    UPDATE_DEPTH_DATA,
    MODIFY_OTHER_CONFIG,
    PUSH_NEW_WEIBO,
    UPDATE_IF_UPDATE_CHAT_MODAL_VIEW,
    ADD_USER_INFO,
    CLEAR_USER_INFO,
    SWITCH_APP,
    LONGS_AND_SHORTS_COIN,
    UPDATE_SEND_MSG,
    SWITCH_SPEED_TYPE,
    UPDATE_MSG,
    UPDATE_MSG_A,
    UPDATE_MSG_B,
    UPDATE_MSG_C,
    UPDATE_MSG_D,
    UPDATE_MSG_E,
    UPDATE_MSG_F,
    UPDATE_MSG_H,
    UPDATE_MSG_I,
    UPDATE_MSG_J,
    UPDATE_MSG_K,
    UPDATE_MSG_L,
    UPDATE_MSG_M,
    UPDATE_MSG_N,
    UPDATE_MSG_O,
    UPDATE_MSG_P,
    UPDATE_MSG_Q,
    UPDATE_MSG_R,
    UPDATE_CHAT,
    UPDATE_MSG_ZI,
    UPDATE_MSG_FEAR,
    SWITCH_SUB_PAGE,
    SWITCH_MODE,
    UPDATE_LOW_AND_HIGN,
    PUSH_NEW_SYSTEM_INFO,
    SWITCH_COLOR_PROGRAM,
    UPDATE_ARTICLE_DATA,
    SHOW_ARTICLE_UPDATE,
    CLEAR_UNREAD_NUMBER,
    UPDATE_UNREAD_NUMBER,
    UPDATE_TEADE_DATA_ARR,
    SWITCH_OKEX_COIN,
    UPDATE_NEW_CHAT,
    SWITCH_CHAT_POP_SWITCH,
    SWITCH_TABLE_EXCHANGE,
    UPDATE_TIMESTAMP
} from '../constants/actionTypes';
import {setCookie} from "../constants/cookie";
import {realHotKeyConfigDefaultObj} from "../constants/hotKey.js";

export function register(info) {
    return async(dispatch,getState) => {
        var myReg=/^[a-zA-Z0-9_-]+@([a-zA-Z0-9]+\.)+(com|cn|net|org)$/;

        let formData = new FormData();
        formData.append("account", info.account);
        formData.append("password",info.password);
        formData.append("name", info.name);
        formData.append("newHotKeyConfigObj",JSON.stringify(realHotKeyConfigDefaultObj));
        let response = await fetch(publicServerURL+"/register", {
            method:'POST',
            body:formData
        }).then((response)=>{
            if (response.ok) {
                return response.json();
            }
        }).then((response)=>{
            if (response['s'] =="ok") {
                message.success('注册成功');
                dispatch(login(info));
                return true;
            } else if(response['s'] =="nameLengthError") {
                message.error('昵称应该为4到20位');

            } else if(response['s'] =="repeatRegister") {
                message.error('该账号已经存在');
            }   else if(response['s'] =="passwordLengthError") {
                message.error('密码应该为4到20位');
            }  else if(response['s'] =="accountLengthError") {
                message.error('账号应该为4到20位');
            }
            return false;
        }).catch((error)=>{
            message.error('网络错误');
            console.error(error);
            return false;
        });
        return response;

        //这里的type一定要全局唯一,因为状态变一次每个Reducer都会根据类型比对一遍

    };
}

export function login(info) {
    return async(dispatch,getState) => {
        let formData = new FormData();
        formData.append("account", info.account);
        formData.append("password",info.password);

        return await fetch(publicServerURL+"/login", {
            method:'POST',
            body:formData,
            charset:"utf-8"
        }).then((response)=>{
            if (response.ok) {
                return response.json();
            }
        }).then((response)=>{
            if(response['s'] =="ok") {
                message.success('登陆成功');
                setCookie("loginInfo",JSON.stringify({"account":response['account'],"password":response['password']}));
                let item = {
                    account:response['account'],
                    password:response['password'],
                    name:response['name'],
                    binanceApiArr:response['binanceApiArr'],
                    hotKeyConfigObj:response['hotKeyConfigObj'],
                    stateConfigObj:response['stateConfigObj'],
                    serverInfoObj:response['serverInfoObj'],
                    accessToken:response['accessToken'],
                    showSymbolObj:response['showSymbolObj']
                };
                dispatch(changeUserInfo(item));
                return true;
            } else if(response['status'] =="noRegister") {
                message.error('该账号尚未注册');
                return false;

            } else if(response['status'] =="passwordError") {
                message.error('密码错误');
                return false;
            }


        }).catch((error)=>{
            message.error('登陆失败');
            console.error(error);
            return false;
        });
        //这里的type一定要全局唯一,因为状态变一次每个Reducer都会根据类型比对一遍

    };
}

export function modifyPassword(info) {
    return async(dispatch,getState) => {
        let formData = new FormData();
        formData.append("account", info.account);
        formData.append("password",info.password);
        formData.append("code",info.code);
        let response = await fetch(serverURL+"/modify_password", {
            method:'POST',
            body:formData
        }).then((response)=>{
            if (response.ok) {
                return response.json();
            }
        }).then((response)=>{
            if (response['status'] =="success") {
                message.success('修改成功，正在自动登录');
                dispatch(login(info));
                return true;
            } else if(response['status'] =="nameLengthError") {
                message.error('昵称长度有误');

            } else if(response['status'] =="repeatRegister") {
                message.error('该账号已经存在');
            } else if(response['status'] =="passwordLengthError") {
                message.error('密码含有非法字符');
            }else if(response['status'] =="nameUnlawful") {
                message.error('昵称含有非法字符');
            }  else if(response['status'] =="passwordLengthError") {
                message.error('密码应该为4到20位');
            }  else if(response['status'] =="accountLengthError") {
                message.error('账号应该为11位手机号');
            }  else if(response['status'] =="accountNoExit") {
                message.error('该手机尚未注册');
            }  else if(response['status'] =="followCoinLengthError") {
                message.error('验证码长度有误');
            }   else if(response['status'] =="codeError") {
                message.error('验证码输入错误');
            }   else {
                message.error('网络错误');
            }
            return false;
        }).catch((error)=>{
            message.error('网络错误');
            console.error(error);
            return false;
        });
        return response;

        //这里的type一定要全局唯一,因为状态变一次每个Reducer都会根据类型比对一遍

    };
}
export function changeUserInfo(newUserInfo){
    return {
        type: ADD_USER_INFO,
        userInfo:newUserInfo
    };
    }
export function clearUserInfo(){
    return {
        type: CLEAR_USER_INFO
    };
}

export function updateMSGA(data){
    return {
        type: UPDATE_MSG_A,
        data:data,
    };
}
export function updateMSGB(data){
    return {
        type: UPDATE_MSG_B,
        data:data,
    };
}
export function modifyOtherConfig(data){
    return {
        type: MODIFY_OTHER_CONFIG,
        otherConfigArr:data,
    };
}

export function modifyChatArr(data){
    return {
        type: MODIFY_CHAT_ARR,
        chat:data,
    };
}

export function updateMSGC(data){
    return {
        type: UPDATE_MSG_C,
        data:data,
    };
}

export function updateMSGD(data){
    return {
        type: UPDATE_MSG_D,
        data:data,
    };
}

export function updateMSGE(data){
    return {
        type: UPDATE_MSG_E,
        data:data,
    };
}
export function updateMSGF(data){
    return {
        type: UPDATE_MSG_F,
        data:data,
    };
}
export function updateMSG(data){
    return {
        type: UPDATE_MSG,
        data:data,
    };
}

export function updateMSGH(data){
    return {
        type: UPDATE_MSG_H,
        data:data,
    };
}


export function updateMSGI(data){
    return {
        type: UPDATE_MSG_I,
        data:data,
    };
}


export function updateMSGJ(data){
    return {
        type: UPDATE_MSG_J,
        data:data,
    };
}


export function updateMSGK(data){
    return {
        type: UPDATE_MSG_K,
        data:data,
    };
}


export function updateMSGL(data){
    return {
        type: UPDATE_MSG_L,
        data:data,
    };
}


export function updateMSGM(data){
    return {
        type: UPDATE_MSG_M,
        data:data,
    };
}

export function updateMSGN(data){
    return {
        type: UPDATE_MSG_N,
        data:data,
    };
}

export function updateMSGO(data){
    return {
        type: UPDATE_MSG_O,
        data:data,
    };
}

export function updateMSGP(data){
    return {
        type: UPDATE_MSG_P,
        data:data,
    };
}

export function updateMSGR(data){
    return {
        type: UPDATE_MSG_R,
        data:data,
    };
}

export function updateMSGQ(data){
    return {
        type: UPDATE_MSG_Q,
        data:data,
    };
}

export function updateMSGZI(data){
    return {
        type: UPDATE_MSG_ZI,
        data:data,
    };
}
export function updateMSGFEAR(data){
    return {
        type: UPDATE_MSG_FEAR,
        data:data,
    };
}
export function updateArticleData(data){
    return {
        type: UPDATE_ARTICLE_DATA,
        data:data,
    };
}


export function updateDepthData(data){
    return {
        type: UPDATE_DEPTH_DATA,
        data:data,
    };
}
export function updateLowAndHign(data){
    return {
        type: UPDATE_LOW_AND_HIGN,
        data:data,
    };
}
export function pushNewSystemInfo(systemInfo){
    return {
        type: PUSH_NEW_SYSTEM_INFO,
        systemInfo:systemInfo,
    };
}

export function pushNewWeibo(weibo){
    return {
        type: PUSH_NEW_WEIBO,
        weibo:weibo,
    };
}

export function switchColorProgram(depthColor,midColor,rateColorA,rateColorB,articleColor,longAndShortColor,bigTradeColor,depthBackgroundColor,depthBackgroundColorB,colorType,longAndShortColorB){
    return {
        type: SWITCH_COLOR_PROGRAM,
        depthColor:depthColor,
        midColor:midColor,
        rateColorA:rateColorA,
        rateColorB:rateColorB,
        articleColor:articleColor,
        longAndShortColor:longAndShortColor,
        bigTradeColor:bigTradeColor,
        depthBackgroundColor:depthBackgroundColor,
        depthBackgroundColorB:depthBackgroundColorB,
        colorType:colorType,
        longAndShortColorB:longAndShortColorB
    };
}

export function switchSpeedType(type){
    return {
        type: SWITCH_SPEED_TYPE,
        speedType:type
    };
}

export function updateChat(chat,withdrawUserID){
    return {
        type: UPDATE_CHAT,
        chat:chat,
    };
}

export function updateNewChat(newChat){
    return {
        type: UPDATE_NEW_CHAT,
        newChat:newChat
    };
}

export function updateMarketModalVisible(marketModalVisible){
    return {
        type: UPDATE_MARKET_MODAL_VISIBLE,
        marketModalVisible:marketModalVisible
    };
}


export function changeChatPopSwitch(chatPopSwitch){
    return {
        type: SWITCH_CHAT_POP_SWITCH,
        chatPopSwitch:chatPopSwitch
    };
}

export function clearUnreadNumber(){
    return {
        type: CLEAR_UNREAD_NUMBER
    };
}
export function updateUnreadNumber(unReadNumber){
    return {
        type: UPDATE_UNREAD_NUMBER,
        unReadNumber:unReadNumber
    };
}

export function clearSystemUnreadNumber(){
    return {
        type: CLEAR_SYSTEM_UNREAD_NUMBER
    };
}
export function updateSystemUnreadNumber(unReadSystemNumber){
    return {
        type: UPDATE_SYSTEM_UNREAD_NUMBER,
        unReadSystemNumber:unReadSystemNumber
    };
}


export function updateTradeDataArr(tradeDataArr){
    return {
        type: UPDATE_TEADE_DATA_ARR,
        tradeDataArr:tradeDataArr
    };
}

export function showArticleUpdate(result){
    return {
        type: SHOW_ARTICLE_UPDATE,
        result:result
    };
}
export function switchOkexCoin(OKEXCoin){
    return {
        type: SWITCH_OKEX_COIN,
        OKEXCoin:OKEXCoin
    };
}
export function switchAPP(webAPP){
    return {
        type: SWITCH_APP,
        webAPP:webAPP
    };
}
export function  changeLongsAndShortsCoin  (longsAndShortsCoin){
    return {
        type: LONGS_AND_SHORTS_COIN,
        longsAndShortsCoin:longsAndShortsCoin
    };
}
export function updateSendMSG(sendMSG){
    return {
        type: UPDATE_SEND_MSG,
        sendMSG:sendMSG
    };
}
export function switchSubPage(subPage){
    console.error(subPage)
    return {
        type: SWITCH_SUB_PAGE,
        subPage:subPage
    };
}
export function switchTableExchange(tableExchange){
    return {
        type: SWITCH_TABLE_EXCHANGE,
        tableExchange:tableExchange
    };
}
export function updateIfUpdateChatModalView(ifUpdateChatModalView){
    return {
        type: UPDATE_IF_UPDATE_CHAT_MODAL_VIEW,
        ifUpdateChatModalView:ifUpdateChatModalView
    };
}
export function updateIfUpdateSystemModalView(ifUpdateSystemModalView){
    return {
        type: UPDATE_IF_UPDATE_SYSTEM_MODAL_VIEW,
        ifUpdateSystemModalView:ifUpdateSystemModalView
    };
}

export function changeFundsCoin(fundsCoin){
    return {
        type: CHANGE_FUNDS_COIN,
        fundsCoin:fundsCoin
    };
}
export function changeBigDataCoin(bigDataCoin){
    return {
        type: CHANGE_BIG_DATA_COIN,
        bigDataCoin:bigDataCoin
    };
}
export function updateTimestamp(timestamp){
    return {
        type: UPDATE_TIMESTAMP,
        timestamp:timestamp
    };
}
export function changeTitleColor(titleColor){
    return {
        type: CHANGE_TITLE_COLOR,
        titleColor:titleColor
    };
}