import React, {Component} from 'react';
import {
    BrowserRouter as Router,
    Route,
} from 'react-router-dom'
import {RouteWithSubRoutes} from '../utils/router_utils';
import routes from '../routes/index';

export default class extends Component {
    render() {
        return (
            <Router>
                <div>
                    {routes.map((route, i) => (
                        <RouteWithSubRoutes key={i} {...route}/>
                    ))}
                </div>
            </Router>
        );
    }
}

