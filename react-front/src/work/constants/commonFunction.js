import {message} from 'antd';


export const supportKlineIntervalEnglish = ["1m","15m","1h","4h","1d","1w","1M"]
export const supportKlineIntervalChinese = ["1分钟","15分钟","1小时","4小时","1天","1周","1月"]
export const stateDefaultObj = {
    "autoBuyBnbConfigArr":[25,50,false],//bnb价值小于 参数1 usd的时候，自动购买参数2 usd的bnb，参数3开关
    "depthConfigArr":[25,1,true], //count sizeIndex profit-mode
    "klineCountConfigArr":[96],
    "sortFrequencyTsConfigArr":[3000],
    "binanceAddressConfigArr": ["binance.com"],
    "selectKlineIntervalConfigArr":["4h","15m","1m"],//参数1 第一个表的时间间隔，参数2 第二个表的时间间隔，参数3 第三个表的时间间隔，
    "klineRowCountConfigArr":[4],
    "autoStopLossConfigArr":["percent",[2,0.1,2],false],//参数1：止损类型:time,percent,money,batch，参数2：止损参数，参数3开关
    "autoCancelStopLossConfigArr":[true],
    "limitMaxPositionLockConfigArr":[5000,5000,false],
    "limitMaxLossLockConfigArr":["15m",5000,30,false],
    "mindModeConfigArr":[false],//图表收益率，仓位收益率，账号资产统计
    "showProfitWithLeverConfigArr":[true],
    "rocketLimitConfigArr":[5,0.8,0.8],
    "autoCancelOrderConfigArr":[180,false],
    "binanceRecommissionConfigArr":[0],
    "limitTimeMaxPositionConfigArr":[5000,false],
    "shieldLossSymbolConfigArr":["15m",1,false]

}
export const getStopLossPriceArrByPercent=(cost,stopLossBeginPercent,stopLossAddPercent,autoStopLossCount,direction)=>{
    let stopLossPriceArr = []

    if (direction == "longs") {
        for (let a = 0; a < autoStopLossCount; a++) {
            stopLossPriceArr.push(cost * (1 - stopLossBeginPercent / 100 - stopLossAddPercent / 100 * a))
        }
        return  stopLossPriceArr
    } else if (direction == "shorts") {
        for (let a = 0; a < autoStopLossCount; a++) {
            stopLossPriceArr.push(cost * (1 + stopLossBeginPercent / 100 + stopLossAddPercent / 100 * a))
        }
        return  stopLossPriceArr
    }else{
        return [0]
    }
}
export const getStopLossPriceByPercent=(cost,percent,direction)=>{
    if(direction=="longs"){
        return cost*(1-percent/100)
    }else if(direction=="shorts"){
        return cost*(1+percent/100)
    }else{
        return 0
    }
}
export const getStopLossPriceByMoney=(cost,lossMoney,allMoney,direction)=>{
    if(direction=="longs"){
        if(lossMoney>allMoney){
            message.error("止损金额大于订单总价值，将按照成本*0.5止损")
            return cost * 0.5
        }
        return cost * (1 - lossMoney / allMoney)
    }else if(direction=="shorts"){
        return cost* (1 + lossMoney / allMoney)
    }
}


export const getStopProfitPriceArrByPercent=(cost,stopLossBeginPercent,stopLossAddPercent,autoStopLossCount,direction)=>{
    let stopProfitPriceArr = []

    if (direction == "longs") {
        for (let a = 0; a < autoStopLossCount; a++) {
            stopProfitPriceArr.push(cost * (1 + stopLossBeginPercent / 100 + stopLossAddPercent / 100 * a))
        }
        return  stopProfitPriceArr
    } else if (direction == "shorts") {
        for (let a = 0; a < autoStopLossCount; a++) {
            stopProfitPriceArr.push(cost * (1 - stopLossBeginPercent / 100 - stopLossAddPercent / 100 * a))
        }
        return  stopProfitPriceArr
    }else{
        return [0]
    }
}
export const getStopProfitPriceByPercent=(cost,percent,direction)=>{
    if(direction=="longs"){
        return cost*(1+percent/100)
    }else if(direction=="shorts"){
        return cost*(1-percent/100)
    }else{
        return 0
    }
}
export const getStopProfitPriceByMoney=(cost,profitMoney,allMoney,direction)=>{
    if(direction=="longs"){

        return cost * (1 + profitMoney / allMoney)
    }else if(direction=="shorts"){
        return cost* (1 - profitMoney / allMoney)
    }
}


