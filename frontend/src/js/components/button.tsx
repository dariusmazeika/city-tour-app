import classnames from 'classnames';
import * as React from 'react';
import { Link } from 'react-router-dom';

import Icon from './icon';

export interface ButtonProps {
  type?: string;
  aria: string;
  to?: any;
  className?: string;
  submit: boolean;
  loading?: boolean;
  disabled?: boolean;
  children: object | string;
}

const buttonComponent: React.FunctionComponent<ButtonProps> = (props) => {
  const {
    aria = 'button',
    type = 'primary',
    to = null,
    className = '',
    submit = false,
    loading = false,
    children = null,
    ...restprops
  } = props;

  const btnprops = {
    ...restprops,
    className: classnames(className, 'btn', `btn-${type}`, { 'btn-loading': loading }),
    type: submit
      ? 'submit'
      : 'button',
  };

  if (to) {
    return (
      <Link aria-label={aria} to={to} {...btnprops}>
        {children}
      </Link>);
  }
  if (loading) {
    return (
      <button aria-label={aria} {...btnprops} >
        <Icon icon="spinner" spin={true} size="sm" />
      </button>);
  }

  return (
    <button aria-label={aria} {...btnprops}>
      {children}
    </button>
  );
};

export default buttonComponent;
