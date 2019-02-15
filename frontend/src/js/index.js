import { setConfig } from 'react-hot-loader';
setConfig({ pureSFC: false ,ignoreSFC: true, pureRender: false,disableHotRenderer:true});

import * as React from 'react';
import { render } from 'react-dom';
import configureStore, { history } from './store/configureStore';
import Root from './components/root';
import '../styles/index.scss';
const store = configureStore();

render(<Root store={store} history={history} />, document.getElementById('mount'));
