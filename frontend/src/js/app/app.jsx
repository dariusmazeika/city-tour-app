import React, {Component} from 'react';
import routes from '../routes/index';
import RouterUtils from '../utils/router-utils';

export default class extends Component {
    render() {
        return (
            <div>
                {routes.map((route, i) => (<RouterUtils.RouteWithSubRoutes key={i} {...route}/>))}
            </div>
        );
    }
}
