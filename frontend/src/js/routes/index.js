import CoreLayout from '../layout/core-layout';
import HomePage from '../containers/HomePage';
import RouterUtils from '../utils/router-utils';

export default [ {
    path: '/',
    component: CoreLayout,
    routes: [
        RouterUtils.ReactRoute({
            path: '/',
            exact: true,
            component: HomePage,
            routes: []
        })
    ]
} ];
