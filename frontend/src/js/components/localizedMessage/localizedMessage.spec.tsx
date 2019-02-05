import { shallow } from 'enzyme/build';
import * as React from 'react';
import { create } from 'react-test-renderer';

import { LocalizedMessage } from './localizedMessage';

describe('<LocalizedMessage />', () => {

  it('should match snapshot', () => {
    const wrapper = create(
      <LocalizedMessage msg={'msg_key'} currentLanguage={'lt'}/>,
    );
    const tree = wrapper.toJSON();
    expect(tree).toMatchSnapshot();
  });

  it('Shoud render key <LocalizedMessage />', () => {
    const key = 'msg_key';
    const wrapper = shallow(
        <LocalizedMessage msg={key} currentLanguage={'lt'}/>,
    );

    const text = wrapper.find('span').text();
    expect(text).toEqual(key);

  });

  it('Shoud find className if one is present', () => {
    const wrapper = create(
      <LocalizedMessage msg={'msg_key'} className={'this-is-css-class'} currentLanguage={'lt'}/>,
    );
    const tree = wrapper.toJSON();
    expect(tree).toMatchSnapshot();
  });

  it('Should find a translation ', () => {
    window._app_messages = {
      lt: {
        msg_key: 'translation',
      },
    };

    const wrapper = create(
      <LocalizedMessage msg={'msg_key'} className={'this-is-css-class'} currentLanguage={'lt'}/>,
    );
    const tree = wrapper.toJSON();
    expect(tree).toMatchSnapshot();
  });

});
