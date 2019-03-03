import { push } from 'connected-react-router';
import { all, put, takeEvery } from 'redux-saga/effects';
import { Action } from 'typescript-fsa';

import { locationChange } from './navigation.actions';
import { NavigationActionPayload } from './navigation.types';

function* locationRedirect(action: Action<NavigationActionPayload>) {
  yield put(push(action.payload.path));
}

export function* navigationSaga() {
  yield all([
    yield takeEvery(locationChange, locationRedirect),
  ]);
}
