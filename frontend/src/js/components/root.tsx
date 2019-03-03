import { ConnectedRouter } from 'connected-react-router';
import * as React from 'react';
import { hot } from 'react-hot-loader/root';
import { Provider } from 'react-redux';
import { Store } from 'redux';

import App from './app';
interface RootContainerProps {
  store: Store;
  history: any;
}
const root: React.FunctionComponent<RootContainerProps> = ({ store, history }) => {
  return (
    <Provider store={store}>
      <ConnectedRouter history={history}>
        <App />
      </ConnectedRouter>
    </Provider>
  );
};

// class Root extends React.PureComponent<any, any> {
//   render() {
//     const { store, history } = this.props;
//     return (
//       <Provider store={store}>
//         <ConnectedRouter history={history}>
//           <App />
//         </ConnectedRouter>
//       </Provider>
//     );
//   }
// }

export default hot(root);
