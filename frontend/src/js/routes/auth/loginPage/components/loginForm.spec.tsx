import { mount, render, shallow } from 'enzyme';
import * as React from 'react';
import { Provider } from 'react-redux';
import { StaticRouter } from 'react-router';
import { create } from 'react-test-renderer';
import configureMockStore from 'redux-mock-store';

import initialTestingState from '../../../../__mocks__/initialTestingState';
import { Forms } from '../../../../config/constants';

import LoginForm from './loginForm';
describe('<LoginForm />', () => {
  let store;
  beforeAll(() => {
    store = configureMockStore([])({
      ...initialTestingState,
      form: {
        [Forms.loginForm]: {
          values: {
          },
        },
      }});
  });
  it('should match snapshot', () => {
    const onSubmitMock = jest.fn();
    const wrapper = create(<StaticRouter location="" context={{}}><Provider store={store}>
            <LoginForm  onSubmit={onSubmitMock}/>
    </Provider></StaticRouter>);
    const tree = wrapper.toJSON();
    expect(tree).toMatchSnapshot();
  });

  it('should simulate click', () => {
    const onSubmitMock = jest.fn();
    const wrapper = shallow(<StaticRouter location="" context={{}}><Provider store={store}>
            <LoginForm  onSubmit={onSubmitMock}/>
    </Provider></StaticRouter>);
    expect(wrapper.find(LoginForm).length).toEqual(1);
    wrapper.find(LoginForm).simulate('submit');
    expect(onSubmitMock).toBeCalled();
  });
});
