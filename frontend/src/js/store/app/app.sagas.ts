import { all, put , takeLatest } from 'redux-saga/effects';
import { Action } from 'typescript-fsa';

import { locationChange } from '@Store/navigation/navigation.actions';

import { LocalStorage } from '@Config/constants';

import { deleteFromLocalStorage } from '@Utils/localStorage';
import { ActionErrorType } from '@Utils/types';

export function* onEmployeeSignupDone(action:Action<ActionErrorType>) {
  if (action.payload.error.status === 401) {
    yield deleteFromLocalStorage(LocalStorage.userToken);
    yield put(locationChange({ path: '/login' }));
  }

}

export function* appSagas() {
  yield all([
    yield takeLatest(action => /_FAILED/.test(action.type), onEmployeeSignupDone),
  ]);
}
