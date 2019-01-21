import { shallow } from 'enzyme/build';
import * as React from 'react';
import LocalizedMessage from './localizedMessage';
import configureMockStore from 'redux-mock-store';
import { Provider } from 'react-redux';
import { create } from 'react-test-renderer';
import initialTestingState from '../../__mocks__/initialTestingState';

describe('<LocalizedMessage />', () => {
  let store;
  beforeAll(() => {
    store = configureMockStore()(initialTestingState);
  });

  it('should match snapshot', () => {
    const wrapper = create(<Provider store={store}>
      <LocalizedMessage msg={'msg_key'}/>
    </Provider>);
    const tree = wrapper.toJSON();
    expect(tree).toMatchSnapshot();
  });

  // it('Shoud render key <LocalizedMessage />', () => {
  //   const key = 'msg_key';
  //   const wrapper = shallow(
  //     <Provider store={store}>
  //       <LocalizedMessage msg={key}/>
  //     </Provider>,
  //   );
  //
  //   const text = wrapper.find('span').text();
  //   expect(text).toEqual(key);
  //
  // });

  // it('Shoud find className if one is present', () => {
  //   const className = 'className';
  //   const wrapper = shallow(<Provider store={store}>
  //     <LocalizedMessage msg={''} className={className}/>
  //     </Provider>,
  //   );
  //   expect(wrapper.find('span').hasClass(className)).toEqual(true);
  //
  // });

});
