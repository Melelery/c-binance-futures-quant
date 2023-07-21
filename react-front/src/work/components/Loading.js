import React  from 'react';
import { Spin,Upload,InputNumber,Radio,Slider,Tag,Input,Pagination,Collapse,Avatar,message,Select,Modal,Checkbox,Alert,Switch } from 'antd';
import { LoadingOutlined } from '@ant-design/icons';
class Loading extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div style={{width:"100%",display: "flex",flexDirection:"column",alignItems:"center", justifyContent: "center",textAlign:"center"}}>
                <div>
                    <Spin style={{fontSize:36}} />
                </div>
                <div style={{marginTop:16}}>
                    <strong>加载中</strong>
                </div>
            </div>
        )

    }
}
export default Loading;
