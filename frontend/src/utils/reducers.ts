import { Action, AsyncActionCreators } from 'typescript-fsa';
import * as dotProp from 'dot-prop-immutable';

export const singleItemReducerInitialState = {
  item: null,
  isFetching: false,
};
export const singleItemReducer = (actionType: AsyncActionCreators<{}, any, {}>, stateName: string) => {
  return {
    [actionType.started.type]: (state: any) => {
      return dotProp.set(state, `${stateName}.isFetching`, true);
    },
    [actionType.done.type]: (state, action: any) => {
      return dotProp.set(state, stateName, { isFetching: false, item: action.payload.result });
    },
    [actionType.failed.type]: (state) => {
      return dotProp.set(state, `${stateName}.isFetching`, false);
    },
  };
};
