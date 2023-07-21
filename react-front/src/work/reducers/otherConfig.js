import {MODIFY_OTHER_CONFIG} from '../constants/actionTypes';
import {stateDefaultObj} from "../constants/commonFunction";
//初始化状态
let storage=window.localStorage;
console.info(storage["autoBuyBnbConfigArr"])
let autoBuyBnbConfigArr = storage["autoBuyBnbConfigArr"]&&storage["autoBuyBnbConfigArr"]!="undefined"?JSON.parse(storage["autoBuyBnbConfigArr"]):stateDefaultObj["autoBuyBnbConfigArr"]
let depthConfigArr = storage["depthConfigArr"]&&storage["depthConfigArr"]!="undefined"?JSON.parse(storage["depthConfigArr"]):stateDefaultObj["depthConfigArr"]
let klineCountConfigArr = storage["klineCountConfigArr"]&&storage["klineCountConfigArr"]!="undefined"?JSON.parse(storage["klineCountConfigArr"]):stateDefaultObj["klineCountConfigArr"]
let sortFrequencyTsConfigArr= storage["sortFrequencyTsConfigArr"]&&storage["sortFrequencyTsConfigArr"]!="undefined"?JSON.parse(storage["sortFrequencyTsConfigArr"]):stateDefaultObj["sortFrequencyTsConfigArr"]
let binanceAddressConfigArr = storage["binanceAddressConfigArr"]&&storage["binanceAddressConfigArr"]!="undefined"?JSON.parse(storage["binanceAddressConfigArr"]):stateDefaultObj["binanceAddressConfigArr"]
let selectKlineIntervalConfigArr = storage["selectKlineIntervalConfigArr"]&&storage["selectKlineIntervalConfigArr"]!="undefined"?JSON.parse(storage["selectKlineIntervalConfigArr"]):stateDefaultObj["selectKlineIntervalConfigArr"]
let klineRowCountConfigArr = storage["klineRowCountConfigArr"]&&storage["klineRowCountConfigArr"]!="undefined"?JSON.parse(storage["klineRowCountConfigArr"]):stateDefaultObj["klineRowCountConfigArr"]
let autoStopLossConfigArr = storage["autoStopLossConfigArr"]&&storage["autoStopLossConfigArr"]!="undefined"?JSON.parse(storage["autoStopLossConfigArr"]):stateDefaultObj["autoStopLossConfigArr"]
let autoCancelStopLossConfigArr = storage["autoCancelStopLossConfigArr"]&&storage["autoCancelStopLossConfigArr"]!="undefined"?JSON.parse(storage["autoCancelStopLossConfigArr"]):stateDefaultObj["autoCancelStopLossConfigArr"]
let limitMaxPositionLockConfigArr= storage["limitMaxPositionLockConfigArr"]&&storage["limitMaxPositionLockConfigArr"]!="undefined"?JSON.parse(storage["limitMaxPositionLockConfigArr"]):stateDefaultObj["limitMaxPositionLockConfigArr"]
let limitMaxLossLockConfigArr= storage["limitMaxLossLockConfigArr"]&&storage["limitMaxLossLockConfigArr"]!="undefined"?JSON.parse(storage["limitMaxLossLockConfigArr"]):stateDefaultObj["limitMaxLossLockConfigArr"]
let showProfitWithLeverConfigArr= storage["showProfitWithLeverConfigArr"]&&storage["showProfitWithLeverConfigArr"]!="undefined"?JSON.parse(storage["showProfitWithLeverConfigArr"]):stateDefaultObj["showProfitWithLeverConfigArr"]
let mindModeConfigArr= storage["mindModeConfigArr"]&&storage["mindModeConfigArr"]!="undefined"?JSON.parse(storage["mindModeConfigArr"]):stateDefaultObj["mindModeConfigArr"]
let rocketLimitConfigArr= storage["rocketLimitConfigArr"]&&storage["rocketLimitConfigArr"]!="undefined"?JSON.parse(storage["rocketLimitConfigArr"]):stateDefaultObj["rocketLimitConfigArr"]
let autoCancelOrderConfigArr= storage["autoCancelOrderConfigArr"]&&storage["autoCancelOrderConfigArr"]!="undefined"?JSON.parse(storage["autoCancelOrderConfigArr"]):stateDefaultObj["autoCancelOrderConfigArr"]
let binanceRecommissionConfigArr= storage["binanceRecommissionConfigArr"]&&storage["binanceRecommissionConfigArr"]!="undefined"?JSON.parse(storage["binanceRecommissionConfigArr"]):stateDefaultObj["binanceRecommissionConfigArr"]
let limitTimeMaxPositionConfigArr= storage["limitTimeMaxPositionConfigArr"]&&storage["limitTimeMaxPositionConfigArr"]!="undefined"?JSON.parse(storage["limitTimeMaxPositionConfigArr"]):stateDefaultObj["limitTimeMaxPositionConfigArr"]
let shieldLossSymbolConfigArr= storage["shieldLossSymbolConfigArr"]&&storage["shieldLossSymbolConfigArr"]!="undefined"?JSON.parse(storage["shieldLossSymbolConfigArr"]):stateDefaultObj["shieldLossSymbolConfigArr"]

const initialState ={
    "autoBuyBnbConfigArr":autoBuyBnbConfigArr,
    "depthConfigArr":depthConfigArr,
    "klineCountConfigArr":klineCountConfigArr,
    "sortFrequencyTsConfigArr":sortFrequencyTsConfigArr,
    "binanceAddressConfigArr":binanceAddressConfigArr,
    "selectKlineIntervalConfigArr":selectKlineIntervalConfigArr,
    "klineRowCountConfigArr":klineRowCountConfigArr,
    "autoStopLossConfigArr":autoStopLossConfigArr,
    "autoCancelStopLossConfigArr":autoCancelStopLossConfigArr,
    "limitMaxPositionLockConfigArr":limitMaxPositionLockConfigArr,
    "limitMaxLossLockConfigArr":limitMaxLossLockConfigArr,
    "showProfitWithLeverConfigArr":showProfitWithLeverConfigArr,
    "mindModeConfigArr":mindModeConfigArr,
    "rocketLimitConfigArr":rocketLimitConfigArr,
    "autoCancelOrderConfigArr":autoCancelOrderConfigArr,
    "binanceRecommissionConfigArr":binanceRecommissionConfigArr,
    "limitTimeMaxPositionConfigArr":limitTimeMaxPositionConfigArr,
    "shieldLossSymbolConfigArr":shieldLossSymbolConfigArr
}
export default function otherConfig(state = initialState,action) {
    switch(action.type) {
        case MODIFY_OTHER_CONFIG:
            return  action.otherConfigArr;
        default:
            return state;
    }
}
