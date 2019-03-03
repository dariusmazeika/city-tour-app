import { authenticatedOnlyComponent } from '../utils/router';

import { privateRoutes, publicRoutes, RouteInfo } from './appRoutes';

export default [...publicRoutes, ...privateRoutes.map((item: RouteInfo) => {
  return {
    ...item, component: authenticatedOnlyComponent(item.component),
  };
}),
];

// export default [...publicRoutes, ...privateRoutes];