export const setLocalStorage=(key,value)=>{
    let storage=window.localStorage;
    storage[key]=value
}

export const getLocalStorage=(key)=>{
    let storage=window.localStorage;
    return storage[key]
}

export const randomString=(e)=>{
    e = e || 32;
    var t = "ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678",
        a = t.length,
        n = "";
    for (let i = 0; i < e; i++) n += t.charAt(Math.floor(Math.random() * a));
    return n
}


export const turnTsToTime=(value,turnType="normal")=>{
    if(typeof value=="number") {
        let ts = value
        if (value < 100000000000) {
            ts = ts * 1000
        }
        var date = new Date(ts)
        let year = date.getFullYear();  // 获取完整的年份(4位,1970)
        let month = date.getMonth() + 1;  // 获取月份(0-11,0代表1月,用的时候记得加上1)
        if (month < 10) {
            month = "0" + month
        }
        let day = date.getDate();  // 获取日(1-31)
        if (day < 10) {
            day = "0" + day
        }
        let hours = date.getHours();  // 获取小时数(0-23)
        if (turnType == "4h"){
            hours = hours-hours%4
        }
        if(hours<10){
            hours = "0"+hours
        }
        let mins = date.getMinutes();  // 获取分钟数(0-59)
        if(turnType=="15m"){
            mins = mins-mins%15
        }
        if(mins<10){
            mins = "0"+mins
        }
        let seconds = date.getSeconds();  // 获取秒数(0-59)
        if(seconds<10){
            seconds = "0"+seconds
        }
        if(turnType=="1m"){
            return year+"-"+month+"-"+day+" "+hours+":"+mins+":00"
        }else if(turnType=="15m"){
            return year+"-"+month+"-"+day+" "+hours+":"+mins+":00"
        }else if(turnType=="1h"){
            return year+"-"+month+"-"+day+" "+hours+":00:00"
        }else if(turnType=="4h"){
            return year+"-"+month+"-"+day+" "+hours+":00:00"
        }else if(turnType=="1d"){
            return year+"-"+month+"-"+day+" "+"00:00:00"
        }else if(turnType=="1w"){
            return year+"-"+month+"-"+day+" "+"00:00:00"
        }else if(turnType=="1M"){
            return year+"-"+month+"-"+day+" "+"00:00:00"
        }else if(turnType=="other"){
            return hours+":"+mins
        }
        return year+"-"+month+"-"+day+" "+hours+":"+mins+":"+seconds
    }else{
        var date = new Date(value.replace(/-/g, '/'))
        let ts = date.getTime();
        return parseInt(ts/1000)
    }
}


export const numOmit = (num) =>{
    num = parseFloat(num)
    if(num>=10000){
        return num.toFixed(1)
    }else if(num>=100){
        return (num).toFixed(2)
    }else if(num>=1){
        return (num).toFixed(3)
    }else{
        let str = num.toString()
        let newStr = ""
        let begin=false
        let noNumCount = 0
        for(let a=0;a<str.length;a++){
            let thisChar = str.charAt(a)
            newStr = newStr+thisChar
            if(thisChar!="0"&&thisChar!="."){
                begin = true
            }
            if (begin){
                noNumCount ++
            }
            if(noNumCount>=3){
                break
            }
        }
        return newStr
    }

}

export const getHourTs = (nowTs) =>{
    var hour=(new Date(nowTs).getHours()).toString();
    return new Date(new Date().toLocaleDateString()).getTime()+hour*3600000
}
export const  deepCopy =(obj) =>{
    var result = Array.isArray(obj) ? [] : {};
    for (var key in obj) {
        if (obj.hasOwnProperty(key)) {
            if (typeof obj[key] === 'object' && obj[key]!==null) {
                result[key] = deepCopy(obj[key]);   //递归复制
            } else {
                result[key] = obj[key];
            }
        }
    }
    return result;
};


