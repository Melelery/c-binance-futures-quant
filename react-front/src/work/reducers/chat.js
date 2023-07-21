import {
    MODIFY_CHAT_ARR
} from '../constants/actionTypes';
import {stateDefaultObj} from "../constants/commonFunction";
//初始化状态
let storage=window.localStorage;
let chatArr = storage["chatArr"]&&storage["chatArr"]!="undefined"?JSON.parse(storage["chatArr"]):[]
let systemArr = storage["systemArr"]&&storage["systemArr"]!="undefined"?JSON.parse(storage["systemArr"]):[]
console.info(chatArr)
const initialState ={
    chatArr:chatArr,
    systemArr:systemArr,
    chatUnreadCount:0,
    systemUnreadCount:0,
    chatModalVisible:false,
    systemModalVisible:false
};

export default function chat(state = initialState,action) {

    switch(action.type) {
        case MODIFY_CHAT_ARR:
            return  action.chat;
        default:
            return state;
    }
}
