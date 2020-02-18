import * as React from 'react';
import { render } from 'react-dom';
import { setConfig } from 'react-hot-loader';

import Root from './components/root';
import configureStore, { history } from './store/configureStore';
import '../styles/index.scss';

setConfig({ pureSFC: false, ignoreSFC: true, pureRender: false, disableHotRenderer: true });
const store = configureStore();

render(<Root store={store} history={history} />, document.getElementById('mount'));
