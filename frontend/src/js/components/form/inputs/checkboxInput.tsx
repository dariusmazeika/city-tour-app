import classnames from 'classnames';
import * as React from 'react';
import { FieldRenderProps } from 'react-final-form';

import FormField from '../formField';

export interface ChckboxInputProps {
  placeholder?: string;
  customFieldClass?: string;
  disabled: boolean;
  type: string;
  label: string;
  checked: boolean;
  showError: boolean;
}

const checkboxInput: React.FunctionComponent<FieldRenderProps<string, HTMLElement> & ChckboxInputProps & any> =
  (props) => {
    const { input, type = 'checkbox', placeholder, label, meta, customFieldClass, showError, disabled } = props;
    let checked = input.value;
    let id = customFieldClass || input.name;
    if (type === 'radio') {
      id = `${id}-${input.value}`;
      checked = null;
    }
    return (
      <FormField label="" meta={meta} showError={showError}>
        <label htmlFor={id} className="checkmark">
          {label}
          <input
            {...input}
            id={id}
            placeholder={placeholder}
            disabled={disabled}
            type={type}
            checked={checked}
            className={classnames(input.value ? 'with-value' : '', customFieldClass)}
          />
          <span className="checkmark__input" />
        </label>
      </FormField>
    );
  };

export default checkboxInput;
