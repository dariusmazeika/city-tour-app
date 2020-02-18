import axios from 'axios';

import { LocalStorage } from '@Config/constants';
import { getFromLocalStorage } from '@Utils/localStorage';

const API_BASE_URL = '';
function getDefaultHeaders() {

  const token = getFromLocalStorage(LocalStorage.userToken);
  return {
    Accept: 'application/json',
    Authorization: token ? `Token ${token}` : '',
  };
}

async function callApi(options: object) {
  const result = await axios({
    ...options,
    baseURL: API_BASE_URL,
    headers: getDefaultHeaders(),
  });
  return result.data;
}

export function callGet(url: string) {
  return callApi({
    url,
    method: 'GET',
  });
}

export function callPost(url: string, data: any) {
  return callApi({
    url,
    data,
    method: 'POST',
  });
}
export function callUpdate(url: string, data: any) {
  return callApi({
    url,
    data,
    method: 'PUT',
  });
}
export function callDelete(url: string) {
  return callApi({
    url,
    method: 'DELETE',
  });
}
export function callPatch(url: string) {
  return callApi({
    url,
    method: 'PATCH',
  });
}
