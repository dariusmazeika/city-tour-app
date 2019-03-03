import * as React from 'react';

import Icon from '../../icon';
import FormField from '../formField';

export class TextInput extends React.PureComponent<any, { inputType: string }> {
  constructor(props: any) {
    super(props);
    this.state = { inputType: props.type };
  }
  render() {
    const { input, label, type, meta, showError, disabled, placeholder } = this.props;
    const toggleVisibility = () => this.state.inputType === 'password' ? this.setState({ inputType: 'text' }) : this.setState({ inputType: 'password' });
    return (
      <FormField label={label} meta={meta} showError={showError}>
        <input
          {...input}
          aria-label={placeholder}
          placeholder={placeholder}
          disabled={disabled}
          type={this.state.inputType}
          autoComplete="off"
          className={input.value ? 'with-value' : ''}
        />
        {type === 'password' ?
          <Icon onClick={toggleVisibility} size={'ss'} icon={this.state.inputType === 'password' ? 'eye' : 'eye-disabled'}
            className="login-image" /> : null}
      </FormField>
    );
  }
}
export default TextInput;
