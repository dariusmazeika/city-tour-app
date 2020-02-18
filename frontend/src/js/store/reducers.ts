import { connectRouter } from 'connected-react-router';
import { History } from 'history';
import { combineReducers } from 'redux';

import authReducer, { AuthState } from './auth/auth.reducer';
import localizationReducer from './localization/localization.reducer';
import { LocalizationState } from './localization/localization.types';

export interface RootState {
  router: any;
  auth: AuthState;
  localization: LocalizationState;
}

const rootReducer = (history: History) => combineReducers<RootState>({
  router: connectRouter(history),
  localization: localizationReducer,
  auth: authReducer,
});
export default rootReducer;
