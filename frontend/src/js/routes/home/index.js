import Home from './containers/home-view-container';
import RouterUtils from '../../utils/router-utils';

export default RouterUtils.ReactRoute({
    path: '/',
    exact: true,
    component: Home,
    routes: []
});
