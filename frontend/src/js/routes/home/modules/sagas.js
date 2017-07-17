import { takeLatest } from 'redux-saga';
import { call, put } from  'redux-saga/effects';
import {testRequest} from '../../../api/api';
import {
    TEST_REQUEST,
    testFailed,
    testSuccess
} from '../../../actions/actions';


function* testSaga(action) {
    try {
        const items = yield call(testRequest);
        yield put(testSuccess());
    } catch (e) {
        yield put(testFailed());
    }
}

export function* homeSagas() {
    yield [
        takeLatest(TEST_REQUEST, testSaga),
    ]
}
