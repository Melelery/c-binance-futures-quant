import {UPDATE_MSG,UPDATE_LOW_AND_HIGN,UPDATE_MSG_A,UPDATE_MSG_B,UPDATE_MSG_C,UPDATE_MSG_D,UPDATE_MSG_E,UPDATE_MSG_F,UPDATE_ARTICLE_DATA,SHOW_ARTICLE_UPDATE,UPDATE_SEND_MSG,UPDATE_MSG_H,
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
    UPDATE_MSG_ZI,
    UPDATE_MSG_FEAR,
    UPDATE_MSG_TM,
    UPDATE_DEPTH_DATA} from '../constants/actionTypes';
//初始化状态
const initialState ={
    historyLongsAndShortsCoin:"",
    priceStr:"",
    depthStr:"",
    depthBStr:"",
    cDepthStr:"",
    tradeStr:"",
    liquidationStr:"",
    historicalPriceStr:"",
    todayPriceStr:"",
    huobiContractPriceStr:"",
    huobiWeekContractPriceStr:"",
    bitmexContractPriceStr:"",
    bitfinexSpotPriceStr:"",
    binanceFuturePriceStr:"",
    okexQuarterPriceStr:"",
    okexWeekPriceStr:"",
    okexForeverPriceStr:"",
    highAndLowStr:"",
    okcoinPriceStr:"",
    longsAndShortsStr:"",
    liquidationStrB:"",
    huobiLiquidationStr:"",
    huobiSLiquidationStr:"",
    bitmexLiquidationStr:"",
    bitmexLiquidationStrB:"",
    historyLikeStr:"",
    historyLikeTStr:"",
    lowAndHignData:[],
    recentContactName:[],
    recentContactAccount:[],
    articleData:[],
    depthData:[],

    nowFundsCoinIndex:"0",
    showArticleUpdate:false,
    largeTradeStr:"",
    contactLargeTradeStr:"",
    tradeStatisticsStr:"",
    cTradeStatisticsStr:"",
    bigDataStr:"",
    bigDataHistoryStr:"",
    bigDataIndex:0,
    bigDataCoin:"",
    usdtStr:"",
    huobiCostStr:"",
    binanceCostStr:"",
    okexCostStr:"",
    bitfinexCostStr:"",
    longsAndShortsHistoryStr:"",
    usdtHistoryStr:"",
    zuibiteIndexStr:"",
    bitmexLeaderBoardPercent:"",
    huobiZuibiteIndexHistoryStr:"",
    binanceZuibiteIndexHistoryStr:"",
    fearHistoryStr:"",
    cTradeStr:"",
    binanceFutureRate:"",
    bitmexFutureRate:"",
    okexFutureRate:"",
    binanceLiquidationStr:"",
    indexLongsAndShortsStr :""
};

