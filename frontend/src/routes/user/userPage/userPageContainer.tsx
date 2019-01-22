import * as React from 'react';
import { connect } from 'react-redux';
import { RootState } from '../../../store/reducers';
import { UserData } from '../../../store/auth/auth.types';

export interface UserPageContainerProps {
  user: UserData,
}

class UserPageContainer extends React.PureComponent<UserPageContainerProps> {

  render() {
    return (
      <div>
        <h2>
          {this.props.user ? this.props.user.email : <div>NO USER</div>}
        </h2>
      </div>
    );
  }

};

const mapStateToProps = (state: RootState) => ({
  user: state.auth.userData
});

export default connect(mapStateToProps, null)(UserPageContainer);
