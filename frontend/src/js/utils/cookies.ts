import { Cookies } from 'react-cookie';

export function getCookie(cookieName: string) {
  const cookies = new Cookies();
  return cookies.get(cookieName);
}

export function setCookie(cookieName: string, value: string|object) {
  const cookies = new Cookies();
  return cookies.set(cookieName, value);
}
