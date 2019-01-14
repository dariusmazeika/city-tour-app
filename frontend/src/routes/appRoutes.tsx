import AuthRoutes from './auth/authRoutes';
import StaticRoutes from './static/staticRoutes';
export type RouteInfo = {
  path: string;
  component: any;
};

const routes: RouteInfo[] = [
  ...StaticRoutes,
  ...AuthRoutes,
];
export default routes;
