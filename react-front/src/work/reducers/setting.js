import {CHANGE_TITLE_COLOR,UPDATE_MARKET_MODAL_VISIBLE,UPDATE_IF_UPDATE_SYSTEM_MODAL_VIEW,CHANGE_BIG_DATA_COIN,UPDATE_TIMESTAMP,CHANGE_FUNDS_COIN,FORCE_SEND_MSG, SWITCH_COLOR_PROGRAM,SWITCH_CHAT_POP_SWITCH,SWITCH_SPEED_TYPE,SWITCH_OKEX_COIN,SWITCH_APP,LONGS_AND_SHORTS_COIN,SWITCH_SUB_PAGE,SWITCH_TABLE_EXCHANGE,UPDATE_IF_UPDATE_CHAT_MODAL_VIEW } from '../constants/actionTypes';
import {longAndShortColorB,depthColor,midColor,rateColorA,rateColorB,articleColor,longAndShortColor,bigTradeColor,depthBackgroundColor,depthBackgroundColorB} from '../constants/color';
import {getLocalStorage} from "../constants/commonFunction";
//初始化状态
const initialState ={
    //#5c0011 or #3f6600
    isSmallScreen:document.body.clientWidth>350?false:true,
    webAPP:false,
    OKEXCoin:"btc",
    bigDataCoin:"BTC",
    fundsCoin:"BTC",
    longsAndShortsCoin: "BTC",
    ifUpdateChatModalView:true,
    ifUpdateSystemModalView:true,
    colorType:'Stock',//Coin Stock
    speedType:600,
    chatPopSwitch:"1",
    tableExchange:"HUOBI",// BINANCE BITFINEX HUOBI OKCOIN
    subPage:"longsAndShorts",//index longsAndShorts   dragon  liquidation backTrack funds large cost OKEXStatistics bigData pendingOrder
    // depthColor:["#135200","#820014"],
    themeColor:"#b63345",
    depthColor:depthColor,
    midColor:midColor,
    rateColorA:rateColorA,
    rateColorB:rateColorB,
    articleColor:articleColor,
    longAndShortColor:longAndShortColor,
    bigTradeColor:bigTradeColor,
    depthBackgroundColor:depthBackgroundColor,
    depthBackgroundColorB:depthBackgroundColorB,
    longAndShortColorB:longAndShortColorB,
    timestamp:(new Date()).getTime(),
    marketModalVisible:false,
    clientRealWidth:document.body.clientWidth,
    titleColor:getLocalStorage("titleColor")||'rgba(100,30,30, 1)'

};

export default function setting(state = initialState,action) {
    switch(action.type) {
        case UPDATE_MARKET_MODAL_VISIBLE:
            return Object.assign({}, state, {
                marketModalVisible:action.marketModalVisible
            })
        case UPDATE_TIMESTAMP:
            return Object.assign({}, state, {
                timestamp:action.timestamp
            })
        case CHANGE_FUNDS_COIN:
            return Object.assign({}, state, {
                fundsCoin:action.fundsCoin
            })
        case CHANGE_BIG_DATA_COIN:
            return Object.assign({}, state, {
                bigDataCoin:action.bigDataCoin
            })
        case SWITCH_COLOR_PROGRAM:
            return Object.assign({}, state, {
                depthColor:action.depthColor,
                midColor:action.midColor,
                rateColorA:action.rateColorA,
                rateColorB:action.rateColorB,
                articleColor:action.articleColor,
                longAndShortColor:action.longAndShortColor,
                bigTradeColor:action.bigTradeColor,
                depthBackgroundColor:action.depthBackgroundColor,
                depthBackgroundColorB:action.depthBackgroundColorB,
                colorType:action.colorType,
                longAndShortColorB:action.longAndShortColorB
            })
        case SWITCH_SPEED_TYPE:
            return Object.assign({}, state, {
                speedType:action.speedType
            })
        case SWITCH_CHAT_POP_SWITCH:
            return Object.assign({}, state, {
                chatPopSwitch:action.chatPopSwitch
            })
        case SWITCH_OKEX_COIN:
            return Object.assign({}, state, {
                OKEXCoin:action.OKEXCoin
            })
        case SWITCH_APP:
            return Object.assign({}, state, {
                webAPP:action.webAPP
            })
        case LONGS_AND_SHORTS_COIN:
            return Object.assign({}, state, {
                longsAndShortsCoin:action.longsAndShortsCoin
            })
        case SWITCH_SUB_PAGE:
            return Object.assign({}, state, {
                subPage:action.subPage
            })
        case SWITCH_TABLE_EXCHANGE:
            return Object.assign({}, state, {
                tableExchange:action.tableExchange
            })
        case UPDATE_IF_UPDATE_CHAT_MODAL_VIEW:
            return Object.assign({}, state, {
                ifUpdateChatModalView:action.ifUpdateChatModalView
            })
        case UPDATE_IF_UPDATE_SYSTEM_MODAL_VIEW:
            return Object.assign({}, state, {
                ifUpdateSystemModalView:action.ifUpdateSystemModalView
            })
        case CHANGE_TITLE_COLOR:
            return Object.assign({}, state, {
                titleColor:action.titleColor
            })
        default:
            return state;
    }
}
