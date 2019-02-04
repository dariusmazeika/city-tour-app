import * as React from 'react';
import LocalizedMessage from '../localizedMessage/localizedMessage';

export interface ErrorDisplayProps {
  msg: any;
}

const errorDisplay: React.FunctionComponent<ErrorDisplayProps> = ({ msg }) => {
  let msgToDispay = msg;

  if (Array.isArray(msg)) {
    msgToDispay = msg[0];
  }
  if (msg.message) {
    msgToDispay = msg.message;
  }

  return (
      <div className="error-msg">
          <LocalizedMessage msg={msgToDispay} />
      </div>
  );
};

export default errorDisplay;
