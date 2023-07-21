import {message} from "antd";

export const  addSelectTypeArr=["all","other","trade","open","close","stop"]

export const  addSelectTypeObj = {
    "all":"全部设置",
    "other":"其他设置",
    "trade":"交易相关",
    "open":"开仓相关",
    "close":"平仓相关",
    "stop":"止盈止损相关"}

export const sortTypeArr =[
    "wave",
    "nowRise",
    "nowDown",
    "allRise",
    "allDown",
    "todayRise",
    "todayDown",
    "oneDayRise",
    "oneDayDown"
]
export const sortTypeObj ={
    "wave":"波动率排序",
    "nowRise":"新线上涨排序",
    "nowDown":"新线下跌排序",
    "allRise":"区间上涨排序",
    "allDown":"区间下跌排序",
    "todayRise":"今日上涨排序",
    "todayDown":"今日下跌排序",
    "oneDayRise":"24小时上涨排序",
    "oneDayDown":"24小时下跌排序"
}
export const keyboardFunArr = [
    {
        "type":"other",
        "index":0,
        "english":"switchKlineInterval",
        "chinese":"切换为para分钟K线",
        "paraRuleArr":[{"explain":"K线的时间间隔","type":"select","value":[{"name":"1分钟","value":"1"},{"name":"15分钟","value":"15"},{"name":"1小时","value":"60"},{"name":"4小时","value":"240"},{"name":"1天","value":"960"},{"name":"1周","value":"6720"},{"name":"1月","value":"28800"}]}],
        "explain":"示例：选择15分钟，下方K线切换为15分钟时间间隔"

    },
    {
        "type":"other",
        "index":1,
        "english":"switchAccount",
        "chinese":"切换账号",
        "paraRuleArr":[],
        "explain":"设置后按键会切换你的账号，需要绑定多个api key才会生效"

    },
    {
        "type":"other",
        "index":2,
        "english":"switchShowMode",
        "chinese":"切换显示模式（精简/全部）",
        "paraRuleArr":[],
        "explain":"精简模式适合较低配置的电脑，按键后会仅显示经过排序规则后的前三十个币种"
    },
    {
        "type":"other",
        "index":3,
        "english":"openBinanceWeb",
        "chinese":"打开选择币种的币安页面",
        "paraRuleArr":[],
        "explain":"按键后会打开相应币种的币安交易页面"
    },
    {
        "type":"trade",
        "index":4,
        "english":"switchTradeMoney",
        "chinese":"投注额切换为para美金",
        "paraRuleArr":[{
            "explain":"单次交易金额（USD）",
            "type":"inputNumber",
            "rule":{"precision":0,"min":10,"max":100000000,"addonAfter":"USD","prefix":""},
            "value":(para)=>{if(parseInt(para)>0&&parseInt(para)<100000000){return true}else{message.error("请输入0到100000000")}}}],
        "explain":"示例：填写100，按键后会切换你的单次交易金额为100 USD"
    },
    {
        "type":"other",
        "index": 5,
        "english": "changeSortType",
        "chinese": "切换排序方式为para",
        "paraRuleArr": [{
            "explain":"下方K线排序规则",
            "type": "select",
            "value": [{"name": "波动率排序", "value": "wave"}, {
                "name": "最新一条线涨幅排序",
                "value": "nowRise"
            }, {"name": "最新一条线跌幅排序", "value": "nowDown"}, {
                "name": "区间涨幅排序",
                "value": "allRise"
            }, {"name": "区间降幅排序", "value": "allDown"}
                , {"name": "24小时跌幅排序", "value": "oneDayDown"}
                , {"name": "24小时涨幅排序", "value": "oneDayRise"}
                , {"name": "今天跌幅排序", "value": "todayDown"}
                , {"name": "今天涨幅排序", "value": "todayRise"}]
        }],
        "explain":"示例：选择波动率排序，按键后会，币种会以波动率大小进行排序，波动率指当前图表每一条线的开始价格和结束价格的变化率的绝对值全部相加"
    },
    {
        "type":"other",
        "index":6,
        "english":"lockSort",
        "chinese":"锁定/解锁当前币种排序",
        "paraRuleArr":[],
        "explain":"按键后会锁定的话，币种将不会再实时排序，建议和强制刷新一起使用"
    },
    {
        "type":"other",
        "index":7,
        "english":"oneForceUpdateSort",
        "chinese":"强制刷新排序一次",
        "paraRuleArr":[],
        "explain":"按键后会按照排序规则强制刷新一次，建议和锁定排序一起使用"
    },
    {
        "type":"stop",
        "index":8,
        "english":"stopLossOrProfitByPercent",
        "chinese":"止盈止损（百分比） - 盈利亏损 para% ，para",
        "paraRuleArr":[
            {
                "explain":"盈利或者亏损百分比",
                "type": "inputNumber",
                "rule":{"precision":2,"min":0.01,"max":99.99,"addonAfter":"%","prefix":""},
                "value": (para)=>{if(parseInt(para)>=0&&parseInt(para)<100){return true}else{message.error("请输入0到100之间的数字")}}
            },
            {
                "explain":"选择止盈还是止损",
                "type": "select",
                "value": [
                    {"name": "止盈", "value": "stopProfit"},
                    {"name": "止损", "value": "stopLoss"}]
            }
        ],
        "explain":"示例：【参数1】为2，第【参数2】为止损，假如您的比特币仓位成本价为10000，" +
            "按键后系统将挂出9800的计划市价平仓单，假如第【参数2】为止盈，则会挂出10200的挂单，" +
            "止盈止损计划单和挂单的价值将等于你的当前仓位，且挂出新的止盈止损订单后，会取消当前币种前面的止盈止损订单"
    },
    {
        "type":"stop",
        "index":9,
        "english":"stopLossOrProfitByTime",
        "chinese":"止盈止损（分钟线极点） -  最近para分钟价格乘以para，para",
        "paraRuleArr":[{
            "explain":"指定分钟数1到720000(500天)的极点止盈止损",
            "type": "inputNumber",
            "rule":{"precision":0,"min":1,"max":720000,"addonAfter":"分钟","prefix":""},
            "value": (para)=>{if(parseInt(para)>0&&parseInt(para)<=60*24*30){return true}else{message.error("请输入1到720000(500天)之间的数字")}}
        },{
            "explain":"价格修正系数，最终订单价格会以设置的单次交易金额乘以这个系数，1为不修正",
            "type": "inputNumber",
            "rule":{"precision":8,"min":0.00000001,"max":10,"prefix":""},
            "value": (para)=>{if(parseFloat(para)>0&&parseFloat(para)<100){return true}else{message.error("请输入0到10之间的数字")}}
        },{
            "explain":"选择止盈还是止损",
            "type": "select",
            "value": [
                {"name": "止盈", "value": "stopProfit"},
                {"name": "止损", "value": "stopLoss"}]
        }],
        "explain":"示例：【参数1】填写为15，【参数2】填写为0.999，【参数3】为止损，设置后，按键时候，如果选中币种有多头仓，系统将自动读取最近15分钟的最低点，" +
            "并乘以0.999后，将该价格设置为计划市价平仓单，假如【参数3】为止盈，系统将自动读取最近15分钟的最高点，将该价格设置为挂单，" +
            "止盈止损计划单和挂单的价值将等于你的当前仓位，且挂出新的止盈止损订单后，会取消当前币种前面的止盈止损订单"
    },
    {
        "type":"stop",
        "index":10,
        "english":"stopLossOrProfitByMoney",
        "chinese":"止盈止损（盈亏金额） - 盈利或者亏损paraUSD，para",
        "paraRuleArr":[{
            "explain":"止盈止损时仓位损失或者盈利的金额",
            "type": "inputNumber",
            "rule":{"precision":2,"min":0.01,"max":100000000,"addonAfter":"USD","prefix":""},
            "value": (para)=>{if(parseInt(para)>0&&parseInt(para)<100000000){return true}else{message.error("请输入0到100000000之间的数字")}}
        },{
            "explain":"选择止盈还是止损",
            "type": "select",
            "value": [
                {"name": "止盈", "value": "stopProfit"},
                {"name": "止损", "value": "stopLoss"}]
        }],
        "explain":"示例：【参数1】填写为1000，【参数2】填写为止盈，如果选中币种有多头仓位，" +
            "则会根据成本价和持仓仓位自动计算出盈利1000usd的止盈价格并挂单，假设【参数2】设置为止损，则会根据成本价和持仓仓位自动计算出亏损1000usd的止盈价格并挂计划单"
    },
    {
        "type":"open",
        "index":11,
        "english":"marketOpen",
        "chinese":"开仓（对手价） - 对手价开para",
        "paraRuleArr":[{
            "explain":"选择开多还是开空",
            "type": "select",
            "value": [
                {"name": "多", "value": "longs"},
                {"name": "空", "value": "shorts"}]
        }],
        "explain":"设置后，按键时候将直接以市价开多开空"
    },
    {
        "type":"open",
        "index":12,
        "english":"depthOpen",
        "chinese":"开仓（盘口价格） - para第para档乘以para开para，且para",
        "paraRuleArr":[{
            "explain":"中间价指(买一价+卖一价)/2",
            "type": "select",
            "value": [
                {"name": "买盘", "value": "buy"},
                {"name": "卖盘", "value": "sell"},
                {"name": "中间价", "value": "mid"}

            ]
        },{
            "explain":"买卖盘第几档价格，选择中间价此项无效，但需要随意填写一个数字",
            "type": "inputNumber",
            "rule":{"precision":0,"min":1,"max":50,"addonAfter":"档","prefix":""},
            "value": (para)=>{if(parseInt(para)>0&&parseInt(para)<=50){return true}else{message.error("请输入1到50之间的数字")}}
        },{
            "explain":"价格修正系数，最终订单价格会乘以这个系数，1为不修正",
            "type": "inputNumber",
            "rule":{"precision":8,"min":0.00000001,"max":10,"prefix":""},
            "value": (para)=>{if(parseFloat(para)>=0&&parseFloat(para)<=10){return true}else{message.error("请输入0到10之间的数字")}}
        },{
            "explain":"选择开多还是开空",
            "type": "select",
            "value": [
                {"name": "多", "value": "openLongsByDepth"},
                {"name": "空", "value": "openShortsByDepth"}]
        },{
            "explain":"仅挂单下只做maker，价格快速变化导致无法挂单，订单会取消",
            "type": "select",
            "value": [
                {"name": "不限制", "value": "GTC"},
                {"name": "仅挂单", "value": "GTX"}]
        }],
        "explain":"示例：【参数1】设置为买盘，【参数2】设置为1，【参数3】设置为0.999，【参数4】设置为多，【参数5】设置为仅挂单，" +
            "按键时，会按照该交易对最新买盘 ，买一价格乘以0.999，挂出多单，且仅能挂单，如果挂出去的时候价格快速下跌导致无法挂单，则订单将会被取消"
    },
    {
        "type":"open",
        "index":13,
        "english":"leftOpen",
        "chinese":"开仓（极点左侧逆势） - 最近para分钟极点乘以para开para",
        "paraRuleArr":[{
            "explain":"价格采用过去多少分钟极点",
            "type": "inputNumber",
            "rule":{"precision":0,"min":1,"max":720000,"addonAfter":"分钟","prefix":""},
            "value": (para)=>{if(parseInt(para)>0&&parseInt(para)<=60*24*30){return true}else{message.error("请输入1到720000(500天)之间的数字")}}
        },{
            "explain":"价格修正系数，最终订单价格会乘以这个系数，1为不修正",
            "type": "inputNumber",
            "rule":{"precision":8,"min":0.00000001,"max":10,"prefix":""},
            "value": (para)=>{if(parseFloat(para)>=0&&parseFloat(para)<=10){return true}else{message.error("请输入0到10之间的数字")}}
        },{
            "explain":"选择开多还是开空",
            "type": "select",
            "value": [
                {"name": "多", "value": "openLongsByLeft"},
                {"name": "空", "value": "openShortsByLeft"}]
        }],
        "explain":"示例：【参数1】设置为15，【参数2】设置为0.999，【参数3】设置为多，按键时，会读取交易对最近十五分钟最低点乘以0.999，挂出多单，假设设置为空，则会照该币种最近十五分钟最高点乘以0.999，挂出空单"
    },
    {
        "type":"open",
        "index":14,
        "english":"batchPercentOpen",
        "chinese":"开仓（批量订单） - para第para档乘以para开para ，单次变化para%，分单数para，para",
        "paraRuleArr":[{
            "explain":"中间价指(买一价+卖一价)/2",
            "type": "select",
            "value": [
                {"name": "买盘", "value": "buy"},
                {"name": "卖盘", "value": "sell"},
                {"name": "中间价", "value": "mid"}

            ]
        },{
            "explain":"选择基础价格为买卖盘第几档价格，选择中间价此项无效",
            "type": "inputNumber",
            "rule":{"precision":0,"min":1,"max":50,"addonAfter":"档","prefix":""},
            "value": (para)=>{if(parseInt(para)>0&&parseInt(para)<=50){return true}else{message.error("请输入1到50之间的数字")}}
        },{
            "explain":"基础价格修正系数，基础价格会乘以这个系数，1为不修正",
            "type": "inputNumber",
            "rule":{"precision":8,"min":0.00000001,"max":10,"prefix":""},
            "value": (para)=>{if(parseFloat(para)>=0&&parseFloat(para)<=10){return true}else{message.error("请输入0到10之间的数字")}}
        },{
            "explain":"选择开多还是开空",
            "type": "select",
            "value": [
                {"name": "多", "value": "openLongsByBatch"},
                {"name": "空", "value": "openShortsByBatch"}]
        },{
            "explain":"开多，为每单减少百分比，开空，为每单变化百分比，核心逻辑为更加远离初始开仓价格，0为特殊模式，表示每单增加或减少该交易对最小价格精度",
            "type": "inputNumber",
            "rule":{"precision":2,"min":0,"max":50,"addonAfter":"%","prefix":""},
            "value": (para)=>{if(parseInt(para)>0&&parseInt(para)<50){return true}else{message.error("请输入0到50之间的数字")}}
        },{
            "explain":"要拆分的单数",
            "type": "inputNumber",
            "rule":{"precision":0,"min":2,"max":10,"addonAfter":"单","prefix":""},
            "value": (para)=>{if(parseInt(para)>1&&parseInt(para)<11){return true}else{message.error("请输入2到10之间的数字")}}
        },{
            "explain":"仅挂单下只做maker，价格快速变化导致无法挂单，订单会取消",
            "type": "select",
            "value": [
                {"name": "不限制", "value": "GTC"},
                {"name": "仅挂单", "value": "GTX"}]
        }
        ],
        "explain":"示例：【参数1】：买盘，【参数2】:1，【参数3】：0.999，【参数4】：开多，【参数5】：0.999，【参数6】：5，【参数7】：不限制，"
            +"按键后会取该交易对买一价格，以10000.00为基础价格，基础价格乘以基础价格系数0.999得到99900后，依次乘以0.999，最后获得五个价格[99900.00  ,  99900.00*0.999  ,  99900.00*0.999*0.999  ,  99900.00*0.999*0.999*0.999  ,  99900.00*0.999*0.999*0.999*0.999  ]，挂出多单，"
            +"特殊模式示例：【参数1】：买盘，【参数2】:1，【参数3】：0.999，【参数4】：开多，【参数5】：0，【参数6】：5，【参数7】：不限制，"
            +"按键后会取该交易对买一价格，以10000.00为例，依次-0.01（交易对最小交易价格精度），获得五个价格[10000.00,9999.99,9999.98,9999.97,9999.96]，分别都乘以0.999后，挂出多单。"
    },
    {
        "type":"close",
        "index":15,
        "english":"forceCloseByAccount",
        "chinese":"平仓（市价） - 市价关闭账户现有所有仓位",
        "paraRuleArr":[],
        "explain":"按键后会市价关闭现有所有仓位，包含但不仅限于选中币种"

    },{
        "type":"close",
        "index":16,
        "english":"forceCloseBySelectCoin",
        "chinese":"平仓（市价） - 市价关闭选中币种所有仓位",
        "paraRuleArr":[],
        "explain":"按键后会市价关选中币种的所有仓位"

    }, {
        "type": "close",
        "index": 17,
        "english": "selectCoinCloseByBatch",
        "chinese": "平仓（批量订单） - 选中的币种按下方交易金额乘以para，以para盘口第para档乘以para（多仓）或para（空仓）的价格为基准价格，每单变化para%，分para单，且para",
        "paraRuleArr": [{
            "explain": "金额修正系数，最终金额为设置的交易金额乘以这个系数，1为不修正",
            "rule": {"precision": 8, "min": 0.00000001, "max": 10, "prefix": ""},
            "type": "inputNumber",
            "value": (para) => {
                if (parseFloat(para) > 0 && parseFloat(para) <= 10) {
                    return true
                } else {
                    message.error("请输入0到10之间的数字")
                }
            }
        }, {
            "explain": "正向：空仓选择买盘，多仓选择卖盘，反之亦同",
            "type": "select",
            "value": [
                {"name": "正向", "value": "positive"},
                {"name": "反向", "value": "reverse"}]
        }, {
            "explain": "买卖盘第几档价格",
            "rule": {"precision": 0, "min": 1, "max": 50, "addonAfter": "档", "prefix": ""},
            "type": "inputNumber",
            "value": (para) => {
                if (parseInt(para) >= 1 && parseInt(para) <= 50) {
                    return true
                } else {
                    message.error("请输入1到50之间的数字")
                }
            }
        }, {
            "explain": "多仓平多的价格修正系数，最终订单价格会乘以这个系数，1为不修正",
            "rule": {"precision": 8, "min": 0.00000001, "max": 10, "prefix": ""},
            "type": "inputNumber",
            "value": (para) => {
                if (parseFloat(para) >= 0 && parseFloat(para) <= 10) {
                    return true
                } else {
                    message.error("请输入0到10之间的数字")
                }
            }
        },{
            "explain": "空仓平空价格修正系数，最终订单价格会乘以这个系数，1为不修正",
            "rule": {"precision": 8, "min": 0.00000001, "max": 10, "prefix": ""},
            "type": "inputNumber",
            "value": (para) => {
                if (parseFloat(para) >= 0 && parseFloat(para) <= 10) {
                    return true
                } else {
                    message.error("请输入0到10之间的数字")
                }
            }
        }, {
            "explain": "多仓时，为每单变化百分比，空仓为每单减少百分比，核心逻辑为更加远离初始开仓价格，0为特殊模式，表示每单增加或减少该交易对最小价格精度",
            "type": "inputNumber",
            "rule": {"precision": 2, "min": 0, "max": 50, "addonAfter": "%", "prefix": ""},
            "value": (para) => {
                if (parseInt(para) > 0 && parseInt(para) < 50) {
                    return true
                } else {
                    message.error("请输入0到50之间的数字")
                }
            }
        }, {
            "explain": "要拆分的单数",
            "type": "inputNumber",
            "rule": {"precision": 0, "min": 2, "max": 10, "addonAfter": "单", "prefix": ""},
            "value": (para) => {
                if (parseInt(para) > 1 && parseInt(para) < 11) {
                    return true
                } else {
                    message.error("请输入2到10之间的数字")
                }
            }
        },{
            "explain": "仅挂单下只做maker，价格快速变化导致无法挂单，订单会取消",
            "type": "select",
            "value": [
                {"name": "不限制", "value": "GTC"},
                {"name": "仅挂单", "value": "GTX"}]
        }],
        "explain": "示例：【参数1】：0.5，【参数2】正向，【参数3】1，【参数4】1.0001，【参数5】1，【参数6】0.5，【参数7】 5，【参数8】不限制，" +
            "按键后，选中币种如果有多仓，会拆分成五单，每单按照下方交易金额乘以0.5除以5进行平仓，平仓价格组【 卖盘第一档*1.0001（基准价格） ，基准价格*1.005  ，基准价格*1.005*1.005  ，基准价格*1.005*1.005*1.005 ，基准价格*1.005*1.005*1.005*1.005】"
    },{
        "type":"close",
        "index":18,
        "english":"selectCoinCloseByDepth",
        "chinese":"平仓（盘口价格） - 选中的币种按下方交易金额乘以para，以para盘口第para档乘以para（多仓）或para（空仓）的价格平仓，且para",
        "paraRuleArr":[{
            "explain":"金额修正系数，最终金额为设置的交易金额乘以这个系数，1为不修正",
            "rule":{"precision":8,"min":0.00000001,"max":10,"prefix":""},
            "type": "inputNumber",
            "value": (para)=>{if(parseFloat(para)>0&&parseFloat(para)<=10){return true}else{message.error("请输入0到10之间的数字")}}
        },{
            "explain":"正向：空仓选择买盘，多仓选择卖盘，反向：空仓选择卖盘，多仓选择买盘",
            "type": "select",
            "value": [
                {"name": "正向", "value": "positive"},
                {"name": "反向", "value": "reverse"},
                {"name": "盘口中间价", "value": "mid"}]
        },{
            "explain":"买卖盘第几档价格，选择中间价此处不影响，但请随便填写个数值",
            "rule":{"precision":0,"min":1,"max":50,"addonAfter":"档","prefix":""},
            "type": "inputNumber",
            "value": (para)=>{if(parseInt(para)>=1&&parseInt(para)<=50){return true}else{message.error("请输入1到50之间的数字")}}
        },{
            "explain":"多仓平多，实际订单方向为卖时，价格修正系数，最终订单价格会乘以这个系数，1为不修正",
            "rule":{"precision":8,"min":0.00000001,"max":10,"prefix":""},
            "type": "inputNumber",
            "value": (para)=>{if(parseFloat(para)>=0&&parseFloat(para)<=10){return true}else{message.error("请输入0到10之间的数字")}}
        },{
            "explain":"空仓平空，实际订单方向为买时，价格修正系数，最终订单价格会乘以这个系数，1为不修正",
            "rule":{"precision":8,"min":0.00000001,"max":10,"prefix":""},
            "type": "inputNumber",
            "value": (para)=>{if(parseFloat(para)>=0&&parseFloat(para)<=10){return true}else{message.error("请输入0到10之间的数字")}}
        },{
            "explain":"仅挂单下只做maker，价格快速变化导致无法挂单，订单会取消",
            "type": "select",
            "value": [
                {"name": "不限制", "value": "GTC"},
                {"name": "仅挂单", "value": "GTX"}]
        }],
        "explain":"示例：【参数1】：0.5，【参数2】正向，【参数3】1，【参数4】0.9999，【参数5】1.0001，【参数6】不限制，" +
            "按键后，选中币种如果有多仓，会按照下方交易金额*0.5进行平仓，平仓价格为卖盘第一档*0.9999，"+
            "选中币种如果有空仓，会按照下方交易金额*0.5进行平仓，平仓价格为买盘第一档*1.0001"

    },
    {
        "type":"other",
        "index":19,
        "english":"switchNavigateShowType",
        "chinese":"切换下方导航栏模式 - 全部，省略，仓位，挂单",
        "paraRuleArr":[],
        "explain":"按键后会切换下方导航栏显示模式 - 全部，省略，仓位，挂单"

    },
    {
        "type":"trade",
        "index":20,
        "english":"cancelOrdersBySelectSymbol",
        "chinese":"取消选中币种的所有挂单",
        "paraRuleArr":[],
        "explain":"按键后会取消选中币种的全部挂单"

    },
    {
        "type":"trade",
        "index":21,
        "english":"cancelOrdersByAccount",
        "chinese":"取消该账户的所有挂单",
        "paraRuleArr":[],
        "explain":"按键后会取消该账户的全部挂单"

    },
    {
        "type":"stop",
        "index":22,
        "english":"stopLossOrProfitByPercentBatch",
        "chinese":"止盈止损（批量订单） - 起始para% ，单次变化para%，分单数para，para",
        "paraRuleArr":[{
            "explain":"止盈止损起始百分比",
            "type": "inputNumber",
            "rule":{"precision":2,"min":0.01,"max":50,"addonAfter":"%","prefix":""},
            "value": (para)=>{if(parseInt(para)>0&&parseInt(para)<50){return true}else{message.error("请输入0.01到50之间的数字")}}
        },{
            "explain":"止损：仓位为多，此处为每单减少百分比，仓位为空，此处为每单变化百分比，止盈则相反，核心逻辑为更加远离成本价",
            "type": "inputNumber",
            "rule":{"precision":2,"min":0.01,"max":50,"addonAfter":"%","prefix":""},
            "value": (para)=>{if(parseInt(para)>0&&parseInt(para)<50){return true}else{message.error("请输入0.01到50之间的数字")}}
        },{
            "explain":"要拆分的单数",
            "type": "inputNumber",
            "rule":{"precision":0,"min":2,"max":10,"addonAfter":"单","prefix":""},
            "value": (para)=>{if(parseInt(para)>1&&parseInt(para)<11){return true}else{message.error("请输入2到10之间的数字")}}
        },{
            "explain":"选择止盈还是止损",
            "type": "select",
            "value": [
                {"name": "止盈", "value": "stopProfit"},
                {"name": "止损", "value": "stopLoss"}]
        }],
        "explain":"示例：【参数1】填写为1，【参数2】填写为0.5，【参数3】填写为2，【参数4】填写为止损，仓位方向为多仓" +
            "则会根据成本价，挂出2个止损单，止损价格分别为 成本价*0.99以及成本价*0.985"
    },
    {
        "type":"open",
        "index":23,
        "english":"rightOpen",
        "chinese":"开仓（极点右侧突破） - 最近para分钟极点乘以para开para",
        "paraRuleArr":[{
            "explain":"触发价格采用过去多少分钟极点",
            "type": "inputNumber",
            "rule":{"precision":0,"min":1,"max":720000,"addonAfter":"分钟","prefix":""},
            "value": (para)=>{if(parseInt(para)>0&&parseInt(para)<=60*24*30){return true}else{message.error("请输入1到720000(500天)之间的数字")}}
        },{
            "explain":"挂单价格修正系数，最终订单价格会乘以这个系数，1为不修正",
            "type": "inputNumber",
            "rule":{"precision":8,"min":0.00000001,"max":10,"prefix":""},
            "value": (para)=>{if(parseFloat(para)>=0&&parseFloat(para)<=10){return true}else{message.error("请输入0到10之间的数字")}}
        },{
            "explain":"选择开多还是开空",
            "type": "select",
            "value": [
                {"name": "多", "value": "openLongsByRight"},
                {"name": "空", "value": "openShortsByRight"}]
        }],
        "explain":"示例：【参数1】设置为15，【参数2】设置为1.01，【参数3】设置为多，按键时，会读取交易对最近十五分钟最高点作为触发价格，挂出触发价格乘以1.01的计划多单，假设设置为空，则会照该币种最近十五分钟最低点乘以0.999，" +
            "挂出计划空单，右侧突破和左侧逆势的挂单方案是有区别的，左侧逆势采取挂单形式，占用你的保证金，但是只要挂出就一定挂出，右侧突破本质是币安的计划开仓，价格到达后由币安服务器再进行挂单，如果此时账户保证金不足可能会因此而挂单失败"
    }

]
export const realHotKeyConfigDefaultObj = {"49": {"index": 4, "paraArr": [100]}, "50": {"index": 4, "paraArr": ["200"]}, "51": {"index": 4, "paraArr": ["500"]}, "53": {"index": 22, "paraArr": [3, 0.5, 6, "stopLoss"]}, "65": {"index": 12, "paraArr": ["sell", 1, 1.0001, "openLongsByDepth", "GTC"]}, "66": {"index": 22, "paraArr": [2, 0.5, 5, "stopLoss"]}, "68": {"index": 20, "paraArr": []}, "71": {"index": 12, "paraArr": ["buy", 1, 0.9999, "openShortsByDepth", "GTC"]}, "72": {"index": 14, "paraArr": ["sell", 1, 1, "openShortsByBatch", 0.1, 5, "GTX"]}, "76": {"index": 6, "paraArr": []}, "79": {"index": 3, "paraArr": []}, "80": {"index": 2, "paraArr": []}, "81": {"index": 15, "paraArr": []}, "82": {"index": 17, "paraArr": [0.5, "positive", 1, 1, 1, 0.05, 5, "GTX"]}, "83": {"index": 14, "paraArr": ["buy", 1, 1, "openLongsByBatch", 0.1, 5, "GTX"]}, "84": {"index": 16, "paraArr": []}, "86": {"index": 1, "paraArr": []}, "88": {"index": 21, "paraArr": []}, "90": {"index": 19, "paraArr": []}, "96": {"index": 7, "paraArr": []}, "97": {"index": 0, "paraArr": ["1"]}, "98": {"index": 0, "paraArr": ["15"]}, "99": {"index": 0, "paraArr": ["60"]}, "100": {"index": 5, "paraArr": ["allRise"]}, "101": {"index": 5, "paraArr": ["allDown"]}, "103": {"index": 5, "paraArr": ["wave"]}, "104": {"index": 5, "paraArr": ["nowRise"]}, "105": {"index": 5, "paraArr": ["nowDown"]}}
export const keyboardObj = {
    "65":"a",
    "66":"b",
    "67":"c",
    "68":"d",
    "69":"e",
    "70":"f",
    "71":"g",
    "72":"h",
    "73":"i",
    "74":"j",
    "75":"k",
    "76":"l",
    "77":"m",
    "78":"n",
    "79":"o",
    "80":"p",
    "81":"q",
    "82":"r",
    "83":"s",
    "84":"t",
    "85":"u",
    "86":"v",
    "87":"w",
    "88":"x",
    "89":"y",
    "90":"z",
    "48":"大键盘 0",
    "49":"大键盘 1",
    "50":"大键盘 2",
    "51":"大键盘 3",
    "52":"大键盘 4",
    "53":"大键盘 5",
    "54":"大键盘 6",
    "55":"大键盘 7",
    "56":"大键盘 8",
    "57":"大键盘 9",
    "96":"小键盘 0",
    "97":"小键盘 1",
    "98":"小键盘 2",
    "99":"小键盘 3",
    "100":"小键盘 4",
    "101":"小键盘 5",
    "102":"小键盘 6",
    "103":"小键盘 7",
    "104":"小键盘 8",
    "105":"小键盘 9",
    "189":"大键盘 -",
    "187":"大键盘 =",
    "219":"大键盘 [",
    "221":"大键盘 ]",
    "186":"大键盘 ;",
    "222":"大键盘 '",
    "188":"大键盘 ,",
    "190":"大键盘 .",
    "191":"大键盘 /",
    "8":"大键盘 Delete",
    "17":"control",
    "18":"alt",
    "192":"大键盘 `",
    "13":"Enter",
    "107":"小键盘 +",
    "109":"小键盘 -",
    "106":"小键盘 * `",
    "111":"小键盘 /",
    "110":"小键盘 .",
}