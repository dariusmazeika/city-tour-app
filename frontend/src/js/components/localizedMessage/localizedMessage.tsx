import classnames from 'classnames';
import * as React from 'react';

import { getMessageKeyTranslation } from '@Config/appConfig';
import { LocaleContextType, withLocaleContext } from '@Config/localeContext';

export interface LocalizedMessageComponentProps {
  msg: string;
  html?: boolean;
  className?: string;
  params?: {
    key: string,
    value: string,
  };
}
export const localizedMessage: React.FunctionComponent<LocalizedMessageComponentProps & LocaleContextType> = (props) => {
  const { params, html = false, msg, className, localeContext } = props;
  let translatedMessage = getMessageKeyTranslation(msg, localeContext);

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

};
export default withLocaleContext(localizedMessage);
