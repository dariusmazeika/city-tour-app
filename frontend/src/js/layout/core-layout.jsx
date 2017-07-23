import React from 'react';
import PropTypes from 'prop-types';
import {RouteWithSubRoutes} from '../utils/router-utils';
import {Switch} from 'react-router';
import {Redirect} from 'react-router-dom';

export const CoreLayout = ({routes}) => (
    <div className="container text-center">
        <div className="page-layout__viewport">
            <Switch>
                {routes.map((route, i) => (<RouteWithSubRoutes key={i} {...route}/>))}
                <Redirect to="/"/>
            </Switch>
        </div>
    </div>
);
CoreLayout.propTypes = {
    children: PropTypes.node
};

export default CoreLayout;
