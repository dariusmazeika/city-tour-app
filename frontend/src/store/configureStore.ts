import { createStore, compose, applyMiddleware } from 'redux';
import reduxImmutableStateInvariant from 'redux-immutable-state-invariant';
// import reduxThunk from 'redux-thunk';
import createBrowserHistory from 'history/createBrowserHistory';
// 'routerMiddleware': the new way of storing route changes with redux middleware since rrV4.
import { connectRouter, routerMiddleware } from 'connected-react-router';
import reducers from './reducers';
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
    // Add other middleware on this line...
    sagaMiddleware,
    // thunk middleware can also accept an extra argument to be passed to each thunk action
    // https://github.com/reduxjs/redux-thunk#injecting-a-custom-argument
    // reduxThunk,
    reactRouterMiddleware,
  ];

  const store =  createStore(
    connectRouterHistory(reducers),
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
    // Add other middleware on this line...
    sagaMiddleware,
    // Redux middleware that spits an error on you when you try to mutate your state either inside a dispatch or between dispatches.
    reduxImmutableStateInvariant(),

    // thunk middleware can also accept an extra argument to be passed to each thunk action
    // https://github.com/reduxjs/redux-thunk#injecting-a-custom-argument
    // reduxThunk,
    reactRouterMiddleware,
  ];

  const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose; // add support for Redux dev tools
  const store = createStore(
    connectRouterHistory(reducers),
    initialState,
    composeEnhancers(applyMiddleware(...middlewares)),
  );

  if (module.hot) {
    // Enable Webpack hot module replacement for reducers
    module.hot.accept('./reducers', () => {
      const nextRootReducer = require('./reducers').default; // eslint-disable-line global-require
      store.replaceReducer(connectRouterHistory(nextRootReducer));
    });
  }

  initSagas(sagas, sagaMiddleware);

  return store;
}

const configureStore = process.env.NODE_ENV === 'production' ? configureStoreProd : configureStoreDev;

export default configureStore;
