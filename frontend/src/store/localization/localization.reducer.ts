import * as dotProp from 'dot-prop-immutable';
import { Action } from 'typescript-fsa';

import { createReducer } from '../../utils/redux';
import { ChangeLanguagePayload, LocalizationState } from './localization.types';
import { getDefaultLanguage } from '../../config/appConfig';
import { changeLanguage } from './localization.actions';

export const initialState: LocalizationState = {
  currentLanguage: getDefaultLanguage(),
};

const localizationReducer = createReducer(initialState, {
  [changeLanguage.type]: (state: LocalizationState, action: Action<ChangeLanguagePayload>) => {
    return dotProp.set(state, 'currentLanguage', action.payload.lang);
  },
});
export default localizationReducer;
