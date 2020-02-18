import classnames from 'classnames';
import * as React from 'react';

export enum IconSizes {
  xss = 'xxs',
  xs = 'xs',
  sss = 'sss',
  ss = 'ss',
  s = 's',
  sm = 'sm',
  m = 'm',
  mm = 'mm',
  mmm = 'mmm',
  l = 'l',
  auto = 'auto',
  none = 'none',
}

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
  size?: keyof typeof sizes;
  className?: string;
  spin?: boolean;
  onClick?: () => void;
}

const IconComponent: React.FunctionComponent<IconProps> = (props) => {
  const { icon, size = 'm', className = null, spin = false, ...restprops } = props;
  // eslint-disable-next-line @typescript-eslint/no-var-requires,global-require,import/no-dynamic-require
  const IC = require(`../../images/icons/${icon}.svg`);
  return (
    <IC
      {...sizes[ size ]}
      {...restprops}
      className={classnames('icon', `icon-${size}`, `icon-${icon}`, { 'icon-spin': !!spin }, className)}
    />
  );
};
export default IconComponent;
