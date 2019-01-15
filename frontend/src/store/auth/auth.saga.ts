import { all, takeLatest } from 'redux-saga/effects';
import { login, logout } from './auth.actions';
import { handleFormSubmit } from '../../utils/sagas';
import { Action } from 'typescript-fsa';
import { LoginActionPayload } from './auth.types';

export function* loginSaga(action: Action<LoginActionPayload>) {
  yield handleFormSubmit('login', action, login);
}
export function* logoutSaga() {
  yield console.log('Will logout');
}

export function* watchAuthSaga() {
  yield all([
    yield takeLatest(login.started, loginSaga),
    yield takeLatest(logout.started, logoutSaga),
  ]);
}
