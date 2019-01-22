import { Action } from 'typescript-fsa';
import { login, logout, getUserData } from './auth.actions';
import { createReducer } from '../../utils/redux';
import * as dotProp from 'dot-prop-immutable';
import { UserAuth, UserData } from './auth.types';

export type AuthState = {
  readonly user: UserAuth | null,
  readonly userData: UserData | null,
};

export const initialState: AuthState = {
  user: null,
  userData: null,
};

const authReducer = createReducer(initialState, {
  [login.started.type]: (state: AuthState) => {
    return dotProp.set(state, 'user', null);
  },
  [login.done.type]: (state: AuthState, action: Action<{ result: UserAuth }>) => {
    const user = action.payload.result;
    return dotProp.set(state, 'user', user);
  },
  [getUserData.done.type]: (state: AuthState, action: Action<{ result: UserAuth }>) => {
    const userData = action.payload.result;
    return dotProp.set(state, 'userData', userData);
  },
  [logout.started.type]: (state: AuthState) => {
    return dotProp.set(state, 'user', null);
  },
});
export default authReducer;
