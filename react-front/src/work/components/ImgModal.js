import React  from 'react';
import { Button,InputNumber,Radio,Slider,Tag,Input,Pagination,Collapse,Avatar,message,Select,Modal,Checkbox,Alert,Switch } from 'antd';
import {PlusCircleFilled,MinusCircleFilled,SearchOutlined} from "@ant-design/icons"

class ImgModal extends React.Component {
    constructor(props) {
        super(props);
        let imgWidth = document.body.clientWidth*0.85
        this.state = {
            imgWidth:imgWidth
        }
    }
    getImgModalView = ()=>{
        return <div >
            <img width={this.state.imgWidth} src={this.props.imgUrl} />
            <div style={{width:"100%",height:256}}/>
        </div>


    }

    cancel= ()=>{
        const {imgModalCancel} = this.props;
        this.setState({
            imgWidth:document.body.clientWidth*0.85
        })
        imgModalCancel()
    }

    getImgModalFoot = ()=>{
        return(
            <div style={{
                width: "100%",
                backgroundColor:"#000000",
                fontSize: 18,height:48,display: "flex",flexDirection:"row",alignItems:"center", justifyContent: "center"}}>
                <div onClick={()=>{
                    this.setState({imgWidth:this.state.imgWidth*0.8})}} style={{ zIndex:999999,color:"#f1f1f1",width:"25%",textAlign:"center",fontSize:30}}>
                    <MinusCircleFilled />
                </div>
                <div onClick={()=>{
                    this.setState({imgWidth:this.state.imgWidth*1.2})}} style={{ zIndex:999999,color:"#f1f1f1",width:"25%",textAlign:"center",fontSize:30}}>
                    <PlusCircleFilled />
                </div>
                <div onClick={()=>{this.cancel()}} style={{color:"#f1f1f1",width:"50%",textAlign:"center",fontSize:20}}>
                    关闭窗口
                </div>

            </div>
        )
    }
    render() {
        const {imgModalVisible} = this.props;
        return(
            <Modal
                visible={imgModalVisible}
                onCancel={this.cancel}
                style={{zIndex:9999,display:!imgModalVisible&&"none"}}
                closable = {false}
                footer={[
                    this.getImgModalFoot()
                ]}
            >
                <div style={{width:"100%",maxHeight:document.body.clientHeight*0.8,overflowY: "auto"}}>
                    <div className={"top"} style={{display: "flex",flexDirection:"row",alignItems:"center", justifyContent: "center"}}>
                        <div style={{textAlign:"center", height: 36,display: "flex",flexDirection:"row",alignItems:"center", justifyContent: "left"}}>
                            <div style={{marginTop:-6,width:36}}>
                                <Avatar
                                    src={"https://yuntuimao.oss-cn-shenzhen.aliyuncs.com/whiteLogo.png"}
                                    alt="Han Solo"
                                    size={18}
                                />
                            </div>
                            <div style={{marginLeft:8,marginTop:10,height: 36,display: "flex",flexDirection:"column",alignItems:"left", justifyContent: "left", textAlign: "left"}}>
                                <div >
                                    <strong>
                                        <i style={{fontSize:16,color:"#f1f1f1"}}>最</i>
                                        <i style={{fontSize:15,color:"#f1f1f1"}}> 比</i>
                                        <i style={{fontSize:14,color:"#f1f1f1"}}> 特 </i>
                                    </strong>
                                    <span  style={{color:"#f5e7e7",marginLeft:16,fontSize:14}} ><SearchOutlined tyle={{color:"#f5e7e7",marginRight:8}}/><span style={{marginLeft:8}}>www.zuibite.com</span></span>
                                </div>
                            </div>
                        </div>

                    </div>

                    <div style={{marginLeft:"5%",marginTop:16,width:"90%"}}>
                        {this.getImgModalView()}
                    </div>

                </div>
            </Modal>
        )

    }
}
export default ImgModal;