export const isIphoneXR = () =>{
    // iPhone X、iPhone XS
    var isIPhoneX = /iphone/gi.test(window.navigator.userAgent) && window.devicePixelRatio && window.devicePixelRatio === 3 && window.screen.width === 375 && window.screen.height === 812;
    var isIPhoneXSMax = /iphone/gi.test(window.navigator.userAgent) && window.devicePixelRatio && window.devicePixelRatio === 3 && window.screen.width === 414 && window.screen.height === 896;
    var isIPhoneXR = /iphone/gi.test(window.navigator.userAgent) && window.devicePixelRatio && window.devicePixelRatio === 2 && window.screen.width === 414 && window.screen.height === 896;
    if(isIPhoneXSMax||isIPhoneXR||isIPhoneX){
        return true;
    }else{
        return false;
    }
}

export const isVIP = (VIPTime)=>{
    let timestamp = Date.parse(new Date())/1000;
    if(VIPTime==undefined||VIPTime=="" ){
        return false
    }
    let userVIPTime = parseInt(VIPTime)
    let timeDifferent = userVIPTime-timestamp
    if(timeDifferent<0){
        return false
    }else{
        return true
    }
}
export const isWeixinVerity = (VIPTime)=>{
    let timestamp = Date.parse(new Date())/1000;
    if(VIPTime==undefined||VIPTime=="" ){
        return false
    }
    let userVIPTime = parseInt(VIPTime)
    let timeDifferent = userVIPTime-timestamp
    if(timeDifferent<0){
        return false
    }else{
        return true
    }
}
export const markT = (account,page,subPage,beginTime,number)=>{
    let duration = parseInt((new Date()).getTime())-beginTime
    let formData = new FormData();
    let interval =0
    formData.append("account", account.length<1?"00000000000":account);
    formData.append("page",page);
    formData.append("subPage",subPage);
    formData.append("duration",duration);

    fetch("http://mark.zbtc.vip:8893/mark", {
        method:'POST',
        body:formData
    }).catch((error)=>{
        if(number==0)
            markT(account,page,subPage,beginTime,number+1)
    });
}

export const mark = (account,page,subPage,beginTime,number)=>{
    let duration = parseInt((new Date()).getTime())-beginTime
    let formData = new FormData();
    let interval =0
    formData.append("account", account.length<1?"00000000000":account);
    formData.append("page",page);
    formData.append("subPage",subPage);
    formData.append("duration",duration);

    fetch("http://mark.zbtc.vip:8893/mark", {
        method:'POST',
        body:formData
    }).catch((error)=>{
        if(number==0)
        mark(account,page,subPage,beginTime,number+1)
    });
}


export const generateMixed=(n)=> {
    var chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'];
    var a = "";
    for (var i = 0; i < n; i++) {
        a += chars[Math.ceil(Math.random() * 35)];
    }
    return a;
}


export const isLIVIP = (LIServer)=>{
    if(LIServer=="-1"||LIServer==""  ){
        return false
    }
    return true
}

export const addWan = (integer, number, mutiple, decimalDigit) => {
    var digit = getDigit(integer);
    if (digit > 3) {
        var remainder = digit % 8;
        if (remainder >= 5) { // ‘十万’、‘百万’、‘千万’显示为‘万’
            remainder = 4;
        }
        return Math.round(number / Math.pow(10, remainder + mutiple - decimalDigit)) / Math.pow(10, decimalDigit) + '万';
    } else {
        return Math.round(number / Math.pow(10, mutiple - decimalDigit)) / Math.pow(10, decimalDigit);
    }
}
export const getDigit = (integer) => {
    var digit = -1;
    while (integer >= 1) {
        digit++;
        integer = integer / 10;
    }
    return digit;
}
export const getFearAndGreedChinese= (index)=>{
    if(index=="/"){
        return "/"
    }
    if(index<=20){
        return "极度恐慌"
    }else if(index>20&&index<=40){
        return "恐慌"
    }else if(index>40&&index<=60){
        return "正常"
    }else if(index>60&&index<=80){
        return "贪婪"
    }else if(index>80&&index<=100){
        return "极度贪婪"
    }
}
export const getZuibiteAndHuobiIndexChinese= (index)=>{
    if(index=="/"){
        return "/"
    }
    if(index<=-300){
        return "崩盘"
    }
    else if(index<=-200){
        return "极度低迷"
    }else if(index<=-100){
        return "中度低迷"
    }else if(index<=0){
        return "轻度低迷"
    }else if(index<=100){
        return "轻度活跃"
    }else if(index<=200){
        return "中度活跃"
    }else if(index<=300){
        return "极度活跃"
    }else {
        return "疯狂"
    }
}

