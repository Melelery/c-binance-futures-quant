import Modal from 'antd/es/Modal';
import Upload from 'antd/es/Upload';
import message from 'antd/es/message';
import React from "react";
import './aliyunOSSUpload.css';
import {generateMixed} from "../constants/commonFunction";
import {UploadOutlined} from '@ant-design/icons';
class AliyunOSSUpload extends React.Component {
    state = {
        OSSData: {},
        previewVisible: false,
        previewImage: '',
        fileList:[]
    };

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
        const filename = generateMixed(20)+suffix;
        file.url = OSSData.dir + filename;
        return file;
    };

    getExtraData = file => {
        const { OSSData } = this.state;
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
    handlePreview = async file => {
        if (!file.url && !file.preview) {
            file.preview = await getBase64(file.originFileObj);
        }
        this.setState({
            previewImage: "https://yuntuimao.oss-cn-shenzhen.aliyuncs.com/"+(file.url || file.preview),
            previewVisible: true,
        });
    };
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
            // onPreview:this.handlePreview,
            beforeUpload: this.beforeUpload,
            accept:"image/*"
        };
        return (
            <div style={{paddingTop:16,width:"90%",textAlign:"center",alignItems:"center",justifyContent: "center",display: "flex",flexDirection:"column"}}>
                <Upload {...props}>
                    {fileList.length >= 9 ? null : <div style={{marginLeft:"5%",width:"90%"}}><UploadOutlined />
                        上传图片
                    </div>}
                </Upload>
                {fileList.length >= 1 ?<a onClick={()=>{this.props.changeFileList([]);this.setState({fileList:[]})}} style={{marginTop:8,marginBottom:8}}>
                    清除所有上传图片
                </a>:null}
                <Modal visible={previewVisible} footer={null} onCancel={this.handleCancel}>
                    <img alt="example" style={{ width: '100%' }} src={previewImage} />
                </Modal>
            </div>
        );
    }
}

export default (AliyunOSSUpload);
