import { RouteInfo } from '../appRoutes';

import UserPageContainer from './userPage/userPageContainer';

const routes: RouteInfo[] = [
  {
    path: '/user',
    component: UserPageContainer,
    title: 'msg_page_user',
  },
];

export default routes;
