import { all, put, takeLatest } from 'redux-saga/effects';
import { login, logout, getUserData } from './auth.actions';
import { callApiGet, handleFormSubmit } from '../../utils/sagas';
import { Action } from 'typescript-fsa';
import { LoginActionPayload, LoginActionSuccess } from './auth.types';
import { setToLocalStorage } from '../../utils/localStorage';
import { LocalStorage } from '../../config/constants';
import { locationChange } from '../navigation/navigation.actions';

export function* loginSaga(action: Action<LoginActionPayload>) {
  yield handleFormSubmit('/api/login/', action, login);
}

export function* loginSuccessSaga(action: Action<LoginActionSuccess>) {
  yield setToLocalStorage(LocalStorage.userToken, action.payload.result.token);
  yield put(locationChange({ path: "/user" }));
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
