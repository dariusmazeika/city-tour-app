import reduxSagaTesting from 'redux-saga-testing';
import { ChangeLanguagePayload } from './localization.types';
import { changeLanguageSaga } from './localization.sagas';
import { changeLanguage } from './localization.actions';
import { setCookie } from '../../utils/cookies';
import { Cookies } from '../../config/constants';

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
