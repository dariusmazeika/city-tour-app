import { RouteInfo } from '../appRoutes';

import LoginPageContainer from './loginPage/loginPageContainer';
import RegisterPageContainer from './registerPage/registerPageContainer';

const routes: RouteInfo[] = [
  {
    path: '/login',
    component: LoginPageContainer,
    title: 'msg_page_login',
  },
  {
    path: '/register',
    component: RegisterPageContainer,
    title: 'msg_page_register',
  },
];

export default routes;
