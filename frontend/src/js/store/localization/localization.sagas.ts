import { all, takeEvery } from 'redux-saga/effects';
import { Action } from 'typescript-fsa';

import { Cookies } from '@Config/constants';

import { setCookie } from '@Utils/cookies';

import { changeLanguage } from './localization.actions';
import { ChangeLanguagePayload } from './localization.types';

export function* changeLanguageSaga(action: Action<ChangeLanguagePayload>) {
  const { lang } = action.payload;
  yield setCookie(Cookies.defaultLang, lang);
  location.reload();
}

export function* languageSagas() {
  yield all([
    takeEvery(changeLanguage.type, changeLanguageSaga),
  ]);
}
