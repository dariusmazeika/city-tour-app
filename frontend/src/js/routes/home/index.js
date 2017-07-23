import Home from './containers/home-view-container';
import {
    ReactRoute
} from '../../utils/router-utils';

export default ReactRoute({
    path: '/',
    exact: true,
    component: Home,
    routes: [

    ]
});
