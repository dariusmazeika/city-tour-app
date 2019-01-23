import authReducer, { AuthState, initialState } from './auth.reducer';
import { login } from './auth.actions';

describe('Reducers::Auth reducer', () => {

  it('Should return the initial state', () => {
    const newState: any = {};
    const state: AuthState = authReducer(undefined, newState);
    expect(state).toEqual(initialState);
  });

  it('Should set auth info on login', () => {
    const state = authReducer(undefined, {
      type: login.done.type,
      payload: {
        params: {},
        result: {
          token: '123',
        },
      },
    });
    expect(state.user.token).toEqual('123');
  });

});
