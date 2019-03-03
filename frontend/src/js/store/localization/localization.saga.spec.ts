import reduxSagaTesting from 'redux-saga-testing';

import { Cookies } from '../../config/constants';
import { setCookie } from '../../utils/cookies';

import { changeLanguage } from './localization.actions';
import { changeLanguageSaga } from './localization.sagas';
import { ChangeLanguagePayload } from './localization.types';

describe('Localization sagas', () => {

  describe('changeLanguageSaga(): Request path', () => {

    const actionPayload: ChangeLanguagePayload = {
      lang: 'be',
    };

    const it = reduxSagaTesting(changeLanguageSaga(changeLanguage(actionPayload)));
    it('Should set cookie', (result) => {
      expect(result).toEqual(setCookie(Cookies.defaultLang, actionPayload.lang));
    });
  });
});
