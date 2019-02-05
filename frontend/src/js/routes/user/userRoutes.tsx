import { RouteInfo } from '../appRoutes';

import UserPageContainer from './userPage/userPageContainer';

const routes: RouteInfo[] = [
  {
    path: '/user',
    component: UserPageContainer,
  },
];

export default routes;
