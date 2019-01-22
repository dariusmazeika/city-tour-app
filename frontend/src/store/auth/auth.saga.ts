import { all, takeLatest } from 'redux-saga/effects';
import { login, logout, getUserData } from './auth.actions';
import { callApiGet, handleFormSubmit } from '../../utils/sagas';
import { Action } from 'typescript-fsa';
import { LoginActionPayload, LoginActionSuccess } from './auth.types';
import { setToLocalStorage } from '../../utils/localStorage';
import { LocalStorage } from '../../config/constants';

export function* loginSaga(action: Action<LoginActionPayload>) {
  yield handleFormSubmit('/api/login/', action, login);
}

export function* loginSuccessSaga(action: Action<LoginActionSuccess>) {
  setToLocalStorage(LocalStorage.userToken, action.payload.result.token);
}

export function* getUserDataSaga(action: Action<LoginActionPayload>) {
  yield callApiGet('/api/login/', action, login);
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
    yield takeLatest(getUserData.started, logoutSaga),
  ]);
}
