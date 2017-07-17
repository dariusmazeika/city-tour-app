import React from 'react';
import {Route} from 'react-router-dom';

export const ReactRoute = (route)=>{
    route.routes.map((routeItem)=>{
        routeItem.path = route.path + routeItem.path;
        routeItem.auth = route.auth || routeItem.auth;
        routeItem = ReactRoute(routeItem);
        return routeItem;
    });
    return route;
};

export const RouteWithSubRoutes = (route) => (
    <Route path={route.path} render={(props) => {
        return <route.component {...props} routes={route.routes}/>;
    }}/>
);
