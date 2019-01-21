import { takeEvery, all } from 'redux-saga/effects';
import { setCookie } from '../../utils/cookies';
import { Action } from 'typescript-fsa';
import { changeLanguage } from './localization.actions';
import { ChangeLanguagePayload } from './localization.types';
import { Cookies } from '../../config/constants';

export function* changeLanguageSaga(data: Action<ChangeLanguagePayload>) {
  yield setCookie(Cookies.defaultLang, data.payload.lang);
}

export default function* languageSagas() {
  yield all([
    takeEvery(changeLanguage.type, changeLanguageSaga),
  ]);
}
