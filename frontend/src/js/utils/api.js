import fetch from 'isomorphic-fetch';
import {
    Promise
} from 'es6-promise';
import {
    getCookie
} from '../utils/cookies';

function addHeaders(options) {
    let headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    };

    const csrftoken = getCookie('csrftoken');
    if (csrftoken) {
        headers['X-CSRFToken'] = csrftoken;
    }

    return { ...options,
        headers: headers,
        credentials: 'same-origin',
        mode: 'cors'
    };
}

function callApi(url, options) {
    let opt = addHeaders(options);
    return fetch(url, opt).then((response) => {

        const contentType = response.headers.get('content-type');
        const isJson = contentType && contentType.indexOf('application/json') >= 0;

        if (response.status >= 200 && response.status < 300) {
            return isJson ? Promise.resolve(response.json()) : Promise.resolve(response.text());
        }
        const error = new Error(response.statusText || response.status);
        if (isJson) {
            return response.json().then((json) => {
                error.response = json;
                error.status = response.status;
                throw error;
            });
        }

        error.response = {
            message: 'Unexpected Error',
            status: response.status
        };
        throw error;
    });
}

export function callGet(url) {
    return callApi(url, {
        method: 'GET'
    });
}

export function callPost(url, data) {
    return callApi(url, {
        method: 'POST',
        body: JSON.stringify(data)
    });
}
export function callUpdate(url, data) {
    return callApi(url, {
        method: 'PUT',
        body: JSON.stringify(data)
    });
}

export function callDelete(url) {
    return callApi(url, {
        method: 'DELETE'
    });
}
