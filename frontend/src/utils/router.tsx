import * as React from 'react';
import { connect } from 'react-redux';
import { Dispatch, bindActionCreators } from 'redux';
import { getFromLocalStorage } from './localStorage';
import { LocalStorage } from '../config/constants';
import { authActions } from '../store/actions';
import { Redirect } from 'react-router-dom';

export interface AuthenticatedComponentProps {
  actions: {
    getUserData: typeof authActions.getUserData.started;
  };
  dispatch: Dispatch;
}

/* tslint:disable: variable-name */
export const authenticatedOnlyComponent = (WrappedComponent: any) => {

  const mapDispatchToProps = (dispatch: Dispatch) => ({
    dispatch,
    actions: {
      getUserData: bindActionCreators(authActions.getUserData.started, dispatch),
    },
  });

  class AuthenticatedComponent extends React.PureComponent<AuthenticatedComponentProps, {}>{

    componentDidMount() {
      if (this.isLoggedIn()) {
        this.props.actions.getUserData({});
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
  }

  return connect(null, mapDispatchToProps)(AuthenticatedComponent);

};
/* tslint:enable */
