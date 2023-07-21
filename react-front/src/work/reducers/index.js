import { combineReducers } from 'redux';
import userInfo from './userInfo';
import mode from './mode';
import msg from './msg';
import setting from './setting';
import chat from './chat';
import otherConfig from './otherConfig';
const rootReducer = combineReducers({
    userInfo,
    msg,
    mode,
    setting,
    chat,
    otherConfig
});

export default rootReducer;
