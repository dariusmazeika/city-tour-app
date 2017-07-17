import React from 'react'
import ReactDOM from 'react-dom'
import {AppContainer} from 'react-hot-loader'
import {Provider} from 'react-redux';
import {store} from './store/store';

import App from './app/app'


const MOUNT_NODE = document.getElementById('root')


const renderRoot = Component => ReactDOM.render(
    <Provider store={store}>
        <AppContainer>
            <Component store={store}/>
        </AppContainer>
    </Provider>,
    MOUNT_NODE
);

renderRoot(App);

// if (window.devToolsExtension) {
//     window.devToolsExtension.open()
// }

if (module.hot) {
    module.hot.accept(() => {
        const reducers = require('./store/reducers').default;
        store.replaceReducer(reducers(store.asyncReducers));
        renderRoot(App)
    });
}
