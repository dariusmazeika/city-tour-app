import { takeLatest } from 'redux-saga';
import { call, put } from  'redux-saga/effects';
import {testRequest} from '../../../api/api';
import types from '../../../actions/types';

import {
    testFailed,
    testSuccess
} from '../../../actions/actions';


function* testSaga() {
    try {
        const items = yield call(testRequest);
        yield put(testSuccess(items));
    } catch (e) {
        yield put(testFailed());
    }
}

export function* homeSagas() {
    yield [
        takeLatest(types.TEST.REQUEST, testSaga),
    ];
}
