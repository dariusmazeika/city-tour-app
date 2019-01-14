import { NavLink, Route, Switch, Redirect } from 'react-router-dom';
import * as React from 'react';

import { hot } from 'react-hot-loader';
import routes from '../routes';

class App extends React.Component<any, any> {
  render() {
    return (
      <div>
        <Switch>
          {routes.map((route, i) => (
              <Route path={route.path} exact key={route.path}><route.component /></Route>),
          )}
          <Redirect to="/"/>
      </Switch>
      </div>
    );
  }
}

export default hot(module)(App);
