import { ADD_USER_INFO,MODIFY_USER_INFO,CLEAR_USER_INFO } from '../constants/actionTypes';
//初始化状态
const initialState ={
    account:"",
    name:"",
    registerTime:"",
    binanceApiArr:[],
    hotKeyConfigObj:{},
    stateConfigObj:{},
    serverInfoObj:{},
    showSymbolObj:{}
};

export default function userInfo(state = initialState,action) {
    switch(action.type) {
        case ADD_USER_INFO:
            return  action.userInfo;
        case MODIFY_USER_INFO:
            return  action.userInfo;
        case CLEAR_USER_INFO:
            return initialState;
        default:
            return state;
    }
}
