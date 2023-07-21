
import { Upload,InputNumber,Radio,Slider,Tag,Input,Pagination,Collapse,Avatar,message,Select,Modal,Checkbox,Alert,Switch } from 'antd';
import React from "react";
import './aliyunOSSUpload.css';
import {connect} from "react-redux";
import {bindActionCreators} from "redux";
import {generateMixed} from "../constants/commonFunction"

class UserAliyunOSSUpload extends React.Component {
    state = {
        OSSData: {},
        previewVisible: false,
        previewImage: '',
        fileList:[]
    };
    componentWillUnmount=()=>{
        console.error("componentWillUnmount")
    }
    async componentDidMount() {
        await this.init();
    }

    init = async () => {
        try {
            await this.mockGetOSSData();
        } catch (error) {
            message.error(error);
        }
    };

    // Mock get OSS api
    // https://help.aliyun.com/document_detail/31988.html
    mockGetOSSData = () => {
        fetch("http://47.75.100.141:9008/", {
            method: 'GET'
        }).then((response) => {
            if (response.ok) {
                return response.json();
            }
        }).then((response) => {
            this.setState({OSSData:{
                    dir: response['dir'],
                    expire: response['expire'],
                    host: response['host'],
                    accessId: response['accessid'],
                    policy: response['policy'],
                    signature: response['signature']
                }});
        })
    };

    onChange = ({ fileList }) => {
        const { onChange } = this.props;
        console.log('Aliyun OSS:', fileList);
        this.props.changeFileList(fileList)
        this.setState({
            fileList:fileList
        })
        if (onChange) {
            onChange([...fileList]);
        }
    };

    onRemove = file => {
        const { value, onChange } = this.props;

        const files = value.filter(v => v.url !== file.url);

        if (onChange) {
            onChange(files);
        }
    };

    transformFile = file => {
        const { OSSData } = this.state;

        const suffix = file.name.slice(file.name.lastIndexOf('.'));
        const filename = "avatar/"+this.props.userInfo.account;
        file.url = OSSData.dir + filename;
        return file;
    };

    getExtraData = file => {
        const { OSSData } = this.state;
        console.info(file)
        const suffix = file.name.slice(file.name.lastIndexOf('.'));
        file.url = OSSData.dir + generateMixed(20)+suffix;
        return {
            key: file.url,
            OSSAccessKeyId: OSSData.accessId,
            policy: OSSData.policy,
            Signature: OSSData.signature,
        };
    };

    beforeUpload = async (file) => {
        const { OSSData } = this.state;
        const expire = OSSData.expire * 1000;

        if (expire < Date.now()) {
            await this.init();
        }

    };
    handleCancel = () => this.setState({ previewVisible: false });

    render() {
        const { value } = this.props;
        const { previewVisible, previewImage, fileList } = this.state;
        const props = {
            listType: 'picture-card',
            action: this.state.OSSData.host,
            onChange: this.onChange,
            transformFile: this.transformFile,
            data: this.getExtraData,
            fileList:fileList,
            className:"avatar-uploader",
            showUploadList:false,
            beforeUpload: this.beforeUpload,
            accept:"image/*"
        };
        return (
            <div style={{width:"100%",textAlign:"center",alignItems:"center",justifyContent: "center",display: "flex",flexDirection:"column"}}>
                <Upload {...props}>
                    {fileList.length >= 1 ? null : <span icon="upload">
                        <div style={{width:document.body.clientWidth*0.8}}>
                            上传图片
                        </div>

                    </span>}
                </Upload>
                {fileList.length >= 1 ?<a onClick={()=>{this.props.changeFileList([]);this.setState({fileList:[]})}} style={{marginTop:8,marginBottom:8}}>
                    重新上传
                </a>:null}
                <Modal visible={previewVisible} footer={null} onCancel={this.handleCancel}>
                    <img alt="example" style={{ width: '100%' }} src={previewImage} />
                </Modal>
            </div>
        );
    }
}
const mapStateToProps = (state) => {
    return ({
        userInfo:state.userInfo,
    });
};
const mapDispatchToProps  = (dispatch, ownProps) => {
    return bindActionCreators({

    }, dispatch);
};
export default connect(mapStateToProps,mapDispatchToProps)(UserAliyunOSSUpload);
