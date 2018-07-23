import React from 'react';
import PropTypes from 'prop-types';
import RouterUtils from '../utils/router-utils';
import { Switch } from 'react-router';
import { Redirect } from 'react-router-dom';

export const CoreLayout = ({ routes }) => (
    <div className="container text-center">
        <div className="page-layout">
            <Switch>
                {routes.map((route, i) => (<RouterUtils.RouteWithSubRoutes key={i} {...route}/>))}
                <Redirect to="/"/>
            </Switch>
        </div>
    </div>
);
CoreLayout.propTypes = {
    children: PropTypes.oneOfType([
        PropTypes.arrayOf(PropTypes.node),
        PropTypes.node
    ]),
    routes: PropTypes.array
};

export default CoreLayout;
