import { combineReducers } from 'redux';
import authReducer, { AuthState } from './auth/auth.reducer';
import { reducer as formReducer } from 'redux-form';

export interface RootState {
  auth: AuthState;
  form: any;
    // entities: {
    // },
}

const entities = combineReducers({ });

const rootReducer = combineReducers<RootState>({
  auth: authReducer,
    // entities,
  form: formReducer,
});

export default rootReducer;