export const addChineseUnitBestTradeRank = (number, decimalDigit) => {

    let absNumber = Math.abs(number)
    // let decimalDigitIndex = Math.floor(absNumber)<100000 ? 2 : 0;
    // if( Math.floor(absNumber)>100000000){
    //     decimalDigitIndex = 2
    // }
    // decimalDigit = decimalDigitIndex ;
    if(number>=0){

        var integer = Math.floor(number);
        var digit =getDigit(integer);
        // ['个', '十', '百', '千', '万', '十万', '百万', '千万'];
        var unit = [];
        if (digit > 3) {
            var multiple = Math.floor(digit / 8);
            if (multiple >= 1) {
                var tmp = Math.round(integer / Math.pow(10, 8 * multiple));
                unit.push(addWan(tmp, number, 8 * multiple, decimalDigit));
                for (var i = 0; i < multiple; i++) {
                    unit.push('亿');
                }
                return unit.join('');
            } else {
                return addWan(integer, number, 0, decimalDigit);
            }
        } else {
            return number;
        }
    }else{
        number = -number
        // let decimalDigitIndex = Math.floor(number)>100000000 ? 2 : 0;
        // decimalDigit = decimalDigit == null ? decimalDigitIndex : decimalDigit;
        var integer = Math.floor(number);
        var digit =getDigit(integer);
        // ['个', '十', '百', '千', '万', '十万', '百万', '千万'];
        var unit = [];
        if (digit > 3) {
            var multiple = Math.floor(digit / 8);
            if (multiple >= 1) {
                var tmp = Math.round(integer / Math.pow(10, 8 * multiple));
                unit.push(addWan(tmp, number, 8 * multiple, decimalDigit));
                for (var i = 0; i < multiple; i++) {
                    unit.push('亿');
                }
                return "-"+unit.join('');
            } else {
                return "-"+addWan(integer, number, 0, decimalDigit);
            }
        } else {
            return "-"+number;
        }
    }

}
export const formatDate = (timestamp,type,now)=> {
    var year=(timestamp.getFullYear()).toString();

    var month=(timestamp.getMonth()+1).toString();
    if(month.length<2){
        month = "0"+month;
    }
    var date=(timestamp.getDate()).toString();
    if(date.length<2){
        date = "0"+date;
    }
    var hour=(timestamp.getHours()).toString();
    if(hour.length<2){
        hour = "0"+hour;
    }
    var minute=(timestamp.getMinutes()).toString();
    if(minute.length<2){
        minute = "0"+minute;
    }
    var second=(timestamp.getSeconds()).toString();
    if(second.length<2){
        second = "0"+second;
    }
    let today = (new Date(now)).getDate().toString()
    let yesterday = (new Date(now-86400000)).getDate().toString()
    let theDayBeforeYesterday = (new Date(now-172800000)).getDate().toString()
    if(today.length<2){
        today = "0"+today;
    }
    if(yesterday.length<2){
        yesterday = "0"+yesterday;
    }
    if(theDayBeforeYesterday.length<2){
        theDayBeforeYesterday = "0"+theDayBeforeYesterday;
    }

    if(type=="F"){
        return month+"月"+date+"号"
    }

    if(type=="D"){
        return year+"-"+month+"-"+date
    }
    if(type=="B"){
        let dayStr = date+"号"
        if(date==today&&now-timestamp<3*86400000){
            dayStr="今天"
            return dayStr+" "+hour+"点"
        }else if (date==yesterday&&now-timestamp<3*86400000){
            dayStr="昨天"
            return dayStr+" "+hour+"点"
        }else if (date==theDayBeforeYesterday&&now-timestamp<3*86400000){
            dayStr="前天"
            return dayStr+" "+hour+"点"
        }else{
            return dayStr+" "+hour+"点"
        }
    }

    if(type=="E"){
        let dayStr = month+"月"+date+"号"
        if(date==today&&now-timestamp<3*86400000){
            dayStr="今天"
            return dayStr+" "+hour+":"+minute
        }else if (date==yesterday&&now-timestamp<3*86400000){
            dayStr="昨天"
            return dayStr+" "+hour+":"+minute
        }else if (date==theDayBeforeYesterday&&now-timestamp<3*86400000){
            dayStr="前天"
            return dayStr+" "+hour+":"+minute
        }else{
            return dayStr+" "+hour+":"+minute
        }
    }
    if(type=="A") {
        let dayStr = date + "号"
        if (date == today && now - timestamp < 3 * 86400000) {
            dayStr = "今天"
            return dayStr + " " + hour + ":" + minute + ":" + second
        } else if (date == yesterday && now - timestamp < 3 * 86400000) {
            dayStr = "昨天"
            return dayStr + " " + hour + ":" + minute + ":" + second
        } else if (date == theDayBeforeYesterday && now - timestamp < 3 * 86400000) {
            dayStr = "前天"
            return dayStr + " " + hour + ":" + minute + ":" + second
        } else {
            return dayStr + " " + hour + ":" + minute + ":" + second
        }
    }
    if(type=="G") {
        let dayStr = date + "号"
        if (date == today && now - timestamp < 3 * 86400000) {
            dayStr = "今天"
            return dayStr + " " + hour + ":" + minute
        } else if (date == yesterday && now - timestamp < 3 * 86400000) {
            dayStr = "昨天"
            return dayStr + " " + hour + ":" + minute
        } else if (date == theDayBeforeYesterday && now - timestamp < 3 * 86400000) {
            dayStr = "前天"
            return dayStr + " " + hour + ":" + minute
        } else {
            return month+"月"+date+"号"
        }
    }
    if(type=="C"){
        return year+"-"+month+"-"+date+" "+hour+":"+minute+":"+second
    }
    if(type=="H"){
        return year+"-"+month+"-"+date
    }
    if(type=="L"){
        return date + "号"+" "+hour+":"+minute+":"+second
    }
    if(type=="M"){
        return hour+":"+minute
    }
    if(type=="N"){
        return minute+":"+second
    }
}
export const getTodayTs = (timestamp) => {
    var year=(timestamp.getFullYear()).toString();

    var month=(timestamp.getMonth()+1).toString();
    if(month.length<2){
        month = "0"+month;
    }
    var date=(timestamp.getDate()).toString();
    if(date.length<2){
        date = "0"+date;
    }
    var date = new Date(year+"/"+month+"/"+date+" "+"00:00")
    console.error(year+"-"+month+"-"+date)
    var ts = Date.parse(date);
    return ts
}

