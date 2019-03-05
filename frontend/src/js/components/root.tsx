import { ConnectedRouter } from 'connected-react-router';
import * as React from 'react';
import { hot } from 'react-hot-loader/root';
import { Provider } from 'react-redux';
import { Store } from 'redux';

import { AppContextProvider } from '@Config/localeContext';

import App from './app';
interface RootContainerProps {
  store: Store;
  history: any;
}
const root: React.FunctionComponent<RootContainerProps> = ({ store, history }) => {
  return (
    <AppContextProvider value={store.getState().localization.currentLanguage}>
      <Provider store={store}>
        <ConnectedRouter history={history}>
          <App />
        </ConnectedRouter>
      </Provider>
    </AppContextProvider>
  );
};

export default hot(root);
