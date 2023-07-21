import React, { Component } from 'react';
import storeConfig from './storeConfig';
import { Provider } from 'react-redux';
import MySwitch from './work/constainers/MySwitch';
// import './App.less
import message from 'antd/es/message';
import 'antd/es/message/style'; // 或者 antd/es/button/style/css 加载 css 文件
require('core-js');
const store = storeConfig();
import 'antd/es/Timeline/style/index.less';
import 'antd/es/Button/style/index.less';
import 'antd/es/Modal/style/index.less';
import 'antd/es/Alert/style/index.less';
import 'antd/es/Input/style/index.less';
import 'antd/es/Collapse/style/index.less';
import 'antd/es/Spin/style/index.less';
import 'antd/es/message/style/index.less';
import 'antd/es/Switch/style/index.less';
import 'antd/es/Checkbox/style/index.less';
import 'antd/es/Upload/style/index.less';
import 'antd/es/Select/style/index.less';
import 'antd/es/Tag/style/index.less';
import 'antd/es/Slider/style/index.less';
import 'antd/es/input-number/style/index.less';
import 'antd/es/Radio/style/index.less';
import 'antd/es/Badge/style/index.less';
import 'antd/es/Avatar/style/index.less';
import 'antd/es/Divider/style/index.less';
import 'antd/es/Pagination/style/index.less';
import 'antd/es/Progress/style/index.less';
import 'antd/es/Card/style/index.less';
import 'antd/es/date-picker/style/index.less';
import 'antd/es/table/style/index.less';
class App extends Component {
    state = {
        Option:"Lucy"
    }

    componentDidCatch(error, info) {

        message.error(error.toString())
        message.error("APP 崩溃，正在自动重启")
        if(process.env.NODE_ENV!="development"){
            window.location.href="#"
            setTimeout(location.reload(),200);
        }
    }


    render() {
        return (
            <Provider store={store}>
                <MySwitch/>
            </Provider>
        );
    }
}
export default App;
