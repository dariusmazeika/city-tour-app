import * as React from 'react';
import { Forms } from '../../../../config/constants';
import { Field, reduxForm, InjectedFormProps, FormSubmitHandler } from 'redux-form';
import TextInput from '../../../../components/form/textInput';
import ErrorDisplay from '../../../../components/form/errorDisplay';
interface LoginFormData {
  email?: string;
  password: string;
}
interface TestFormComponentProps {
  onSubmit: FormSubmitHandler;
}

type InjectedProps = InjectedFormProps<{}, TestFormComponentProps>;

const loginForm: React.FunctionComponent<TestFormComponentProps & InjectedProps> =
  ({ handleSubmit, onSubmit, submitting, error }) => {
    return (
    <form onSubmit={handleSubmit(onSubmit)} className="form" noValidate={true}>
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

export default reduxForm({
  form: Forms.loginForm,

})(loginForm);