export const addChineseUnitWithSymbol = (number, decimalDigit) => {

    let absNumber = Math.abs(number)
    let decimalDigitIndex = Math.floor(absNumber)<100000 ? 2 : 0;
    if( Math.floor(absNumber)>100000000){
        decimalDigitIndex = 2
    }
    decimalDigit = decimalDigitIndex ;
    if(number>=0){

        var integer = Math.floor(number);
        var digit =getDigit(integer);
        // ['个', '十', '百', '千', '万', '十万', '百万', '千万'];
        var unit = [];
        if (digit > 3) {
            var multiple = Math.floor(digit / 8);
            if (multiple >= 1) {
                var tmp = Math.round(integer / Math.pow(10, 8 * multiple));
                unit.push(addWan(tmp, number, 8 * multiple, decimalDigit));
                for (var i = 0; i < multiple; i++) {
                    unit.push('亿');
                }
                return "+"+unit.join('');
            } else {
                return "+"+addWan(integer, number, 0, decimalDigit);
            }
        } else {
            return "+"+number;
        }
    }else{
        number = -number
        // let decimalDigitIndex = Math.floor(number)>100000000 ? 2 : 0;
        // decimalDigit = decimalDigit == null ? decimalDigitIndex : decimalDigit;
        var integer = Math.floor(number);
        var digit =getDigit(integer);
        // ['个', '十', '百', '千', '万', '十万', '百万', '千万'];
        var unit = [];
        if (digit > 3) {
            var multiple = Math.floor(digit / 8);
            if (multiple >= 1) {
                var tmp = Math.round(integer / Math.pow(10, 8 * multiple));
                unit.push(addWan(tmp, number, 8 * multiple, decimalDigit));
                for (var i = 0; i < multiple; i++) {
                    unit.push('亿');
                }
                return "-"+unit.join('');
            } else {
                return "-"+addWan(integer, number, 0, decimalDigit);
            }
        } else {
            return "-"+number;
        }
    }

}

