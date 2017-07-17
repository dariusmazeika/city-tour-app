import {createStore, applyMiddleware, compose} from 'redux';
import createSagaMiddleware from 'redux-saga';
import thunk from 'redux-thunk';
import { createLogger } from 'redux-logger';
import RootSaga from '../sagas';
import combineReducers from '../reducers';

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

export function configureStore(initialState) {
    const sagaMiddleware = createSagaMiddleware();
    const logger = createLogger();
    const middleware = [sagaMiddleware, thunk, logger];
    return {
        ...createStore(combineReducers,
            initialState,
            composeEnhancers(applyMiddleware(...middleware))),
        runSaga: sagaMiddleware.run
    };
}
export const store = configureStore();
store.runSaga(RootSaga);
