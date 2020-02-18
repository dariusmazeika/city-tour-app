import * as React from 'react';

import LocalizedMessage from '@Components/localizedMessage';

export interface ErrorDisplayProps {
  msg: string | string[] | { message: string };
}

const parseMessageToDisplay = (msg: string | string[] | { message: string }) => {
  if (typeof msg === 'string') {
    return msg;
  }

  if (Array.isArray(msg)) {
    return msg[ 0 ];
  }

  return msg.message;
};

const errorDisplay: React.FunctionComponent<ErrorDisplayProps> = ({ msg }) => {
  const msgToDispay = parseMessageToDisplay(msg);

  return (
    <div className="error-msg">
      <LocalizedMessage msg={msgToDispay} />
    </div>
  );
};

export default errorDisplay;
