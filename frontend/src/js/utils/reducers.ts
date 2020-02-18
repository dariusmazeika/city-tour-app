import * as dotProp from 'dot-prop-immutable';
import { AsyncActionCreators } from 'typescript-fsa';

export const singleItemReducerInitialState = {
  item: null,
  isFetching: true,
};

export const multipleItemsReducerInitialState = {
  list: [],
  isFetching: true,
};

export const singleItemReducer = (actionType: AsyncActionCreators<{}, any, {}>, stateName: string) => {
  return {
    [ actionType.started.type ]: (state: any) => {
      return dotProp.set(state, `${stateName}.isFetching`, true);
    },
    [ actionType.done.type ]: (state: any, action: any) => {
      return dotProp.set(state, stateName, { isFetching: false, item: action.payload.result });
    },
    [ actionType.failed.type ]: (state: any) => {
      return dotProp.set(state, `${stateName}.isFetching`, false);
    },
  };
};

export const multipleItemsReducer = (actionType: AsyncActionCreators<{}, any, {}>, stateName: string) => {
  return {
    [ actionType.started.type ]: (state: any) => {
      return dotProp.set(state, `${stateName}.isFetching`, true);
    },
    [ actionType.done.type ]: (state: any, action: any) => {
      return dotProp.set(state, stateName, { isFetching: false, list: action.payload.result });
    },
    [ actionType.failed.type ]: (state: any) => {
      return dotProp.set(state, `${stateName}.isFetching`, false);
    },
  };
};
