import React, {Fragment} from 'react';
import {
    Router,
    Route,
    Switch,
    Redirect
} from 'react-router-dom';

import history from '@components/public/history';
import {url_add} from '@config';
import {url_data} from './work/router/data';

class App extends React.Component {
    constructor(props, context) {
        super(props, context);
    }

    render() {
        //auth_arr就是后台维护的一个权限的数组，[1]里面的1，就是有权限的访问的1的界面，这里的权限控制模型，可以自行编写
        const {auth_arr} = this.props;
        let list = (url_data) => url_data.map((data, i) => {
            if (data.children && data.children.length > 0) {
                return (
                    <data.comp key={i}>
                        {list(data.children)}
                    </data.comp>
                );
            }
            if (data.auth) {
                if (auth_arr.find((data_arr) => data_arr == data.auth)) {
                    return (<Route key={i} exact path={url_add + data.url} component={data.comp}/>);
                } else {
                    return null;
                }
            } else {
                return (<Route key={i} exact path={url_add + data.url} component={data.comp}/>);
            }
        });

        return (
            <Router
                history={history}
            >
                <Fragment>
                    {/**
                     * 这里可以公共的样式,比如 头部, 尾部, 等.
                     */
                    }
                    <Switch>
                        {list(url_data)}
                    </Switch>
                </Fragment>
            </Router>
        );
    }
}

export default App;
