import { combineReducers } from 'redux';
import authReducer, { AuthState } from './auth/auth.reducer';
import localizationReducer from './localization/localization.reducer';
import { reducer as formReducer } from 'redux-form';
import { connectRouter } from 'connected-react-router';
import { LocalizationState } from './localization/localization.types';

export interface RootState {
  router: any;
  auth: AuthState;
  localization: LocalizationState;
  form: any;
}

const rootReducer = history => combineReducers<RootState>({
  router: connectRouter(history),
  localization: localizationReducer,
  auth: authReducer,
  // entities,
  form: formReducer,
});
export default rootReducer;
