import reduxSagaTesting from 'redux-saga-testing';

import { LocalStorage } from '../../config/constants';
import { setToLocalStorage } from '../../utils/localStorage';
import { callApiGet, handleFormSubmit } from '../../utils/sagas';

import { login, logout } from './auth.actions';
import { loginSaga, logoutSaga } from './auth.saga';
import { LoginActionPayload } from './auth.types';

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
      expect(result).toEqual(handleFormSubmit('/api/login/', login.started(actionPayload), login));
    });
  });

  describe('logoutSaga(): Request path', () => {

    const actionPayload: {} = {};

    const it = reduxSagaTesting(logoutSaga(logout.started(actionPayload)));
    it('Should start logout and call API', (result) => {
      expect(result).toEqual(callApiGet('/api/logout/', logout.started(actionPayload), logout));
    });

    it('Should set empty local storage', (result) => {
      expect(result).toEqual(setToLocalStorage(LocalStorage.userToken, null));
    });
  });
});
