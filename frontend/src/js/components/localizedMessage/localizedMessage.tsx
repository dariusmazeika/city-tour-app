import classnames from 'classnames';
import * as React from 'react';
import { connect } from 'react-redux';

import { getCurrentLanguage } from '@Store/localization/localization.selector';
import { RootState } from '@Store/reducers';

import { getMessageKeyTranslation } from '@Config/appConfig';
export interface LocalizedMessageComponentProps {
  msg: string;
  html?: boolean;
  className?: string;
  params?: {
    key: string,
    value: string,
  };
}
export interface LocalizedMessageStateProps {
  currentLanguage: string;

}
export class LocalizedMessage extends React.PureComponent<LocalizedMessageComponentProps & LocalizedMessageStateProps, {}> {
  render() {
    const { params, html = false, msg, className, currentLanguage } = this.props;
    let translatedMessage = getMessageKeyTranslation(msg, currentLanguage);

    if (params) {
      Object.keys(params).forEach((key) => {
        translatedMessage = translatedMessage.replace(`{{${key}}}`, params[ key ]);
      });
    }
    if (html) {
      return (
        <span dangerouslySetInnerHTML={{ __html: translatedMessage }} className={classnames('html-content', className)} />
      );
    }
    return (
      <span className={className}>{translatedMessage}</span>
    );
  }
}

export default connect<LocalizedMessageStateProps, {}, LocalizedMessageComponentProps>((state: RootState) => {
  return {
    currentLanguage: getCurrentLanguage(state),
  };
})(LocalizedMessage);
