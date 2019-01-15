import { createStore, compose, applyMiddleware } from 'redux';
import reduxImmutableStateInvariant from 'redux-immutable-state-invariant';
import createBrowserHistory from 'history/createBrowserHistory';
import { connectRouter, routerMiddleware } from 'connected-react-router';
import createRootReducer from './reducers';
import reduxSaga from 'redux-saga';
import { initSagas } from '../utils/redux';
import * as sagas from './sagas';

export const history = createBrowserHistory();
const connectRouterHistory = connectRouter(history);

declare global {
  interface Window {
    __REDUX_DEVTOOLS_EXTENSION_COMPOSE__: any;
  }
}

function configureStoreProd(initialState: {} = {}) {
  const sagaMiddleware = reduxSaga();

  const reactRouterMiddleware = routerMiddleware(history);
  const middlewares = [
    sagaMiddleware,
    reactRouterMiddleware,
  ];

  const store =  createStore(
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
      const nextRootReducer = require('./reducers').default;
    });
  }

  initSagas(sagas, sagaMiddleware);

  return store;
}

const configureStore = process.env.NODE_ENV === 'production' ? configureStoreProd : configureStoreDev;

export default configureStore;
