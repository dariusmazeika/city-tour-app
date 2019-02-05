import { fetch } from 'whatwg-fetch';

import { Cookies, LocalStorage } from '../config/constants';

import { getCookie } from './cookies';
import { getFromLocalStorage } from './localStorage';

const API_URL = '';

export class FetchError extends Error {
  constructor(message: string, response?: object, status?: number) {
    super(message);
    this.message = message;
    this.response = response;
    this.status = status;
  }
  response?: object;
  status?: number;
}

function addHeaders(options: object) {

  const headers = {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  };

  const token = getFromLocalStorage(LocalStorage.userToken);
  if (token) {
    headers['Authorization'] = `Token ${token}`;
  }

  const csrftoken = getCookie(Cookies.crfToken);
  if (csrftoken) {
    headers['X-CSRFToken'] = csrftoken;
  }

  const langCookie = getCookie(Cookies.defaultLang);
  if (langCookie) {
    headers['Content-Language'] = langCookie;
  }

  return {
    ...options,
    headers,
    mode: 'cors',
    cache: 'default',
  };
}

function callApi(url: string, options: object, isFile: boolean = false) {
  const opt = addHeaders(options);
  return fetch(`${API_URL}${url}`, opt).then((response) => {
    const contentType = response.headers.get('content-type');
    const isJson = contentType && contentType.indexOf('application/json') >= 0;

    if (response.status >= 200 && response.status < 300) {
      return isJson ? Promise.resolve(
        response.json()) : isFile ? Promise.resolve(response.blob()) : Promise.resolve(response.text(),
        );
    }

    const error = new FetchError(response.statusText || response.status, { message: 'Unexpected Error' }, response.status);

    if (isJson) {
      return response.json().then((json: any) => {
        error.response = json;
        error.status = response.status;
        throw error;
      });
    }
    throw error;
  });
}

export function callGet(url: string) {
  return callApi(url, {
    method: 'GET',
  });
}

export function callPost(url: string, data: object) {
  return callApi(url, {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export function callUpdate(url: string, data: object) {
  return callApi(url, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

export function callPatch(url: string, data: object) {
  return callApi(url, {
    method: 'PATCH',
    body: JSON.stringify(data),
  });
}

export function callDelete(url: string) {
  return callApi(url, {
    method: 'DELETE',
  });
}
