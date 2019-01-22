import { all, takeEvery, put } from 'redux-saga/effects';
import { push } from 'connected-react-router';
import { locationChange } from './navigation.actions';
import { Action } from 'typescript-fsa';
import { NavigationActionPayload } from './navigation.types';

function* locationRedirect(action: Action<NavigationActionPayload>) {
  yield put(push(action.payload.path));
}

export function* navigationSaga() {
  yield all([
    yield takeEvery(locationChange, locationRedirect),
  ]);
}
