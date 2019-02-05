import classnames from 'classnames';
import * as React from 'react';
import { WrappedFieldProps } from 'redux-form';

import FormField from '../formField';

// TODO https://github.com/DefinitelyTyped/DefinitelyTyped/issues/26253#
export interface ChckboxInputProps extends WrappedFieldProps {
  placeholder?: string;
  customFieldClass?: string;
  disabled: boolean;
  type: string;
  label: string;
  checked: boolean;
  showError: boolean;
}

const checkboxInput: React.FunctionComponent<any> = (props: ChckboxInputProps) => {
  const { input, type = 'checkbox', placeholder, label, meta, customFieldClass, showError, disabled } = props;
  let checked = input.value;
  let id = customFieldClass || input.name;
  if (type === 'radio') {
    id = `${id}-${input.value}`;
    checked = null;
  }
  return (
    <FormField label={false} meta={meta} showError={showError}>
      <label htmlFor={id} className="checkmark">{label}
        <input
          {...input}
          id={id}
          placeholder={placeholder}
          disabled={disabled}
          type={type}
          checked={checked}
          className={classnames(input.value ? 'with-value' : '', customFieldClass)}
        />
        <span className="checkmark__input"></span>
      </label>
    </FormField>
  );
};

export default checkboxInput;
