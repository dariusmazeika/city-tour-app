import React, { useState } from 'react';
import { FieldRenderProps } from 'react-final-form';

import Icon, { IconSizes } from '../../icon';
import FormField from '../formField';

export interface TextInputProps {
  placeholder?: string;
  required?: boolean;
  disabled: boolean;
  type: string;
  label: string;
  showError: boolean;
  className?: string;
  actions: object;
  children: any;
}

const TextInput: React.FunctionComponent<FieldRenderProps<string, HTMLElement> & TextInputProps & any>
  = ({ input, label, type, meta, showError, disabled, className, placeholder, required, children }) => {

    const [ inputType, changeInputType ] = useState(type);

    const toggleVisibility = () => inputType === 'password' ? changeInputType('text') : changeInputType('password');
    return (
      <FormField className={className} label={label} meta={meta} showError={showError} required={required}>
        <input
          {...input}
          aria-label={placeholder}
          placeholder={placeholder}
          disabled={disabled}
          type={inputType}
          autoComplete="off"
          className={input.value ? 'with-value' : ''}
        />
        {children}
        {type === 'password' && (
          <Icon
            onClick={toggleVisibility}
            size={IconSizes.ss}
            icon={inputType === 'password' ? 'eye' : 'eye-disabled'}
            className="form__input__svg"
          />
        )}
      </FormField>
    );

  };
export default TextInput;
