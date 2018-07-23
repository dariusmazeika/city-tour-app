import types from './types';
export function testRequest() {
    return { type: types.TEST.REQUEST };
}
export function testSuccess() {
    return { type: types.TEST.SUCCESS };
}
export function testFailed() {
    return { type: types.TEST.FAILURE };
}
