import { routerMiddleware } from 'connected-react-router';
import { createBrowserHistory } from 'history';
import { applyMiddleware, compose, createStore } from 'redux';
import reduxImmutableStateInvariant from 'redux-immutable-state-invariant';
import reduxSaga from 'redux-saga';

import { initSagas } from '@Utils/redux';

import createRootReducer from './reducers';
import * as sagas from './sagas';

export const history = createBrowserHistory();

declare global {
  interface Window {
    __REDUX_DEVTOOLS_EXTENSION_COMPOSE__: any;
    _app_conf: any;
    _app_messages: any;
  }
}

function configureStoreProd(initialState: {} = {}) {
  const sagaMiddleware = reduxSaga();

  const reactRouterMiddleware = routerMiddleware(history);
  const middlewares = [
    sagaMiddleware,
    reactRouterMiddleware,
  ];

  const store = createStore(
    createRootReducer(history),
    initialState,
    compose(applyMiddleware(...middlewares)),
  );
  initSagas(sagas, sagaMiddleware);

  return store;
}

function configureStoreDev(initialState: {} = {}) {
  const sagaMiddleware = reduxSaga();

  const reactRouterMiddleware = routerMiddleware(history);
  const middlewares = [
    sagaMiddleware,
    reduxImmutableStateInvariant(),
    reactRouterMiddleware,
  ];

  const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
  const store = createStore(
    createRootReducer(history),
    initialState,
    composeEnhancers(applyMiddleware(...middlewares)),
  );

  if (module.hot) {
    // Enable Webpack hot module replacement for reducers
    module.hot.accept('./reducers', () => {
    });
  }

  initSagas(sagas, sagaMiddleware);

  return store;
}

const configureStore = process.env.NODE_ENV === 'production' ? configureStoreProd : configureStoreDev;

export default configureStore;
