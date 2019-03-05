import { RouteInfo } from '../appRoutes';

import LandingPageContainer from './landingPage/landingPageContainer';

const routes: RouteInfo[] = [
  {
    path: '/',
    component: LandingPageContainer,
    title: 'msg_page_landing',
  },
];

export default routes;
