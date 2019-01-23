import * as React from 'react';
import FormField from './formField';
import { WrappedFieldProps } from 'redux-form';

// TODO https://github.com/DefinitelyTyped/DefinitelyTyped/issues/26253#
export interface TextInputProps extends WrappedFieldProps{
  placeholder?: string;
  disabled: boolean;
  type: string;
  label: string;
  showError: boolean;
}

const textInput: React.FunctionComponent<any> = ({ input, label, type, meta, showError, disabled = false, placeholder }) => {
  return (
        <FormField label={label} meta={meta} showError={showError}>
        <input
            {...input}
            placeholder={placeholder}
            disabled={disabled}
            type={type}
            autoComplete="off"
            className={input.value ? 'with-value' : ''}
        />
        </FormField>
  );
};

export default textInput;
