import { Action } from 'typescript-fsa';
import { login, logout } from './auth.actions';
import { createReducer } from '../../utils/redux';
import * as dotProp from 'dot-prop-immutable';
import { UserAuth } from './auth.types';

export type AuthState = {
  readonly user: UserAuth | null,
};

export const initialState: AuthState = {
  user: null,
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
});
export default authReducer;
