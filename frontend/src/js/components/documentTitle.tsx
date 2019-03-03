import * as React from 'react';
import DocumentTitle from 'react-document-title';
import { connect } from 'react-redux';

import { getCurrentLanguage } from '@Store/localization/localization.selector';
import { RootState } from '@Store/reducers';

import { getMessageKeyTranslation } from '@Config/appConfig';

export interface DocumentTitleComponentProps {
  title: string;
  children: any;

}
export interface DocumentTitleStateProps {
  currentLanguage: string;

}

export class LocalizedMessage extends React.PureComponent<DocumentTitleComponentProps & DocumentTitleStateProps, {}> {
  componentDidMount() {
    window.scrollTo(0, 0);
  }

  buildTitle(text) {
    const root = getMessageKeyTranslation('page_title', this.props.currentLanguage) || '';
    if (text) {
      return `${`${text.charAt(0).toUpperCase()}${text.slice(1)}`} | ${root || ''}`;
    }
    return root;
  }
  render() {
    const { children, title, ...restprops } = this.props;
    return (
      <DocumentTitle title={this.buildTitle(getMessageKeyTranslation(title, this.props.currentLanguage))} {...restprops } >
        { children }
      </DocumentTitle>
    );
  }
}

export default connect<DocumentTitleStateProps, {}, DocumentTitleComponentProps>((state: RootState) => {
  return {
    currentLanguage: getCurrentLanguage(state),
  };
})(LocalizedMessage);
