import { ActionCreator } from 'redux';

import { PayloadWithPromises } from '@Utils/types';

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

export const createReducer = (initialState: any, handlers: any) =>
  (state = initialState, actionC: MinimalAction | Action) => {
    if (Object.prototype.hasOwnProperty.call(handlers, actionC.type)) {
      return handlers[ actionC.type ](state, actionC);
    }
    return state;
  };

export const initSagas = (sagas: any, sagaMiddleware: any): void => {
  Object.values(sagas).forEach(sagaMiddleware.run.bind(sagaMiddleware));
};

export function bindActionToPromise<T>(dispatch: any, actionCreator: ActionCreator<T & PayloadWithPromises>):
  (p: T) => any {
  return (payload: T) => {
    return new Promise((resolve, reject) => dispatch(actionCreator({ ...payload, resolve, reject })));
  };
}
