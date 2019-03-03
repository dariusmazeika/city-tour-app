import * as React from 'react';
import { Redirect, Route, Switch } from 'react-router-dom';

import routes from '../routes';

import DocumentTitle from './documentTitle';

const app: React.FunctionComponent<{}> = () => {
  return (<Switch>
    {routes.map(route => (
      <Route path={route.path} exact key={route.path} component={(props) => {
        return (<DocumentTitle title={route.title}>
          <route.component {...props}/>
        </DocumentTitle>);
      }}>

      </Route>),
    )}
    <Redirect to="/" />
  </Switch>);

};
export default app;
