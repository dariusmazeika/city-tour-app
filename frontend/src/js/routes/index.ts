import { privateRoutes, publicRoutes, RouteInfo } from './appRoutes';
import { authenticatedOnlyComponent } from '../utils/router';

export default [...publicRoutes, ...privateRoutes.map((item: RouteInfo) => {
  return {
    ...item, component: authenticatedOnlyComponent(item.component),
  };
}),
];

// export default [...publicRoutes, ...privateRoutes];
