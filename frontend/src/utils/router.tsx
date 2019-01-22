import * as React from 'react';
import { connect } from 'react-redux';
import { getFromLocalStorage } from './localStorage';
import { LocalStorage } from '../config/constants';
import { Redirect } from 'react-router-dom';
import { bindActionToPromise } from '../utils/redux';
import { getUserData } from '../store/auth/auth.actions'

/* tslint:disable: variable-name */
export const authenticatedOnlyComponent = (WrappedComponent) => {

  const mapDispatchToProps = (dispatch) => ({
    actions: {
      getUserData: bindActionToPromise(dispatch, getUserData.started),
    },
    dispatch
  });
  class AuthenticatedComponent extends React.Component<{}, {}> {

    componentDidMount() {
      if (this.isLoggedIn()) {
        console.log(':)')
      }
    }

    isLoggedIn() {
      return getFromLocalStorage(LocalStorage.userToken) !== null;
    }

    render() {

      return this.isLoggedIn() ? <WrappedComponent {...this.props} /> : <Redirect to={{
        pathname: '/',
      }} />;
    }
  };

  return connect(null, mapDispatchToProps)(AuthenticatedComponent);

};
/* tslint:enable */
