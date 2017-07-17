export default class BaseReducer {
    constructor() {
        this.initialState = {};
        this.ACTION_HANDLERS = {};
        this.handleActions = this.handler.bind(this);

    }

    handler(state, action) {
        if (!state) {
            state = this.initialState;
        }
        const handler = this.ACTION_HANDLERS[action.type];
        return handler ? handler(state, action) : state;
    }

}
