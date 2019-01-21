import * as React from 'react';
import { getFromLocalStorage } from './localStorage';
import { LocalStorage } from '../config/constants';
import { Redirect } from 'react-router-dom';

/* tslint:disable: variable-name */
export const authenticatedOnlyComponent = (WrappedComponent) => {
  return class AuthenticatedComponent extends React.Component<{}, {}> {

    isLoggedIn() {
      return getFromLocalStorage(LocalStorage.userToken) !== null;
    }

    render() {

      return this.isLoggedIn() ? <WrappedComponent {...this.props} /> :<Redirect to={{
        pathname: '/',
      }}/>;
    }
  };
};
/* tslint:enable */
