import { shallow } from 'enzyme';
import * as React from 'react';
import { Provider } from 'react-redux';
import { StaticRouter } from 'react-router';
import { create } from 'react-test-renderer';
import configureMockStore from 'redux-mock-store';

import initialTestingState from '@Mocks/initialTestingState';

import LoginForm from './LoginForm';

describe('<LoginForm />', () => {
  let store: any;
  beforeAll(() => {
    store = configureMockStore([])({
      ...initialTestingState,
    });
  });
  it('should match snapshot', () => {
    const onSubmitMock = jest.fn();
    const element = (
      <StaticRouter location="" context={{}}>
        <Provider store={store}>
          <LoginForm onSubmit={onSubmitMock} />
        </Provider>
      </StaticRouter>
    );
    const wrapper = create(element);
    const tree = wrapper.toJSON();
    expect(tree).toMatchSnapshot();
  });

  it('should simulate click', () => {
    const onSubmitMock = jest.fn();
    const element = (
      <StaticRouter location="" context={{}}>
        <Provider store={store}>
          <LoginForm onSubmit={onSubmitMock} />
        </Provider>
      </StaticRouter>
    );
    const wrapper = shallow(element);
    expect(wrapper.find(LoginForm).length).toEqual(1);
    wrapper.find(LoginForm).simulate('submit');
    expect(onSubmitMock).toBeCalled();
  });
});
