/**
 * Created by tomasgobionis on 6/5/17.
 */
import {
    TEST_RESPONSE_FAILED,
    TEST_RESPONSE_SUCCESSFUL
} from '../../../actions/actions';

export function testSuccess(state, action) {
    return {...state, testSuccess: true}
}

export function testFailed(state, action) {
    return {...state, testSuccess: true}
}

const ACTION_HANDLERS = {
    [TEST_RESPONSE_FAILED]: (state, action) => testFailed(state, action),
    [TEST_RESPONSE_SUCCESSFUL]: (state, action) => testFailed(state, action),
};

const initialState = {};

export default (state = initialState, action) => {
    const handler = ACTION_HANDLERS[action.type]
    return handler ? handler(state, action) : state
}
