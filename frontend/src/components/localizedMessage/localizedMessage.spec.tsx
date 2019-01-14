import { shallow } from 'enzyme/build';
import * as React from 'react';
import LocalizedMessage from './localizedMessage';

describe('<LocalizedMessage />', () => {

  it('Shoud render key <LocalizedMessage />', () => {
    const key = 'msg_key';
    const wrapper = shallow(
            <LocalizedMessage msg={key}/>,
    );

    const text = wrapper.find('span').text();
    expect(text).toEqual(key);

  });

});
