import React, { Component} from 'react';
import './Switch.css';
import {bindActionCreators} from "redux";
import {connect} from "react-redux";
import { Switch, Route,Router} from 'react-router-dom'
import Show from './Show'

import history from './History';

class MySwitch extends Component {

    state = {
    }




    constructor(props) {
        super(props);

    }

    componentDidMount() {

    }

    render() {

        return (
            <Router  history={history}>
                <Switch >
                    <Route exact path="/" component={Show}/>
                </Switch>
            </Router>

        );
    }
}
const mapStateToProps = (state) => {
    return ({

    });
};
const mapDispatchToProps  = (dispatch, ownProps) => {
    return bindActionCreators({

    }, dispatch);
};
export default connect(mapStateToProps,mapDispatchToProps)(MySwitch);
