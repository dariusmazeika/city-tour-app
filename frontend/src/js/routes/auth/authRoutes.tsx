import { RouteInfo } from '../appRoutes';

import LoginPageContainer from './loginPage/loginPageContainer';
import RegisterPageContainer from './registerPage/registerPageContainer';

const routes: RouteInfo[] = [
  {
    path: '/login',
    component: LoginPageContainer,
  },
  {
    path: '/register',
    component: RegisterPageContainer,
  },
];

export default routes;
