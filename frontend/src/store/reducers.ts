import { combineReducers } from 'redux';
import authReducer, { AuthState } from './auth/auth.reducer';
import { reducer as formReducer } from 'redux-form';
import { connectRouter } from 'connected-react-router';

export interface RootState {
  router: any;
  auth: AuthState;
  form: any;
}

const rootReducer = history => combineReducers<RootState>({
  router: connectRouter(history),
  auth: authReducer,
  // entities,
  form: formReducer,
});
export default rootReducer;