export const addChineseUnit = (number, decimalDigit) => {

    let absNumber = Math.abs(number)
    let decimalDigitIndex = Math.floor(absNumber)<100000 ? 2 : 0;
    if( Math.floor(absNumber)>100000000){
        decimalDigitIndex = 2
    }
    decimalDigit = decimalDigitIndex ;
    if(number>=0){

        var integer = Math.floor(number);
        var digit =getDigit(integer);
        // ['个', '十', '百', '千', '万', '十万', '百万', '千万'];
        var unit = [];
        if (digit > 3) {
            var multiple = Math.floor(digit / 8);
            if (multiple >= 1) {
                var tmp = Math.round(integer / Math.pow(10, 8 * multiple));
                unit.push(addWan(tmp, number, 8 * multiple, decimalDigit));
                for (var i = 0; i < multiple; i++) {
                    unit.push('亿');
                }
                return unit.join('');
            } else {
                return addWan(integer, number, 0, decimalDigit);
            }
        } else {
            return number;
        }
    }else{
        number = -number
        // let decimalDigitIndex = Math.floor(number)>100000000 ? 2 : 0;
        // decimalDigit = decimalDigit == null ? decimalDigitIndex : decimalDigit;
        var integer = Math.floor(number);
        var digit =getDigit(integer);
        // ['个', '十', '百', '千', '万', '十万', '百万', '千万'];
        var unit = [];
        if (digit > 3) {
            var multiple = Math.floor(digit / 8);
            if (multiple >= 1) {
                var tmp = Math.round(integer / Math.pow(10, 8 * multiple));
                unit.push(addWan(tmp, number, 8 * multiple, decimalDigit));
                for (var i = 0; i < multiple; i++) {
                    unit.push('亿');
                }
                return "-"+unit.join('');
            } else {
                return "-"+addWan(integer, number, 0, decimalDigit);
            }
        } else {
            return "-"+number;
        }
    }

}
export const getPercentStr=(num, total) => {
    if (total == 0) {
        return 0
    } else {
        if (num > 0) {
            return "+" + (Math.round(num / total * 10000) / 100.00).toFixed(2)+"%";// 小数点后两位百分比
        }
        return (Math.round(num / total * 10000) / 100.00).toFixed(2)+"%";// 小数点后两位百分比
    }
}


export const getPercentNum=(num, total) => {
    if(total ==0){
        return 0
    }else{
        return Math.round(num / total * 10000) / 100.00;// 小数点后两位百分比
    }

}

export const getPercentNumT=(num, total) => {
    if(total ==0){
        return 0
    }else{
        return Math.round(num / total * 1000000) / 10000.00;// 小数点后两位百分比
    }

}

export const getPlusAndLessNumber =(number,precision)=>{
    let numberStr = ""
    if(number>0){
        numberStr = "+"+number.toFixed(precision)
    }else{
        numberStr = number.toFixed(precision)
    }
    return numberStr
}
//(now - past) / past
export const getPercent=(num, total) =>{
    if(total ==0){
        return "0%"
    }else {
        return addZero(Math.round(num / total * 10000) / 100.00) + "%";// 小数点后两位百分比
    }


}

export const getPercentWithSymbol=(num, total) =>{
    if(total ==0){
        return "0%"
    }else {
        if((Math.round(num / total * 10000) / 100.00)>0){
            return "+"+addZero(Math.round(num / total * 10000) / 100.00) + "%";// 小数点后两位百分比
        }
        return addZero(Math.round(num / total * 10000) / 100.00) + "%";// 小数点后两位百分比
    }


}

export const timeTurnIntoWord=(time) =>{
     if(time<60){
         return time+"秒"
     }else if (time<3600){
         return parseInt(time/60)+"分"+time%60+"秒"
     }else{
         let minTime = time%3600
         return parseInt(time/3600)+"小时"+parseInt(minTime/60)+"分"+minTime%60+"秒"
     }
}

export const getIntPercent=(num, total) =>{
    if(total ==0){
        return "0%"
    }else {
        return  parseInt(Math.round(num / total * 10000) /  100.00) + "%";// 小数点后两位百分比
    }


}

