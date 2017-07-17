import React from 'react';
import PropTypes from 'prop-types';
import {RouteWithSubRoutes} from '../utils/router-utils';

export const CoreLayout = ({routes}) => (
    <div className="container text-center">
        <div>
            HEADER
        </div>
        <div className="page-layout__viewport">
            {routes.map((route, i) => (<RouteWithSubRoutes key={i} {...route}/>))}
        </div>
        <div>FOOTER</div>
    </div>
);
CoreLayout.propTypes = {
    children: PropTypes.node
};

export default CoreLayout;
