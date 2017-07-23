import React, {Component} from 'react';
import {Route, Switch} from 'react-router-dom';

export const ReactRoute = (route) => {
    route.routes.map((routeItem) => {
        routeItem.path = route.path + routeItem.path;
        routeItem.auth = route.auth || routeItem.auth;
        routeItem = ReactRoute(routeItem);
        return routeItem;
    });
    return route;
};

export const RouteWithSubRoutes = (route) => (
    <Route path={route.path} exact={route.exact} render={(props) => {
        return <route.component {...props} routes={route.routes}/>;
    }}/>
);

export class DefaultRouteHandler extends Component {
    render() {
        return (
            <Switch>
                {this.props.routes.map((route, i) => (<RouteWithSubRoutes key={i} {...route}/>))}
            </Switch>
        );
    }
}
