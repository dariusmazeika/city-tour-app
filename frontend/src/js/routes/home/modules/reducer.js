import types from '../../../actions/types';


export function testSuccess(state) {
    return {...state, testSuccess: true};
}

export function testFailed(state) {
    return {...state, testSuccess: true};
}

const ACTION_HANDLERS = {
    [types.TEST.FAILURE]: (state, action) => testFailed(state, action),
    [types.TEST.SUCCESS]: (state, action) => testFailed(state, action),
};

const initialState = {};

export default (state = initialState, action) => {
    const handler = ACTION_HANDLERS[action.type];
    return handler ? handler(state, action) : state;
};
