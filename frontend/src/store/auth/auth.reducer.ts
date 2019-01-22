import { Action } from 'typescript-fsa';
import { login, logout, getUserData } from './auth.actions';
import { createReducer } from '../../utils/redux';
import * as dotProp from 'dot-prop-immutable';
import { UserAuth, UserData } from './auth.types';
import { singleItemReducerInitialState, singleItemReducer } from '../../utils/reducers';
export type AuthState = {
  readonly user: UserAuth | null,
  readonly userData: UserData,
};

export const initialState: AuthState = {
  user: null,
  userData: singleItemReducerInitialState,
};

const authReducer = createReducer(initialState, {
  [login.started.type]: (state: AuthState) => {
    return dotProp.set(state, 'user', null);
  },
  [login.done.type]: (state: AuthState, action: Action<{ result: UserAuth }>) => {
    const user = action.payload.result;
    return dotProp.set(state, 'user', user);
  },
  [logout.started.type]: (state: AuthState) => {
    return dotProp.set(state, 'user', null);
  },
  ...singleItemReducer(getUserData, 'userData'),
});
export default authReducer;
