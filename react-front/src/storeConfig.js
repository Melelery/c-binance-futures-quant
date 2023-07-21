import { compose, createStore, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
import rootReducer from './work/reducers';
const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const store = createStore(rootReducer, /* preloadedState, */ composeEnhancers(
    applyMiddleware(thunk)
));

export default function storeConfig(initialState) {
    const store = createStore(rootReducer, /* preloadedState, */ composeEnhancers(
        applyMiddleware(thunk)
    ));
    return store;
}
