import * as React from 'react';
import { BrowserRouter, Redirect, Route, Switch } from 'react-router-dom';

import routes from '../routes';

import DocumentTitle from './documentTitle';

const App: React.FunctionComponent<{}> = () => {
  return (
    <BrowserRouter>
      <Switch>
        {routes.map(route => (
          <Route
            path={route.path}
            exact
            key={route.path}
            component={(props: JSX.IntrinsicAttributes) => {
              return (
                <DocumentTitle title={route.title}>
                  <route.component {...props} />
                </DocumentTitle>
              );
            }}
          />
        ))}
        <Redirect to="/" />
      </Switch>
    </BrowserRouter>
  );

};
export default App;
