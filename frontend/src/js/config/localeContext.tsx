import * as React from 'react';

import { getDefaultLanguage } from './appConfig';

export interface LocaleContextType {
  localeContext: string;
}
const localeContext = React.createContext(getDefaultLanguage());

/* tslint:disable: variable-name */
export const AppContextProvider = localeContext.Provider;

export const AppContextConsumer = localeContext.Consumer;

export const withLocaleContext = (Component: any) => {
  return function ComponentBoundWithAppContext(props: any) {
    return (
      <AppContextConsumer>
        {appContext => <Component {...props} localeContext={appContext} />}
      </AppContextConsumer>
    );
  };

};
/* tslint:enable */
