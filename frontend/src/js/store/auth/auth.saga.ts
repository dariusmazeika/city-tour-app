import { all, put, takeLatest } from 'redux-saga/effects';
import { Action } from 'typescript-fsa';

import { LocalStorage } from '@Config/constants';
import { deleteFromLocalStorage, setToLocalStorage } from '@Utils/localStorage';
import { callApiGet, callApiPost, handleFormSubmit } from '@Utils/sagas';

import { locationChange } from '../navigation/navigation.actions';

import { getUserData, login, logout } from './auth.actions';
import { LoginActionPayload, LoginActionSuccess } from './auth.types';

export function* loginSaga(action: Action<LoginActionPayload>) {
  yield deleteFromLocalStorage(LocalStorage.userToken);
  yield handleFormSubmit('/api/login/', action, login);
}

export function* loginSuccessSaga(action: Action<LoginActionSuccess>) {
  yield setToLocalStorage(LocalStorage.userToken, action.payload.result.token);
  yield put(locationChange({ path: '/user' }));
}

export function* getUserDataSaga(action: Action<{}>) {
  yield callApiGet('/api/current-user/', action, getUserData);
}

export function* logoutSaga(action: any) {
  yield callApiPost('/api/logout/', action, logout);
  yield deleteFromLocalStorage(LocalStorage.userToken);

}

export function* watchAuthSaga() {
  yield all([
    yield takeLatest(login.started, loginSaga),
    yield takeLatest(login.done, loginSuccessSaga),
    yield takeLatest(logout.started, logoutSaga),
    yield takeLatest(getUserData.started, getUserDataSaga),
  ]);
}
