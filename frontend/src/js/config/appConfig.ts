import { getCookie } from '../utils/cookies';
import { Cookies } from './constants';

export function configValue(param: string) {
  return window._app_conf[param] || param;
}
export function getDefaultLanguage() {
  const cookieLanguage = getCookie(Cookies.defaultLang);
  return cookieLanguage || configValue('default_language');
}

export function getMessageKeyTranslation(msgid: string, language: string) {
  if (!language) {
    return msgid;
  }
  const languageMessages = window._app_messages[language] || {};
  return languageMessages[msgid] || msgid;
}
