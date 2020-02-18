import * as React from 'react';
import DocumentTitle from 'react-document-title';

import { getMessageKeyTranslation } from '@Config/appConfig';
import { LocaleContextType, withLocaleContext } from '@Config/localeContext';

export interface DocumentTitleComponentProps {
  title: string;
  children: any;
}

export class DocumentTitleComponent extends React.PureComponent<DocumentTitleComponentProps & LocaleContextType, {}> {
  componentDidMount() {
    window.scrollTo(0, 0);
  }

  buildTitle(text: string) {
    const root = getMessageKeyTranslation('page_title', this.props.localeContext) || '';
    if (text) {
      return `${`${text.charAt(0).toUpperCase()}${text.slice(1)}`} | ${root || ''}`;
    }
    return root;
  }

  render() {
    const { children, title, ...restprops } = this.props;
    return (
      <DocumentTitle title={this.buildTitle(getMessageKeyTranslation(title, this.props.localeContext))} {...restprops}>
        { children }
      </DocumentTitle>
    );
  }
}

export default withLocaleContext(DocumentTitleComponent);
