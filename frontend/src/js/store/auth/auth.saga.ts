import { all, put, takeLatest } from 'redux-saga/effects';
import { Action } from 'typescript-fsa';

import { LocalStorage } from '../../config/constants';
import { setToLocalStorage } from '../../utils/localStorage';
import { callApiGet, handleFormSubmit } from '../../utils/sagas';
import { locationChange } from '../navigation/navigation.actions';

import { getUserData, login, logout } from './auth.actions';
import { LoginActionPayload, LoginActionSuccess } from './auth.types';

export function* loginSaga(action: Action<LoginActionPayload>) {
  yield handleFormSubmit('/api/login/', action, login);
}

export function* loginSuccessSaga(action: Action<LoginActionSuccess>) {
  yield setToLocalStorage(LocalStorage.userToken, action.payload.result.token);
  yield put(locationChange({ path: '/user' }));
}

export function* getUserDataSaga(action: Action<{}>) {
  yield callApiGet('/api/current-user/', action, getUserData);
}

export function* logoutSaga(action) {
  yield callApiGet('/api/logout/', action, logout);
  yield setToLocalStorage(LocalStorage.userToken, null);
}

export function* watchAuthSaga() {
  yield all([
    yield takeLatest(login.started, loginSaga),
    yield takeLatest(login.done, loginSuccessSaga),
    yield takeLatest(logout.started, logoutSaga),
    yield takeLatest(getUserData.started, getUserDataSaga),
  ]);
}
