import {CHANGE_MODAL} from '../constants/actionTypes';
//初始化状态
const initialState ={page:"CLOSE_MODAL",data:{}};

export default function modalControl(state = initialState,action) {
    switch(action.type) {
        case CHANGE_MODAL:
            return  {page:action.data.page,data:action.data.para};
        default:
            return state;
    }
}
