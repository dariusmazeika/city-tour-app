import { FORM_ERROR } from 'final-form';
import { call, put } from 'redux-saga/effects';
import { Action, AsyncActionCreators } from 'typescript-fsa';

import { callGet, callPatch, callPost, callUpdate } from './api';

export function* handleFormAction<Params, Result, Error>(
  url: string,
  action: Action<any>,
  actionType: AsyncActionCreators<Params, Result, Error>,
  callAction: any,
) {
  const { resolve, reject, ...requestPayload } = action.payload;
  try {
    const result = yield call(callAction, url, requestPayload);
    yield call(action.payload.resolve, result);
    yield put(actionType.done({ result, params: action.payload }));
  } catch (e) {
    const { data: { non_field_errors, ...restData } } = e.response;
    const errorResponse = { ...restData };
    if (non_field_errors) {
      errorResponse[ FORM_ERROR ] = non_field_errors;
    }
    yield call(reject, errorResponse);
    yield put(actionType.failed({ error: errorResponse as Error, params: action.payload }));
  }
}

export function* handleFormUpdate<Params, Result, Error>(
  url: string,
  action: Action<any>,
  actionType: AsyncActionCreators<Params, Result, Error>,
) {
  yield handleFormAction(url, action, actionType, callUpdate);
}
export function* handleFormSubmit<Params, Result, Error>(
  url: string,
  action: Action<any>,
  actionType: AsyncActionCreators<Params, Result, Error>,
) {
  yield handleFormAction(url, action, actionType, callPost);
}
export function* handleFormPatch<Params, Result, Error>(
  url: string,
  action: Action<any>,
  actionType: AsyncActionCreators<Params, Result, Error>,
) {
  yield handleFormAction(url, action, actionType, callPatch);
}

export function* callApiGet<Params, Result, Error>(
  url: string,
  action: Action<any>,
  actionType: AsyncActionCreators<Params, Result, Error>,
) {
  try {
    const result = yield call(callGet, url);
    yield put(actionType.done({ result, params: action.payload }));
  } catch (error) {
    yield put(actionType.failed({ error, params: action.payload }));
  }
}

export function* callApiPut<Params, Result, Error>(
  url: string,
  action: Action<any>,
  actionType: AsyncActionCreators<Params, Result, Error>,
) {
  try {
    const result = yield call(callUpdate, url, action.payload);
    yield put(actionType.done({ result, params: action.payload }));
  } catch (error) {
    yield put(actionType.failed({ error, params: action.payload }));
  }
}

export function* callApiPost<Params, Result, Error>(
  url: string,
  action: Action<any>,
  actionType: AsyncActionCreators<Params, Result, Error>,
) {
  try {
    const result = yield call(callPost, url, action.payload);
    yield put(actionType.done({ result, params: action.payload }));
  } catch (error) {
    yield put(actionType.failed({ error, params: action.payload }));
  }
}
