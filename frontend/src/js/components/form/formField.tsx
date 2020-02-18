import classnames from 'classnames';
import * as React from 'react';
import { FieldRenderProps } from 'react-final-form';

import LocalizedMessage from '@Components/localizedMessage';

import ErrorDisplay from './errorDisplay';

export interface FormFieldProps {
  className?: string;
  label?: string;
  showError?: boolean;
  name?: boolean;
  required?: boolean;
}

const formField: React.FunctionComponent<FieldRenderProps<string, HTMLElement> & FormFieldProps & any> = (props) => {
  const {
    className = '',
    children = [],
    label,
    required = false,
    name = null,
    showError = true,
    meta: { touched, error = null, submitFailed },
  } = props;
  const hasError = touched && error && submitFailed;
  return (
    <div className={classnames('form__field', name && `form__field__${name}`, className, hasError && 'error')}>

      {label && <LocalizedMessage className="form__label" msg={label} />}
      {required && <span className="form__required"> *</span>}
      <div className="form__input">
        {children}
        {showError && hasError && <ErrorDisplay msg={error} />}
      </div>
    </div>
  );
};

export default formField;
