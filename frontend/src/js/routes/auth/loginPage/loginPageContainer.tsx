import * as React from 'react';
import { connect } from 'react-redux';
import { bindActionCreators, Dispatch } from 'redux';

import { authActions, localizationActions } from '@Store/actions';
import { bindActionToPromise } from '@Utils/redux';

import LoginForm from './components/loginForm';

export interface LoginPageContainerActions {
  actions: {
    login: any;
    changeLanguage: any;
  };
}

const loginPageContainer: React.FunctionComponent<LoginPageContainerActions> = ({ actions }) => {
  return (
    <div>
      <button onClick={() => {
        actions.changeLanguage({ lang: 'lt' });
      }}
      >
        Change s
      </button>
      <LoginForm onSubmit={actions.login} />
    </div>
  );
};

const mapDispatchToProps = (dispatch: Dispatch) => ({
  actions: {
    login: bindActionToPromise<any>(dispatch, authActions.login.started),
    ...bindActionCreators({ changeLanguage: localizationActions.changeLanguage }, dispatch),
  },
});
export default connect<{}, LoginPageContainerActions, {}>(
  null,
  mapDispatchToProps,
)(loginPageContainer);
