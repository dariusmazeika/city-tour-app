import AuthRoutes from './auth/authRoutes';
import StaticRoutes from './static/staticRoutes';
import UserRoutes from './user/userRoutes';

export type RouteInfo = {
  path: string;
  component: any;
};

export const publicRoutes: RouteInfo[] = [
  ...StaticRoutes,
  ...AuthRoutes,
];

export const privateRoutes: RouteInfo[] = [
  ...UserRoutes,
];
