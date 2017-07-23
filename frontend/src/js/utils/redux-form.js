import {
    Promise
} from 'es6-promise';
import {SubmissionError} from 'redux-form';
import {callPost, callUpdate} from './api';
import {call} from 'redux-saga/effects';

export const bindActionToPromise = (dispatch, actionCreator) => payload => {
    return new Promise((resolve, reject) => dispatch(actionCreator(payload, resolve, reject)));
};

function* handleFormAction(url, callAction, action){
    try {
        const result = yield call(callAction, url, action.payload.data);
        yield call(action.payload.resolve, result);
        return result;
    } catch (e) {
        let error = new SubmissionError(e.response);
        if (e.response.non_field_errors) {
            error = new SubmissionError({_error: e.response.non_field_errors});
        }
        if (e.response.message) {
            error = new SubmissionError({_error: e.response.message});
        }
        yield call(action.payload.reject, error);
        throw error;
    }
}
export function* handleFormSubmit(url, action) {
    return yield handleFormAction(url, callPost, action);
}

export function* handleFormUpdate(url, action) {
    return yield handleFormAction(url, callUpdate, action);
}
