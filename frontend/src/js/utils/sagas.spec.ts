import { SubmissionError } from 'redux-form';
import reduxSagaTesting from 'redux-saga-testing';
import { call, put } from 'redux-saga/effects';
import typescriptFsa from 'typescript-fsa';

import { callPost, callUpdate, FetchError } from './api';
import { handleFormAction, handleFormSubmit, handleFormUpdate } from './sagas';

const actionCreator = typescriptFsa();

export const testAction = actionCreator.async<{}, {}>('TestAction');

const URL = 'my-url';
const ACTION_PAYLOAD = {
  email: 'myemail@mail.com',
  password: 'helloPassword',
  resolve: () => {},
  reject: () => {},
};
const ACTION_RESPONSE = {
  token: 'hello',
};

describe('Sagas utils', () => {

  describe('handleFormAction(): Success', () => {

    const it = reduxSagaTesting(handleFormAction(URL, testAction.started(ACTION_PAYLOAD), testAction, callPost));
    it('Should call action', (result) => {
      expect(result).toEqual(call(callPost, URL, ACTION_PAYLOAD));
      return ACTION_RESPONSE;
    });

    it('Should resolve promise', (result) => {
      expect(result).toEqual(call(ACTION_PAYLOAD.resolve, ACTION_RESPONSE));
    });

    it('Should push SUCCESS action', (result) => {
      expect(result).toEqual(put(testAction.done({ result: ACTION_RESPONSE, params: ACTION_PAYLOAD })));
    });

  });

  describe('handleFormAction(): error', () => {

    const ERROR_RESPONSE = { response: 'this is an error' };

    const it = reduxSagaTesting(handleFormAction(URL, testAction.started(ACTION_PAYLOAD), testAction, callPost));
    it('Should call action', (result) => {
      expect(result).toEqual(call(callPost, URL, ACTION_PAYLOAD));
      return new FetchError('error', ERROR_RESPONSE, 404);
    });

    it('Should reject promise', (result) => {
      expect(result).toEqual(call(ACTION_PAYLOAD.reject, new SubmissionError(ERROR_RESPONSE)));
    });

    it('Should REJECT ACTION', (result) => {
      expect(result).toEqual(put(testAction.failed({ error: new SubmissionError(ERROR_RESPONSE), params: ACTION_PAYLOAD })));
    });

  });

  describe('handleFormAction(): error with not field errors', () => {

    const ERROR_RESPONSE = { response: { non_field_errors: 'Unable to save' } };

    const it = reduxSagaTesting(handleFormAction(URL, testAction.started(ACTION_PAYLOAD), testAction, callPost));
    it('Should call action', (result) => {
      expect(result).toEqual(call(callPost, URL, ACTION_PAYLOAD));
      return new FetchError('error', ERROR_RESPONSE, 404);
    });

    it('Should reject promise', (result) => {
      expect(result).toEqual(call(ACTION_PAYLOAD.reject, new SubmissionError({ _error: ERROR_RESPONSE.response.non_field_errors })));
    });

    it('Should REJECT ACTION', (result) => {
      expect(result).toEqual(put(testAction.failed({ error: new SubmissionError({ _error: ERROR_RESPONSE.response.non_field_errors }), params: ACTION_PAYLOAD })));
    });

  });

  describe('handleFormAction(): error with message', () => {

    const ERROR_RESPONSE = { response: { message: 'Unable to save' } };

    const it = reduxSagaTesting(handleFormAction(URL, testAction.started(ACTION_PAYLOAD), testAction, callPost));
    it('Should call action', (result) => {
      expect(result).toEqual(call(callPost, URL, ACTION_PAYLOAD));
      return new FetchError('error', ERROR_RESPONSE, 404);
    });

    it('Should reject promise', (result) => {
      expect(result).toEqual(call(ACTION_PAYLOAD.reject, new SubmissionError({ _error: ERROR_RESPONSE.response.message })));
    });

    it('Should REJECT ACTION', (result) => {
      expect(result).toEqual(put(testAction.failed({ error: new SubmissionError({ _error: ERROR_RESPONSE.response.message }), params: ACTION_PAYLOAD })));
    });

  });

  describe('handleFormSubmit(): Success', () => {

    const it = reduxSagaTesting(handleFormSubmit(URL, testAction.started(ACTION_PAYLOAD), testAction));
    it('Should call handleFormAction', (result) => {
      expect(result).toEqual(handleFormAction(URL, testAction.started(ACTION_PAYLOAD), testAction, callPost));
    });

  });

  describe('handleFormUpdate(): Success', () => {

    const it = reduxSagaTesting(handleFormUpdate(URL, testAction.started(ACTION_PAYLOAD), testAction));
    it('Should call handleFormAction', (result) => {
      expect(result).toEqual(handleFormAction(URL, testAction.started(ACTION_PAYLOAD), testAction, callUpdate));
    });

  });

});
