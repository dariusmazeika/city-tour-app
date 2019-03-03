import * as React from 'react';
import { Redirect, Route, Switch } from 'react-router-dom';

import routes from '../routes';

class App extends React.Component<{}, {}> {
  render() {
    return (
      <Switch>
        {routes.map(route => (
          <Route path={route.path} exact key={route.path}><route.component /></Route>),
        )}
        <Redirect to="/" />
      </Switch>
    );
  }
}

export default App;
