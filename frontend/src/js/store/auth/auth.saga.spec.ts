import reduxSagaTesting from 'redux-saga-testing';

import { LocalStorage } from '@Config/constants';
import { setToLocalStorage } from '@Utils/localStorage';
import { callApiPost, handleFormSubmit } from '@Utils/sagas';

import { login, logout } from './auth.actions';
import { loginSaga, logoutSaga } from './auth.saga';
import { LoginActionPayload } from './auth.types';

describe('Auth sagas', () => {

  describe('loginSaga(): Request path', () => {

    const actionPayload: LoginActionPayload = {
      email: 'myemail@mail.com',
      password: 'helloPassword',
      resolve: () => { },
      reject: () => { },
    };

    const it = reduxSagaTesting(loginSaga(login.started(actionPayload)));
    it('should return null', (result: any) => {
      expect(result).toBe(undefined);
    });
    it('Should start loading', (result: any) => {
      expect(result).toEqual(handleFormSubmit('/api/login/', login.started(actionPayload), login));
    });
  });

  describe('logoutSaga(): Request path', () => {

    const actionPayload: {} = {};

    const it = reduxSagaTesting(logoutSaga(logout.started(actionPayload)));
    it('Should start logout and call API', (result: any) => {
      expect(result).toEqual(callApiPost('/api/logout/', logout.started(actionPayload), logout));
    });

    it('Should set empty local storage', (result: any) => {
      expect(result).toEqual(setToLocalStorage(LocalStorage.userToken, null));
    });
  });
});
