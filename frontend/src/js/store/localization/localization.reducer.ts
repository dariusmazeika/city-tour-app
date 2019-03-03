import * as dotProp from 'dot-prop-immutable';
import { Action } from 'typescript-fsa';

import { getDefaultLanguage } from '../../config/appConfig';
import { createReducer } from '../../utils/redux';

import { changeLanguage } from './localization.actions';
import { ChangeLanguagePayload, LocalizationState } from './localization.types';

export const initialState: LocalizationState = {
  currentLanguage: getDefaultLanguage(),
};

const localizationReducer = createReducer(initialState, {
  [changeLanguage.type]: (state: LocalizationState, action: Action<ChangeLanguagePayload>) => {
    return dotProp.set(state, 'currentLanguage', action.payload.lang);
  },
});
export default localizationReducer;
