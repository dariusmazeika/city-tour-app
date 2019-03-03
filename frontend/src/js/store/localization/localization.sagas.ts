import { all, takeEvery } from 'redux-saga/effects';
import { Action } from 'typescript-fsa';

import { Cookies } from '../../config/constants';
import { setCookie } from '../../utils/cookies';

import { changeLanguage } from './localization.actions';
import { ChangeLanguagePayload } from './localization.types';

export function* changeLanguageSaga(action: Action<ChangeLanguagePayload>) {
  yield setCookie(Cookies.defaultLang, action.payload.lang);
}

export default function* languageSagas() {
  yield all([
    takeEvery(changeLanguage.type, changeLanguageSaga),
  ]);
}
