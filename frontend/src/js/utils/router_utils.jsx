/**
 * Created by tomasgobionis on 6/6/17.
 */
import React from 'react'
import {
    Route,
} from 'react-router-dom'

export const RouteWithSubRoutes = (route) => (
    <Route path={route.path} render={props => (
        <route.component {...props} routes={route.routes}/>
    )}/>
)
