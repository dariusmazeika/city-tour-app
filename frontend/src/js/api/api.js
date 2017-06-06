/**
 * Created by tomasgobionis on 6/6/17.
 */
import fetch from 'isomorphic-fetch';
import {Promise} from 'es6-promise'

const API = 'http://httpbin.org';

function addHeaders(options) {
    // TODO Add auth headers and cors type here
    let headers = {
        'Content-Type': 'application/json'
    };
    return {...options, headers: headers};
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
        if (isJson)
            return response.json().then((json) => {
                error.response = json;
                throw error;
            });

        error.response = {message: 'Unexpected Error'};
        throw error;
    });
}

export function testRequest() {
    return callApi(API + '/get', { method: 'GET'});
}
