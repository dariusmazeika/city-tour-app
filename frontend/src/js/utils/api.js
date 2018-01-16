import {API, Cookies} from 'cct-react-commons';

function addHeaders(options) {
    let headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    };

    const csrftoken = Cookies.getCookie('csrftoken');
    if (csrftoken) {
        headers['X-CSRFToken'] = csrftoken;
    }

    return {
        ...options,
        headers: headers,
        credentials: 'same-origin',
        mode: 'cors'
    };
}

const api = new API(addHeaders);
export default api;
