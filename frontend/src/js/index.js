import React from 'react';
import ReactDOM from 'react-dom';
import {AppContainer} from 'react-hot-loader';
import {Provider} from 'react-redux';
import {buildStore} from './store/store';
import App from './app/app';

import '../style/index.scss';
import { ConnectedRouter, routerMiddleware } from 'react-router-redux';
import createHistory from 'history/createBrowserHistory';


// Create a history of your choosing (we're using a browser history in this case)
const history = createHistory();
const middleware = routerMiddleware(history);

const MOUNT_NODE = document.getElementById('root');
const store = buildStore(middleware);

const renderRoot = Component => ReactDOM.render(
    <Provider store={store}>
    <ConnectedRouter history={history}>
        <AppContainer>
            <Component store={store}/>
        </AppContainer>
    </ConnectedRouter>
</Provider>, MOUNT_NODE);

renderRoot(App);

// if (window.devToolsExtension) {
//     window.devToolsExtension.open()
// }

if (module.hot) {
    module.hot.accept(() => {
        const reducers = require('./reducers').default;
        store.replaceReducer(reducers(store.asyncReducers));
        renderRoot(App);
    });
}
