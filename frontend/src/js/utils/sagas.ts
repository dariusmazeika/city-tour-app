import { SubmissionError } from 'redux-form';
import { call, put } from 'redux-saga/effects';
import { Action, AsyncActionCreators } from 'typescript-fsa';

import { callGet, callPatch, callPost, callUpdate } from './api';

export function* handleFormAction(url: string, action: Action<any>, actionType: AsyncActionCreators<{}, any, {}>, callAction) {
  try {
    const result = yield call(callAction, url, action.payload);
    yield call(action.payload.resolve, result);
    yield put(actionType.done({ result, params: action.payload }));
  } catch (e) {
    let error = new SubmissionError(e.response);
    if (e.response.non_field_errors) {
      error = new SubmissionError({ _error: e.response.non_field_errors });
    }
    if (e.response.message) {
      error = new SubmissionError({ _error: e.response.message });
    }
    yield call(action.payload.reject, error);
    yield put(actionType.failed({ error, params: action.payload }));
  }
}

export function* handleFormUpdate(url: string, action: Action<any>, actionType: AsyncActionCreators<{}, any, {}>) {
  yield handleFormAction(url, action, actionType, callUpdate);
}
export function* handleFormSubmit(url: string, action: Action<any>, actionType: AsyncActionCreators<{}, any, {}>) {
  yield handleFormAction(url, action, actionType, callPost);
}
export function* handleFormPatch(url: string, action: Action<any>, actionType: AsyncActionCreators<{}, any, {}>) {
  yield handleFormAction(url, action, actionType, callPatch);
}

export function* callApiGet(url: string, action: Action<any>, actionType: AsyncActionCreators<{}, any, {}>) {
  try {
    const result = yield call(callGet, url);
    yield put(actionType.done({ result, params: action.payload }));
  } catch (error) {
    yield put(actionType.failed({ error, params: action.payload }));
  }
}

export function* callApiPut(url: string, action: Action<any>, actionType: AsyncActionCreators<{}, any, {}>) {
  try {
    const result = yield call(callUpdate, url, action.payload);
    yield put(actionType.done({ result, params: action.payload }));
  } catch (error) {
    yield put(actionType.failed({ error, params: action.payload }));
  }
}

export function* callApiPost(url: string, action: Action<any>, actionType: AsyncActionCreators<{}, any, {}>) {
  try {
    const result = yield call(callPost, url, action.payload);
    yield put(actionType.done({ result, params: action.payload }));
  } catch (error) {
    yield put(actionType.failed({ error, params: action.payload }));
  }
}
