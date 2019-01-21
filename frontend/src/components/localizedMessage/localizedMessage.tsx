import * as React from 'react';
import classnames from 'classnames';
import { connect } from 'react-redux';
import { RootState } from '../../store/reducers';
import { getMessageKeyTranslation } from '../../config/appConfig';
import { getCurrentLanguage } from '../../store/localization/localization.selector';
export interface LocalizedMessageProps {
  msg: string;
  html?: boolean;
  currentLanguage: string;
  className?: string;
  params?: {
    key: string,
    value: string,
  };
}
export class LocalizedMessage extends React.PureComponent<LocalizedMessageProps, {}> {
  render() {
    const { params, html, msg, className, currentLanguage } = this.props;
    let translatedMessage = getMessageKeyTranslation(msg, currentLanguage);

    if (params) {
      Object.keys(params).forEach((key) => {
        translatedMessage = translatedMessage.replace(`{{${key}}}`, params[key]);
      });
    }
    if (html) {
      return (
        <span dangerouslySetInnerHTML={{ __html: translatedMessage }} className={classnames('html-content', className)}/>
      );
    }
    return (
      <span>{translatedMessage}</span>
    );
  }
}

export default connect((state: RootState) => {
  return {
    currentLanguage: getCurrentLanguage(state),
  };
})(LocalizedMessage);