export const addZero = (value) => {

    var value = Math.round(parseFloat(value) * 100) / 100;
    var xsd = value.toString().split(".");
    if (xsd.length == 1) {
        value = value.toString() + ".00";
        return value;
    }
    if (xsd.length > 1) {
        if (xsd[1].length < 2) {
            value = value.toString() + "0";
        }
        return value;
    }
}
export const sortNumber = (a, b) => {
    return parseFloat(b.rate) - parseFloat(a.rate);
}

/**
 * 用touch事件模拟点击、左滑、右滑、上拉、下拉等时间，
 * 是利用touchstart和touchend两个事件发生的位置来确定是什么操作。
 * 例如：
 * 1、touchstart和touchend两个事件的位置基本一致，也就是没发生位移，那么可以确定用户是想点击按钮等。
 * 2、touchend在touchstart正左侧，说明用户是向左滑动的。
 * 利用上面的原理，可以模拟移动端的各类事件。
 **/
export const EventUtil = (function() {

    //支持事件列表
    let eventArr = ['eventswipeleft', 'eventswiperight', 'eventslideup', 'eventslidedown', 'eventclick', 'eventlongpress'];

    //touchstart事件，delta记录开始触摸位置
    function touchStart(event) {
        this.delta = {};
        this.delta.x = event.touches[0].pageX;
        this.delta.y = event.touches[0].pageY;
        this.delta.time = new Date().getTime();
    }

    /**
     * touchend事件，计算两个事件之间的位移量
     * 1、如果位移量很小或没有位移，看做点击事件
     * 2、如果位移量较大，x大于y，可以看做平移，x>0,向右滑，反之向左滑。
     * 3、如果位移量较大，x小于y，看做上下移动，y>0,向下滑，反之向上滑
     * 这样就模拟的移动端几个常见的时间。
     * */
    function touchEnd(event) {
        let delta = this.delta;
        delete this.delta;
        let timegap = new Date().getTime() - delta.time;
        delta.x -= event.changedTouches[0].pageX;
        delta.y -= event.changedTouches[0].pageY;
        if (Math.abs(delta.x) < 5 && Math.abs(delta.y) < 5) {
            if (timegap < 1000) {
                if (this['eventclick']) {
                    this['eventclick'].map(function(fn){
                        fn(event);
                    });
                }
            } else {
                if (this['eventlongpress']) {
                    this['eventlongpress'].map(function(fn){
                        fn(event);
                    });
                }
            }
            return;
        }
        if (Math.abs(delta.x) > Math.abs(delta.y)) {
            if (delta.x > 0) {
                if (this['eventswipeleft']) {
                    this['eventswipeleft'].map(function(fn){
                        fn(event);
                    });
                }
            } else {
                this['eventswiperight'].map(function(fn){
                    fn(event);
                });
            }
        } else {
            if (delta.y > 0) {
                if (this['eventslidedown']) {
                    this['eventslidedown'].map(function(fn){
                        fn(event);
                    });
                }
            } else {
                this['eventslideup'].map(function(fn){
                    fn(event);
                });
            }
        }
    }

    function bindEvent(dom, type, callback) {
        if (!dom) {
            console.error('dom is null or undefined');
        }
        let flag  = eventArr.some(key => dom[key]);
        if (!flag) {
            dom.addEventListener('touchstart', touchStart);
            dom.addEventListener('touchend', touchEnd);
        }
        if (!dom['event' + type]) {
            dom['event' + type] = [];
        }
        dom['event' + type].push(callback);
    }

    function removeEvent(dom, type, callback) {
        if (dom['event' + type]) {
            for(let i = 0; i < dom['event' + type].length; i++) {
                if (dom['event' + type][i] === callback) {
                    dom['event' + type].splice(i, 1);
                    i--;
                }
            }
            if (dom['event' + type] && dom['event' + type].length === 0) {
                delete dom['event' + type];
                let flag  = eventArr.every(key => !dom[key]);
                if (flag) {
                    dom.removeEventListener('touchstart', touchStart);
                    dom.removeEventListener('touchend', touchEnd);
                }
            }
        }
    }
    return {
        bindEvent,
        removeEvent
    }
})();

