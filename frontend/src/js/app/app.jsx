import React, {Component} from 'react';
import {BrowserRouter as Router} from 'react-router-dom';
import {RouteWithSubRoutes} from '../utils/router-utils';
import routes from '../routes/index';

export default class extends Component {
    render() {
        return (
            <Router>
                <div>
                    {routes.map((route, i) => (<RouteWithSubRoutes key={i} {...route}/>))}
                </div>
            </Router>
        );
    }
}
