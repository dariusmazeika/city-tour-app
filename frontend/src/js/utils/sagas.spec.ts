import { FORM_ERROR } from 'final-form';
import reduxSagaTesting from 'redux-saga-testing';
import { call, put } from 'redux-saga/effects';
import typescriptFsa from 'typescript-fsa';

import { PayloadWithPromises } from '@Utils/types';

import { callPost, callUpdate } from './api';
import { handleFormAction, handleFormSubmit, handleFormUpdate } from './sagas';

class FetchError extends Error {
  constructor(message: string, response?: object, status?: number) {
    super(message);
    this.message = message;
    this.response = response;
    this.status = status;
  }

  response?: object;

  status?: number;
}
const sendError = (data: { response?: string; non_field_errors?: string; message?: string }) => {
  return new FetchError('Error', { data });
};
const actionCreator = typescriptFsa();

export interface PayloadType{
  email: string;
  password: string;
}
interface PayloadTypeWithPromises extends PayloadType, PayloadWithPromises {}
interface ResponseType {
  token: string;
}
export const testAction = actionCreator.async<PayloadTypeWithPromises, ResponseType>('TestAction');

const URL = 'my-url';
const ACTION_PAYLOAD_DATA = {
  email: 'myemail@mail.com',
  password: 'helloPassword',
};
const ACTION_PAYLOAD: PayloadTypeWithPromises = {
  ...ACTION_PAYLOAD_DATA,
  resolve: () => { },
  reject: () => { },
};
const ACTION_RESPONSE = {
  token: 'hello',
};

describe('Sagas utils', () => {

  describe('handleFormAction(): Success', () => {

    const it = reduxSagaTesting(handleFormAction(URL, testAction.started(ACTION_PAYLOAD), testAction, callPost));
    it('Should call action', (result: any) => {
      expect(result).toEqual(call(callPost, URL, ACTION_PAYLOAD_DATA));
      return ACTION_RESPONSE;
    });

    it('Should resolve promise', (result: any) => {
      expect(result).toEqual(call(ACTION_PAYLOAD.resolve, ACTION_RESPONSE));
    });

    it('Should push SUCCESS action', (result: any) => {
      expect(result).toEqual(put(testAction.done({ result: ACTION_RESPONSE, params: ACTION_PAYLOAD })));
    });

  });

  describe('handleFormAction(): error', () => {
    const ERROR_RESPONSE_DATA = { response: 'this is an error' };
    const it = reduxSagaTesting(handleFormAction(URL, testAction.started(ACTION_PAYLOAD), testAction, callPost));
    it('Should call action', (result: any) => {
      expect(result).toEqual(call(callPost, URL, ACTION_PAYLOAD_DATA));
      return sendError(ERROR_RESPONSE_DATA);
    });

    it('Should reject promise', (result: any) => {
      expect(result).toEqual(call(ACTION_PAYLOAD.reject, ERROR_RESPONSE_DATA));
    });

    it('Should REJECT ACTION', (result: any) => {
      expect(result).toEqual(put(testAction.failed({ error: ERROR_RESPONSE_DATA, params: ACTION_PAYLOAD })));
    });

  });
  //
  describe('handleFormAction(): error with not field errors', () => {

    const ERROR_RESPONSE = { non_field_errors: 'Unable to save' };

    const it = reduxSagaTesting(handleFormAction(URL, testAction.started(ACTION_PAYLOAD), testAction, callPost));
    it('Should call action', (result: any) => {
      expect(result).toEqual(call(callPost, URL, ACTION_PAYLOAD_DATA));
      return sendError(ERROR_RESPONSE);
    });

    it('Should reject promise', (result: any) => {
      expect(result).toEqual(call(ACTION_PAYLOAD.reject, { [ FORM_ERROR ]: ERROR_RESPONSE.non_field_errors }));
    });

    it('Should REJECT ACTION', (result: any) => {
      expect(result).toEqual(put(testAction.failed({
        error: {
          [ FORM_ERROR ]: ERROR_RESPONSE.non_field_errors,
        },
        params: ACTION_PAYLOAD,
      })));
    });

  });
  //
  describe('handleFormAction(): error with message', () => {

    const ERROR_RESPONSE = { message: 'Unable to save' };

    const it = reduxSagaTesting(handleFormAction(URL, testAction.started(ACTION_PAYLOAD), testAction, callPost));
    it('Should call action', (result: any) => {
      expect(result).toEqual(call(callPost, URL, ACTION_PAYLOAD_DATA));
      return sendError(ERROR_RESPONSE);
    });

    it('Should reject promise', (result: any) => {
      expect(result).toEqual(call(ACTION_PAYLOAD.reject, { message: ERROR_RESPONSE.message }));
    });

    it('Should REJECT ACTION', (result: any) => {
      expect(result).toEqual(put(testAction.failed({ error: { message: ERROR_RESPONSE.message },
        params: ACTION_PAYLOAD })));
    });

  });
  //
  describe('handleFormSubmit(): Success', () => {

    const it = reduxSagaTesting(handleFormSubmit(URL, testAction.started(ACTION_PAYLOAD), testAction));
    it('Should call handleFormAction', (result: any) => {
      expect(result).toEqual(handleFormAction(URL, testAction.started(ACTION_PAYLOAD), testAction, callPost));
    });

  });

  describe('handleFormUpdate(): Success', () => {

    const it = reduxSagaTesting(handleFormUpdate(URL, testAction.started(ACTION_PAYLOAD), testAction));
    it('Should call handleFormAction', (result: any) => {
      expect(result).toEqual(handleFormAction(URL, testAction.started(ACTION_PAYLOAD), testAction, callUpdate));
    });

  });

});
