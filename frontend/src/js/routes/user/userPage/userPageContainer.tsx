import * as React from 'react';
import { connect } from 'react-redux';

import { UserData } from '../../../store/auth/auth.types';
import { RootState } from '../../../store/reducers';

export interface UserPageContainerProps {
  user: UserData;
  newUser: any;
}

class UserPageContainer extends React.PureComponent<UserPageContainerProps> {

  render() {
    const { isFetching, item } = this.props.user;
    return (
      <div>
        <h2>
          {!item || isFetching ? <div>I am loading</div> : <div>{item.email}</div>}
        </h2>
      </div>
    );
  }

}

const mapStateToProps = (state: RootState) => ({
  user: state.auth.userData,
});

export default connect(mapStateToProps, null)(UserPageContainer);
