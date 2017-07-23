import React, {Component} from 'react';
import {RouteWithSubRoutes} from '../utils/router-utils';
import routes from '../routes/index';

export default class extends Component {
    render() {
        return (
            <div>
                {routes.map((route, i) => (<RouteWithSubRoutes key={i} {...route}/>))}
            </div>
        );
    }
}
