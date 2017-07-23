import React from 'react';
import classnames from 'classnames';

const sizes = {
    ss: {
        width: 19,
        height: 19
    },
    s: {
        width: 24,
        height: 24
    },
    sm: {
        width: 35,
        height: 35
    },
    m: {
        width: 55,
        height: 55
    },
    mm: {
        width: 42,
        height: 42
    },
    l: {
        width: 70,
        height: 70
    }
};

export default function Icon(props) {

    const { icon, size='m', className=null, spin=false, ...restprops} = props;

    const Ic = require(`../../images/icons/${icon}.svg`);


    return <Ic {...sizes[size]} {...restprops} className={classnames('icon', `icon-${size}`, `icon-${icon}`, {'icon-spin': !!spin}, className)}/>;
}
