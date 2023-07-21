import { SWITCH_MODE } from '../constants/actionTypes';
//初始化状态
const initialState ={
    isMobile:false
};

export default function page(state = initialState,action) {
    switch(action.type) {
        case SWITCH_MODE:
            return {isMobile:action.mode};
        default:
            return state;
    }
}
