import * as React from 'react';
import { mount, shallow, render } from 'enzyme';
import { Provider } from 'react-redux';
import { create } from 'react-test-renderer';
import LoginForm from './loginForm';
import configureMockStore from 'redux-mock-store';
import { Forms } from '../../../../config/constants';
import initialTestingState from '../../../../__mocks__/initialTestingState';

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
    const wrapper = create(<Provider store={store}>
            <LoginForm  onSubmit={onSubmitMock}/>
        </Provider>);
    const tree = wrapper.toJSON();
    expect(tree).toMatchSnapshot();
  });

  it('should simulate click', () => {
    const onSubmitMock = jest.fn();
    const wrapper = shallow(<Provider store={store}>
            <LoginForm  onSubmit={onSubmitMock}/>
        </Provider>);
    expect(wrapper.find(LoginForm).length).toEqual(1);
    wrapper.find(LoginForm).simulate('submit');
    expect(onSubmitMock).toBeCalled();
  });
});
