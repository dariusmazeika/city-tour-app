import {call, put, takeLatest} from 'redux-saga/effects';
import types from '../../../actions/types';
import API from '../../../utils/api';

import {
    testFailed,
    testSuccess
} from '../../../actions/actions';


function* testSaga() {
    try {
        const items = yield call(API.callGet, '/get');
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
