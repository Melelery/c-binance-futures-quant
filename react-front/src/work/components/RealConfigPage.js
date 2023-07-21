import React from 'react';
import {
    CloseOutlined,
    EditOutlined, ToolOutlined
} from '@ant-design/icons';
import {
    Button,
    Upload,
    InputNumber,
    Radio,
    Slider,
    Tag,
    Input,
    Pagination,
    Collapse,
    Avatar,
    message,
    Select,
    Modal,
    Checkbox,
    Alert,
    Switch,
    Table
} from 'antd';
import {coinArr,coinChineseObj} from "../constants/coinType";
import {connect} from "react-redux";
import * as action from "../actions";
import {bindActionCreators} from "redux";
import {keyboardObj, realHotKeyConfigDefaultObj,keyboardFunArr,sortTypeObj} from '../constants/hotKey'
import {deepCopy} from '../constants/commonFunction'
import HotKeyModal from "./HotKeyModal";
import {CopyToClipboard} from "react-copy-to-clipboard";
const { Option } = Select;
const { TextArea } = Input;
const { Panel } = Collapse;
const darkWordColor="#8c8c8c"
import {publicServerURL} from "../constants/serverURL";

const apiColumns = [
    {
        title: 'API KEY',
        dataIndex: 'apiKey',
        key: 'apiKey',
    },
    {
        title: '备注',
        dataIndex: 'describe',
        key: 'describe'
    },
    // {
    //     title: '删除',
    //     dataIndex: 'deleteButton',
    //     key: 'deleteButton'
    // }
];

class RealConfigPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            newBinanceApiKey:"",
            newBinanceApiSecret:"",
            newBinanceApiDescribe:"",
            hotKeyConfigModalVisible:""
        };
    }

    componentDidMount = () => {

    }

    getInputNameAndValueContent = (name,value,extraValueA,extraValueB,allWidth,nameWidth,marginTop)=>{
        let valueWidth = allWidth - nameWidth
        return (

            <div style={{alignItems: "center",display: "flex",flexDirection: "row",width:allWidth,marginTop:marginTop}}>
                <div style={{width:nameWidth}}>
                    {name}
                </div>
                <div style={{width:valueWidth}}>
                    {
                        value
                    }
                    {
                        extraValueA
                    }
                    {
                        extraValueB
                    }
                </div>
            </div>
        )
    }




    addApi = ()=>{
        const {userInfo} = this.props

        const {page,newBinanceApiKey,newBinanceApiSecret,newBinanceApiDescribe} = this.state;
        if(newBinanceApiKey.length<10||newBinanceApiSecret.length<10){
            console.error(newBinanceApiKey)
            console.error(newBinanceApiSecret)
            message.error("请输入API KEY 和API SECRET")
            return
        }
        if(newBinanceApiDescribe.length<1||newBinanceApiDescribe.length>6){
            message.error("备注需1~6字符")
            return
        }
        let formData = new FormData();
        formData.append("accessToken",userInfo["accessToken"]);
        formData.append("apiKey",newBinanceApiKey);
        formData.append("apiSecret",newBinanceApiSecret);
        formData.append("apiDescribe",newBinanceApiDescribe);
        fetch(publicServerURL+"/add_api", {
            method:'POST',
            body:formData
        }).then((response)=>{
            if (response.ok) {
                return response.json();
            }
        }).then((response)=>{
            if(response['s']=="error"){
                message.error("绑定失败，请确认您已经开通合约交易权限且填写无误")
            }else{
                this.props.changeUserInfo({
                    ...userInfo,
                    binanceApiArr:response['binanceApiArr']
                })
                this.setState({
                    "newBinanceApiKey":"",
                    "newBinanceApiSecret":"",
                    "newBinanceApiDescribe":""
                })
                message.success("绑定成功")
            }
        }).catch((error)=>{
            console.error(error)
        });
    }

    deleteApi = (apiKey)=>{
        const {userInfo} = this.props

        let formData = new FormData();
        formData.append("accessToken",userInfo["accessToken"]);
        formData.append("apiKey",apiKey);
        fetch(publicServerURL+"/delete_api", {
            method:'POST',
            body:formData
        }).then((response)=>{
            if (response.ok) {
                return response.json();
            }
        }).then((response)=>{
            if(response['s']=="error"){
                message.error("删除失败，请稍后再试")
            }else{
                this.props.changeUserInfo({
                    ...userInfo,
                    binanceApiArr:response['binanceApiArr']
                })

                message.success("删除成功")
            }
        }).catch((error)=>{
            console.error(error)
        });
    }

    onChangeBinanceApiSecret= (e)=>{
        let value = e.target.value
        this.setState({
            newBinanceApiSecret:value
        })
    }

    onChangeBinanceApiKey = (e)=>{
        let value = e.target.value
        this.setState({
            newBinanceApiKey:value
        })
    }

    onChangeBinanceApiDescribe = (e)=>{
        let value = e.target.value
        this.setState({
            newBinanceApiDescribe:value
        })

    }


    getBinanceServerContent = ()=>{
        const {userInfo} = this.props
        if(JSON.stringify(userInfo["serverInfoObj"])=="{}"){
            return <CopyToClipboard text={"frozen_quant"} onCopy={() => {message.success("复制成功")}}><div style={{display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignItems: "center",width:1000,marginTop:64}}>

                系统没有检测到您的交易服务器。<br/><br/>
                如果您是第一次注册使用，请先添加客服微信 frozen_quant （点击复制） 。<br/><br/>
                充值最低15USD后体验。<br/><br/>
                详细收费规则请查阅下方手续费栏目。<br/><br/>


            </div></CopyToClipboard>
        }
    }

    getBinanceApiContent = ()=>{
        const {page,newBinanceApiKey,newBinanceApiSecret,newBinanceApiDescribe} = this.state;
        const {userInfo} = this.props;

        let apiTableData = []
        userInfo["binanceApiArr"].map((item,i)=>{
            apiTableData.push({
                "apiKey":item["apiKey"].substr(0,10)+'********************'+item["apiKey"].substr(50),
                "describe":item["apiDescribe"],
                "deleteButton":<span onClick={()=>{this.deleteApi(item["apiKey"])}}>删除</span>
            })
        })
        if(JSON.stringify(userInfo["serverInfoObj"])!="{}"&&userInfo["binanceApiArr"].length<=0){
            return <div style={{                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignItems: "center",width:1000}}>
                {this.getInputNameAndValueContent("币安API KEY",
                    <Input style={{width: "100%"}} value={newBinanceApiKey} onChange={this.onChangeBinanceApiKey}/>,"","",
                    1000, 250,32)}
                {this.getInputNameAndValueContent("币安API SECRET",
                    <Input style={{width: "100%"}} value={newBinanceApiSecret} onChange={this.onChangeBinanceApiSecret}/>,"","",
                    1000, 250,32)}
                {this.getInputNameAndValueContent("备注（1~3字），将在下方显示",
                    <Input style={{width: "100%"}} value={newBinanceApiDescribe} onChange={this.onChangeBinanceApiDescribe}/>,"","",
                    1000, 250,32)}
                <div style={{marginTop:48,width:1000}}>

                    <div style={{display: "flex",flexDirection: "row",alignItems: "center"}}>
                        <strong>*建议您API绑定您两个独立服务器地址以提高安全性(需同时绑定)：</strong>

                        <CopyToClipboard text={userInfo["serverInfoObj"]["serverAPublicIP"]} onCopy={() => {message.success("复制地址成功")}}>
                            <div style={{textDecoration:"underline",marginLeft:16}}>
                                {userInfo["serverInfoObj"]["serverAPublicIP"]}
                            </div>
                        </CopyToClipboard>

                        <CopyToClipboard text={userInfo["serverInfoObj"]["serverBPublicIP"]} onCopy={() => {message.success("复制地址成功")}}>
                            <div style={{textDecoration:"underline",marginLeft:16}}>
                                {userInfo["serverInfoObj"]["serverBPublicIP"]}
                            </div>
                        </CopyToClipboard>
                    </div>
                    <div style={{marginTop:32}}>
                        <strong>*请确保开启U本位合约交易和查询权限</strong>
                    </div>
                    <div style={{marginTop:32}}>
                        <strong>*如需BNB小额自动购买划转抵扣手续费，需开启万向划转和现货交易权限<br/><br/></strong>
                    </div>
                </div>

                <Button onClick={()=>{this.addApi()}} type={"primary"} style={{marginTop:32,width:400}}>绑定一个API KEY来开启交易</Button>
            </div>

        }else if(userInfo["binanceApiArr"].length>0){
            return <div style={{width:1000}}>
                {this.getInputNameAndValueContent("币安API KEY",
                    <Input style={{width: "100%"}} value={newBinanceApiKey} onChange={this.onChangeBinanceApiKey}/>,"","",
                    1000, 250,32)}
                {this.getInputNameAndValueContent("币安API SECRET",
                    <Input style={{width: "100%"}} value={newBinanceApiSecret} onChange={this.onChangeBinanceApiSecret}/>,"","",
                    1000, 250,32)}
                {this.getInputNameAndValueContent("备注（1~3字），将在下方显示",
                    <Input style={{width: "100%"}} value={newBinanceApiDescribe} onChange={this.onChangeBinanceApiDescribe}/>,"","",
                    1000, 250,32)}
                <Button onClick={()=>{this.addApi()}} style={{marginTop:32,width:1000}}>继续添加其他账号同时交易</Button>
                <div style={{marginTop:32}}>
                    <Table dataSource={apiTableData} columns={apiColumns}
                           pagination={false}/>
                </div>

            </div>

        }
    }


    render() {
        const {userInfo}=this.props;
        return <div style={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            color: darkWordColor,
            minHeight: document.body.clientHeight,
            backgroundColor: "#f0f0f0",
            width: "100%",
            height: "100%",
            padding: 32
        }}>
            <HotKeyModal hotKeyConfigModalVisible={this.state.hotKeyConfigModalVisible} cancelHotKeyConfigModal={() => {
                this.setState({hotKeyConfigModalVisible: false})
            }}/>

            {this.getBinanceApiContent()}
            {this.getBinanceServerContent()}


            {/*{userInfo["binanceApiArr"].length > 0 && <div onClick={() => {*/}
            {/*    this.setState({hotKeyConfigModalVisible: true})*/}
            {/*}} style={{marginTop: 32, fontSize: 16, marginLeft: 32}}>*/}
            {/*    操作快捷键配置：<ToolOutlined/>*/}
            {/*</div>}*/}
            {userInfo["binanceApiArr"].length > 0 &&
                <Button style={{marginTop: 128, width: 1000}} type={"primary"} onClick={() => {
                    this.props.goToTrade()}
                }>进入最交易-币安合约交易系统</Button>}


            <div style={{width: 1000, marginTop: 32, paddingBottom: 64, color: "black"}}>
                <Collapse accordion>
                    <Panel header="使用建议（重要且必读）" key="0">
                        下面的每一行文字都非常重要，交易是一项直接直接关联到您资产的事情，使用本系统前，我们强烈要求您务必仔细阅读，并且理解以下文字，遇到有问题的，及时向客服咨询之后再进行实操。<br/><br/>
                        <strong>1.交易风险警告</strong><br/><br/>
                        交易是一项直接关联到您资产的事情，使用最交易工具不代表您能够稳定盈利，由于潜在BUG，服务器，币安等不稳定性，我们也不能保证您从这里发出的订单能够100%满足您的意向需求。<br/><br/>
                        尤其是在全市场极端行情，剧烈波动的时候，本系统技术使用的服务器与币安服务器之间可能存在巨大延迟/不可下单/止损失败等等意外风险，当然此时币安的网页和app亦会存在此类问题，根据一年来实际测试，通常该类风险时间不会超过万分之一，但我们仍需要您明白并理解。<br/><br/>
                        我们强烈建议您保持其他币安渠道(APP,WEB)登录，并且在紧急情况下通过官网进行避险平仓操作。<br/><br/>
                        <strong>2.账户设置要求和建议</strong><br/><br/>
                        我们强烈建议您使用币安子账户功能，仅使用子账户API进行操作。<br/><br/>
                        出于开发效率的考量，我们不会识别您的订单来源，使用期间所有账号成交量都会录入系统，录入系统的所有的成交量都会收取相应最交易手续费（详见下方）。<br/><br/>
                        使用子账户，将最交易的交易和资产和您的主要资产和其他交易进行隔离，是最有效的解决方案，同时可以防止极端情况的风险。<br/><br/>
                       使用的账户，其币安U本位合约，必需设置为全仓模式<br/><br/>
                        我们建议开启混合保证金模式，混合保证金模式下，您可以持有USDT，BNB，交易BUSD合约，或者持有BNB，BUSD，交易USDT合约<br/><br/>
                        <strong>3.网络风险警告</strong><br/><br/>
                        交易页面左下方，标明了您现在和最比特服务器群之间的联系是否正常<br/><br/>
                        我们强烈建议您在该图标为红色叉，且显示网络错误的时候，刷新页面<br/><br/>
                        如问题还是存在，停止使用该系统进行交易并联系客服处理，如有未平仓订单及时登录币安官方网站或者APP进行处理<br/><br/>
                        我们为您建立的服务器群位于中国香港，购买前我们强烈建议您通过直播页面判断服务器延迟是否可以接受<br/><br/>
                        <strong>4.API风险警告</strong><br/><br/>
                        我们采用和币安，欧意一致的API管理方案，API仅会在您首次录入的时候进行网络传输，且服务器安全架构和欧意服务器安全架构一致，但我们无法保证100%的安全<br/><br/>
                        现实可能会发生任何风险，区块链世界更是如此，面对风险最好的方式并不是恐惧，而是隔离，所以我们强烈建议您仅在子账户，或者专门用一个账号存放交易资产连接最交易<br/><br/>
                        如果以上条件都不具备，我们强烈建议您仅开启合约交易权限，不要使用BNB自动购买功能（需开启万向转账和现货交易权限）<br/><br/>
                        产品已经自用一年，并无发生任何风险事件，但是我们还是要请求您注意风险防范<br/><br/>
                        请注意，我们产品利润微薄，大部分开发成本都回收不了，如您发生被盗事件，我们不会进行任何赔付<br/><br/>
                        <strong>5.API交易规则风险</strong><br/><br/>
                        币安对每个账户的交易频率，成家率等等都有限制，该交易系统并无法也无可能突破这个限制，所以请您在规则内使用<br/><br/>
                        下单限制为10秒100单<br/><br/>
                        该限制并非针对最交易用户，包括您在币安网页，APP交易同样受此规则限制<br/><br/>
                        正常情况下很难触及，但不排除您过度使用导致触发币安的风控，触发后账户开仓功能会被停止一段时间<br/><br/>
                        我们特别建议您对于批量开，关及止盈止损的设置，最好不要超过5（系统最高设置为10）<br/><br/>
                        <a href={"https://www.binance.com/zh-CN/futures/trading-rules/perpetual"} target="_blank">点击此处阅读币安交易规则</a><br/><br/>
                            <strong>6.延迟及其他使用注意事项</strong><br/><br/>
                        每个账号都是绑定三个独立服务器，以实现最低程度的延迟，该系统极度依赖本地端，且极度依赖交易员，我们不建议您在人离开的时候信任程序的执行，不建议您一个账号同时打开多个页面，每次使用请仅保持一个浏览器，一个页面进行（直播页面不影响）。<br/><br/>
                        目前已知K线图，相对于官网存在一定延迟（1秒以下），我们的设计方案是对于最上方，选择币种的K线图，我们进行了特殊化处理，使其延迟甚至能够略低于官网和APP（大部分时间），所以请尽量以最上方选择币种的K线数据为准，直播页面该处不做优化。<br/><br/>
                        深度图的延迟为250毫秒，订单，仓位的延迟，也应该略低余官网和APP。<br/><br/>
                        统计数据的延迟为1~30秒。<br/><br/>
                    </Panel>
                    <Panel header="基础操作" key="1">
                        进去后页面大部分为快捷键操作(使用前务必确认电脑目前为英文输入)<br/><br/>
                        所有快捷键均可通过按键配置自行更换<br/><br/>
                        具体快捷键设置和详细说明请在交易页面点击右下角图标浏览<br/><br/>
                    </Panel>

                    <Panel header="手续费" key="2">
                        出于开发效率的考量，使用期间所有账号成交量都会录入系统，录入系统的所有的成交量都会收取相应最交易手续费，建议使用子账户来隔离交易和资产，避免错误识别。<br/><br/>
                        如该交易对的手续费率为正值，最交易手续费固定为您支付的币安usdt合约手续费的10%，<strong>（不计算任何形式的返佣，仅计算币安实时收取的手续费用）</strong>。<br/><br/>
                        如该交易对的手续费率为负值，则固定为币安支付给您的手续费的5%。<br/><br/>
                        我们对每个用户都配置三台独立的服务器，确保您拥有最优的交易体验。<br/><br/>
                        因此每个用户每三十天都有最低消费限额（15 USD），以确保我们的基本服务器费用能得到回收。<br/><br/>
                        用户每次充值最低为15 USDT，当用户余额为负数或者不满足下一个三十天最低消费时，服务器会被释放，需要联系客服重新开通<br/><br/>
                    </Panel>
                    <Panel header="免责条约" key="3">
                        我们为每个用户配置了三台独立的阿里云服务器，且该系统已经有接近一年的自用成熟度，我们相信这是目前业界能够提供的可靠性最强的方案<br/><br/>
                        但任何服务都是具备风险的，我们仅提供软件服务且利润微薄<br/><br/>
                        我们明白无论可用性在99.99...%增加多少个9，对于交易都是毁灭性的<br/><br/>
                        但我们无法向您保证或赔付，任何网络或者是其他问题造成的损失<br/><br/>
                        我们强烈建议您在币安官方网页或者app保持登录状态，在极端情况服务不可用的时候，尝试使用币安官网或者APP进行避险交易<br/><br/>
                    </Panel>
                    <Panel header="其他问题" key="4">
                        <Collapse accordion>
                            <Panel header="浏览器卡顿" key="1">
                                由于系统非常复杂且有非常多的计算和缓存在本地端完成，以达到千人千面的设计，所以该系统对电脑内存要求较高，最低要求8G内存
                            </Panel>
                            <Panel header="为何不适用tradingview" key="2">
                                性能原因，范币种展示如果采用tradingview将会卡死，解决方案是对于您需要详细查阅的交易对，通过选择币种->按o，打开币安交易网页查看
                            </Panel>
                        </Collapse>
                    </Panel>
                </Collapse>


            </div>

        </div>

    }
}
const mapStateToProps = (state) => {
    return ({
        userInfo:state.userInfo,
    });
};
const mapDispatchToProps  = (dispatch, ownProps) => {
    return bindActionCreators({
        updateIfUpdateChatModalView:action.updateIfUpdateChatModalView,
        updateChat:action.updateChat,
        changeUserInfo:action.changeUserInfo
    }, dispatch);
};
export default connect(mapStateToProps,mapDispatchToProps)(RealConfigPage);
