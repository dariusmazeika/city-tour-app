import types from '../../../actions/types';
import BaseReducer from '../../../reducers/base-reducer';
class HomePageReducer extends BaseReducer {
    constructor() {
        super();
        this.initialState = {};
        this.ACTION_HANDLERS = {
            [types.TEST.FAILURE]: this.testFailed,
            [types.TEST.SUCCESS]: this.testSuccess,
        };
    }

    testFailed(state) {
        return { ...state,
            testSuccess: false
        };
    }

    testSuccess(state) {
        return { ...state,
            testSuccess: true
        };
    }

}
export default new HomePageReducer().handleActions;
