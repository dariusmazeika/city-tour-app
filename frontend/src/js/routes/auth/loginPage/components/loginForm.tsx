import * as React from 'react';
import { Field, reduxForm } from 'redux-form';

import { LoginFormData } from '@Store/auth/auth.types';

import { Forms } from '@Config/constants';

import { ReduxFormBase } from '@Utils/types';

import ErrorDisplay from '@Components/form/errorDisplay';
import TextInput from '@Components/form/inputs/textInput';

const loginForm: React.FunctionComponent<ReduxFormBase> =
  ({ handleSubmit, submitting, error }) => {
    return (
    <form onSubmit={handleSubmit} className="form" noValidate={true}>
     {error && <ErrorDisplay msg={error}/>}
        <div className="login-form">
          <Field name="email" component={TextInput}
             label={'msg_label_email'} type="email" placeholder={'msg_label_email'}/>
          <Field name="password" component={TextInput}
           label={'msg_label_password'} type="password" placeholder={'msg_label_password'}/>

        </div>
        {submitting && <div>Saving</div>}
        <button type="submit">Save</button>
      </form>
    );
  };

export default reduxForm<LoginFormData>({
  form: Forms.loginForm,

})(loginForm);
