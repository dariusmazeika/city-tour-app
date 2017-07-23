import {handleFormSubmit as handleFormSubmitAction, handleFormUpdate as handleFormUpdateAction} from '../utils/redux-form';
import {put} from 'redux-saga/effects';

function* handleFormAction(url, action, actionType, submitAction){
    try {
        const result = yield submitAction(url, action);
        yield put({type: actionType.SUCCESS, payload: result});
    } catch (e) {
        yield put({type: actionType.FAILURE, payload: e});
    }
}

export function* handleFormSubmit(url, action, actionType) {
    yield handleFormAction(url, action, actionType, handleFormSubmitAction);
}
export function* handleFormUpdate(url, action, actionType) {
    yield handleFormAction(url, action, actionType, handleFormUpdateAction);

}
