import * as React from 'react';
import classnames from 'classnames';
import ErrorDisplay from './errorDisplay';
import { WrappedFieldMetaProps } from 'redux-form';

export interface TextInputProps {
  className?: string;
  label?: string;
  showError?: boolean;
  name?: boolean;
  meta: WrappedFieldMetaProps;
}

const formField: React.FunctionComponent<any> = (props) => {
  const {
        className = '',
        children = [],
        name = null,
        showError = true,
        meta: { touched, error = null, submitFailed },
    } = props;
  const hasError = touched && error && submitFailed;
  return (
    <div className={classnames('form-field', name && `form-field-${name}`, className, hasError && 'error')}>
        <div className="form-input">{children}</div>
        {showError && hasError && <ErrorDisplay msg={error}/>}
    </div>
  );
};

export default formField;
