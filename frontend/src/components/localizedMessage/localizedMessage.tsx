import * as React from 'react';

export interface LocalizedMessageProps {
  msg: string;
  html?: boolean;
  currentLanguage?: string;
  params?: {
    key: string,
    value: string,
  };
}

const localizedMessage: React.FunctionComponent<LocalizedMessageProps> = ({ params, html, msg }) => {

  let translatedMessage = msg;

  if (params) {
    Object.keys(params).forEach((key) => {
      translatedMessage = translatedMessage.replace(`{{${key}}}`, params[key]);
    });
  }
  if (html) {
    return (
            <span dangerouslySetInnerHTML={{ __html: translatedMessage }} className="html-content"/>
    );
  }
  return (
        <span>{translatedMessage}</span>
  );
};

export default localizedMessage;
