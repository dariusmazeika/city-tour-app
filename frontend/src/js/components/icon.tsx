import * as React from 'react';
import classnames from 'classnames';

const sizes = {
  xs: {
    width: 10,
    height: 10,
  },
  ss: {
    width: 19,
    height: 19,
  },
  s: {
    width: 24,
    height: 24,
  },
  sm: {
    width: 30,
    height: 30,
  },
  m: {
    width: 55,
    height: 55,
  },
  mm: {
    width: 42,
    height: 42,
  },
  l: {
    width: 70,
    height: 70,
  },
  auto: {
    width: '100%',
    height: '100%',
  },
};
export interface IconProps {
  icon: string;
  size: string;
  className?: string;
  spin?: boolean;
  onClick?: () => void;

}
const iconComponent: React.FunctionComponent<IconProps> = (props) => {
  const { icon, size = 'm', className = null, spin = false, ...restprops } = props;

  const IC = require(`../../images/icons/${icon}.svg`);
  return <IC {...sizes[size]} {...restprops}
             className={classnames('icon', `icon-${size}`, `icon-${icon}`, { 'icon-spin': !!spin }, className)} />;
};
export default iconComponent;
