import * as React from 'react';
import { connect } from 'react-redux';
import { Dispatch } from 'redux';

import { authActions } from '../../../store/actions';
import { changeLanguage } from '../../../store/localization/localization.actions';
import { RootState } from '../../../store/reducers';
import { bindActionToPromise } from '../../../utils/redux';

import LoginForm from './components/loginForm';

export interface LandingPageContainerProps {
  dispatch: Dispatch<any>;
  actions: {
    login: (values: Partial<{}>, dispatch: Dispatch<any>, props: {}) => Promise<any>;
  };
}

export class LoginPageContainer extends React.PureComponent<LandingPageContainerProps, {}> {
  render() {
    return (
      <div>
        <a onClick={() => {
          this.props.dispatch(changeLanguage({ lang: 'lt' }));
        }}>Change</a>
        <LoginForm onSubmit={this.props.actions.login} />
      </div>
    );
  }
}

const mapStateToProps = (state: RootState) => ({
  clickCount: state,
});

const mapDispatchToProps = (dispatch: Dispatch) => ({
  dispatch,
  actions: {
    login: bindActionToPromise(dispatch, authActions.login.started),
  },
});

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(LoginPageContainer);
