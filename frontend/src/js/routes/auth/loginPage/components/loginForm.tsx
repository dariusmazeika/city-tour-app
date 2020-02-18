import * as React from 'react';
import { ReactNode } from 'react';
import { Field, Form, FormRenderProps } from 'react-final-form';

import ErrorDisplay from '@Components/form/errorDisplay';
import TextInput from '@Components/form/inputs/textInput';
import { LoginFormData } from '@Store/auth/auth.types';

enum LoginFormFields {
  email = 'email',
  password = 'password',
}

interface LoginFormProps {
  onSubmit: (values: any) => Promise<LoginFormData>;
}

const renderForm = ({ handleSubmit, submitting, error }: FormRenderProps): ReactNode => {
  return (
    <form onSubmit={handleSubmit} className="form" noValidate={true}>
      {error && <ErrorDisplay msg={error} />}
      <div className="login-form">
        <Field
          name={LoginFormFields.email}
          component={TextInput}
          label="msg_label_email"
          type="email"
          placeholder="msg_label_email"
        />
        <Field
          name={LoginFormFields.password}
          component={TextInput}
          label="msg_label_password"
          type="password"
          placeholder="msg_label_password"
        />

      </div>
      {submitting && <div>Saving</div>}
      <button type="submit">Save</button>
    </form>
  );
};


const LoginForm: React.FC<LoginFormProps> = ({ onSubmit }) => (
  <Form
    onSubmit={onSubmit}
    initialValues={{}}
    render={renderForm}
  />
);

export default LoginForm;
