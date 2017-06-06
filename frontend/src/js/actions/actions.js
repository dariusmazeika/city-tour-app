/**
 * Created by tomasgobionis on 6/5/17.
 */
export const TEST_REQUEST = 'TEST_REQUEST';
export function testRequest() {
    return {type: TEST_REQUEST};
}

export const TEST_RESPONSE_SUCCESSFUL = 'TEST_RESPONSE_SUCCESSFUL';
export function testSuccess() {
    return {type: TEST_RESPONSE_SUCCESSFUL};
}

export const TEST_RESPONSE_FAILED = 'TEST_RESPONSE_FAILED';
export function testFailed() {
    return {type: TEST_RESPONSE_FAILED};
}
