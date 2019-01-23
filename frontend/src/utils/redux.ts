export declare type MinimalAction = {
  type: string;
};

export declare type Action = {
  payload: any;
  type: string;
  error?: any;
  meta?: {
    schema: any;
  };
};

export const createReducer = (initialState: any, handlers: {}) =>
  (state = initialState, actionC: MinimalAction | Action) => {
    if (Object.prototype.hasOwnProperty.call(handlers, actionC.type)) {
      return handlers[actionC.type](state, actionC);
    }
    return state;
  };

export const initSagas = (sagas: any, sagaMiddleware: any): void => {
  Object.values(sagas).forEach(sagaMiddleware.run.bind(sagaMiddleware));
};

export const bindActionToPromise = (dispatch: any, actionCreator: any) => (payload) => {
  return new Promise((resolve, reject) => dispatch(actionCreator({ ...payload, resolve, reject })));
};
