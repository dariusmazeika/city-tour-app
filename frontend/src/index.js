import * as React from 'react';
import { render } from 'react-dom';
import { AppContainer } from 'react-hot-loader';
import configureStore, { history } from './store/configureStore';
import Root from './components/root';
import './styles/styles.scss';
const store = configureStore();

render(
  <AppContainer>
    <Root store={store} history={history} />
  </AppContainer>,
  document.getElementById('mount')
);

if (module.hot) {
  module.hot.accept('./components/root', () => {
    const NewRoot = require('./components/root').default;
    render(
      <AppContainer>
        <NewRoot store={store} history={history} />
      </AppContainer>,
      document.getElementById('mount')
    );
  });
}
