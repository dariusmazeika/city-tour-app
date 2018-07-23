import React from 'react';
import classnames from 'classnames';
import { Link } from 'react-router-dom';
import Icon from './icon';
import PropTypes from 'prop-types';

const Button = (props) => {
    const {
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
            : 'button'
    };

    if (to) {
        return (
            <Link to={to} {...btnprops}>
                {children}
            </Link>
        );
    }
    if (loading) {
        return (
            <button {...btnprops}>
                <Icon icon="spinner" spin={true} size="ss"/>
            </button>
        );
    }

    return (
        <button {...btnprops}>
            {children}
        </button>
    );
};

Button.propTypes = {
    type: PropTypes.string,
    to: PropTypes.string,
    className: PropTypes.string,
    submit: PropTypes.bool,
    loading: PropTypes.bool,
    children: PropTypes.oneOfType([
        PropTypes.arrayOf(PropTypes.node),
        PropTypes.node
    ])
};
export default Button;
