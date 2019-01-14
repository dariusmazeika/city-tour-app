import reduxSagaTesting from 'redux-saga-testing';
import { loginSaga } from './auth.saga';
import { login } from './auth.actions';
import { LoginActionPayload } from './auth.types';

import { handleFormSubmit } from '../../utils/sagas';

describe('Auth sagas', () => {

  describe('loginSaga(): Request path', () => {

    const actionPayload: LoginActionPayload = {
      email: 'myemail@mail.com',
      password: 'helloPassword',
      resolve: () => {},
      reject: () => {},
    };

    const it = reduxSagaTesting(loginSaga(login.started(actionPayload)));
    it('Should start loading', (result) => {
      expect(result).toEqual(handleFormSubmit('login', login.started(actionPayload), login));
    });
  });
});