export default function msg(state = initialState,action) {
    switch(action.type) {
        case UPDATE_MSG:
            return Object.assign({}, state, {
                data:action.data
            })

        case UPDATE_MSG_A:
            return Object.assign({}, state, {
                priceStr:action.data['priceStr'],
                depthStr:action.data['depthStr'],
                depthBStr:action.data['depthBStr'],
                tradeStr:action.data['tradeStr'],
                todayPriceStr:action.data['todayPriceStr'],
            })
        case UPDATE_MSG_B:
            return Object.assign({}, state, {
                priceStr:action.data['priceStr'],
                cDepthStr:action.data['depthStr'],
                cTradeStr:action.data['tradeStr'],
                todayPriceStr:action.data['todayPriceStr'],
            })
        case UPDATE_MSG_D:
            return Object.assign({}, state, {
                todayPriceStr:action.data['todayPriceStr']
            })
        case UPDATE_MSG_E:
            return Object.assign({}, state, {
                historicalPriceStr:action.data['historicalPriceStr'],
                highAndLowStr:action.data['highAndLowStr'],
            })
        case UPDATE_MSG_F:
            return Object.assign({}, state, {
                usdtStr:action.data['usdtStr']
            })
        case UPDATE_MSG_H:
            return Object.assign({}, state, {
                todayPriceStr:action.data['todayPriceStr'],
                huobiContractPriceStr:action.data['huobiContractPriceStr'],
                huobiWeekContractPriceStr:action.data['HCW'],
                bitmexContractPriceStr:action.data['BPS'],
                bitfinexSpotPriceStr:action.data['BIPS'],
                binanceFuturePriceStr:action.data['BFP'],
                longsAndShortsStr:action.data['longsAndShortsStr'],
                indexLongsAndShortsStr:action.data['lass'],
                okexQuarterPriceStr:action.data['okexQuarterPriceStr'],
                okexWeekPriceStr:action.data['OWP'],
                okexForeverPriceStr:action.data['OFP'],
                okcoinPriceStr:action.data['okcoinPriceStr'],
                usdtStr:action.data['usdtStr'],
                zuibiteIndexStr:action.data['zuibiteIndexStr'],
                bitmexLeaderBoardPercent:action.data['BLBS'],
                binanceFutureRate:action.data['BINF'],
                bitmexFutureRate:action.data['BITF'],
                okexFutureRate:action.data['OFS'],
            })
        case UPDATE_MSG_I:
            return Object.assign({}, state, {
                todayPriceStr:action.data['todayPriceStr']
            })
        case UPDATE_MSG_J:
            return Object.assign({}, state, {
                liquidationStrB:action.data['liquidationStrB'],
                huobiSLiquidationStr:action.data['HS'],
                huobiLiquidationStr:action.data['hLiquidationStr'],
                binanceLiquidationStr:action.data['Bin'],
                bitmexLiquidationStrB:action.data['BS']
            })
        case UPDATE_MSG_K:
            return Object.assign({}, state, {
                historyLikeStr:action.data['historyLikeStr'],
                historyLikeTStr:action.data['historyLikeTStr'],
            })
        // case UPDATE_MSG_G:
        //     return Object.assign({}, state, {
        //         historyData:{bitS:action.data['bitS'],binH:action.data['binH'],bitH:action.data['bitH'],huoS:action.data['huoS'],okQH:action.data['okQH'],okFH:action.data['okFH'],okWH:action.data['okWH'],huoWH:action.data['huoWH'],huoQH:action.data['huoQH']}
        //     })
        case UPDATE_MSG_L:
            return Object.assign({}, state, {
                tradeStatisticsStr:action.data['tradeStatisticsStr'],
                nowFundsCoinIndex:action.data['index']
            })
        case UPDATE_MSG_M:
            return Object.assign({}, state, {
                largeTradeStr:action.data['largeTradeStr'],
                contactLargeTradeStr:action.data['CLTR']
            })
        case UPDATE_MSG_N:
            let bigDataStr = action.data['BDS'].split("=")
            let historyPositionArr = action.data['BDHS'].split("=")
            for(let a=0;a<historyPositionArr.length;a++){
                historyPositionArr[a] = historyPositionArr[a].split("$")
            }

            return Object.assign({}, state, {
                bigDataStr:bigDataStr,
                bigDataHistoryStr:historyPositionArr,
                bigDataIndex:parseInt(action.data['index'])
            })
        case UPDATE_MSG_O:
            return Object.assign({}, state, {
                huobiCostStr:action.data['huobiCost'],
                binanceCostStr:action.data['binanceCost'],
                okexCostStr:action.data['okexCost'],
                bitfinexCostStr:action.data['bitfinexCost'],
            })
        case UPDATE_MSG_P:
            return Object.assign({}, state, {
                longsAndShortsHistoryStr:action.data['LASHS']
            })
        case UPDATE_MSG_Q:
            return Object.assign({}, state, {
                usdtHistoryStr:action.data['USDT']
            })
        case UPDATE_MSG_R:
            return Object.assign({}, state, {
                cTradeStatisticsStr:action.data['tradeStatisticsStr']
            })
        case UPDATE_MSG_ZI:
            return Object.assign({}, state, {
                todayPriceStr:action.data['todayPriceStr'],
                huobiContractPriceStr:action.data['huobiContractPriceStr'],
                huobiWeekContractPriceStr:action.data['HCW'],
                bitmexContractPriceStr:action.data['BPS'],
                bitfinexSpotPriceStr:action.data['BIPS'],
                binanceFuturePriceStr:action.data['BFP'],
                longsAndShortsStr:action.data['longsAndShortsStr'],
                okexQuarterPriceStr:action.data['okexQuarterPriceStr'],
                okexWeekPriceStr:action.data['OWP'],
                okexForeverPriceStr:action.data['OFP'],
                okcoinPriceStr:action.data['okcoinPriceStr'],
                usdtStr:action.data['usdtStr'],
                zuibiteIndexStr:action.data['zuibiteIndexStr'],
                huobiZuibiteIndexHistoryStr:action.data['HZIHS'],
                binanceZuibiteIndexHistoryStr:action.data['BZIHS'],
            })

        case UPDATE_MSG_FEAR:
            return Object.assign({}, state, {
                todayPriceStr:action.data['todayPriceStr'],
                huobiContractPriceStr:action.data['huobiContractPriceStr'],
                huobiWeekContractPriceStr:action.data['HCW'],
                bitmexContractPriceStr:action.data['BPS'],
                bitfinexSpotPriceStr:action.data['BIPS'],
                binanceFuturePriceStr:action.data['BFP'],
                longsAndShortsStr:action.data['longsAndShortsStr'],
                okexQuarterPriceStr:action.data['okexQuarterPriceStr'],
                okexWeekPriceStr:action.data['OWP'],
                okexForeverPriceStr:action.data['OFP'],
                okcoinPriceStr:action.data['okcoinPriceStr'],
                usdtStr:action.data['usdtStr'],
                zuibiteIndexStr:action.data['zuibiteIndexStr'],
                fearHistoryStr:action.data['FIHS']
            })
        case UPDATE_LOW_AND_HIGN:
            return Object.assign({}, state, {
                lowAndHignData:action.data,
            })
        case UPDATE_ARTICLE_DATA:
            return Object.assign({}, state, {
                articleData:action.data,
            })
        case UPDATE_DEPTH_DATA:
            return Object.assign({}, state, {
                depthData:action.data,
            })
        case SHOW_ARTICLE_UPDATE:
            return Object.assign({}, state, {
                showArticleUpdate:action.result,
            })

        default:
            return state;
    }
}
