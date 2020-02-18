import { Dispatch } from 'redux';

export type MapT<V> = { [ key: string ]: V };
export type HOC<PWrapped, PHoc> = React.ComponentClass<PWrapped & PHoc> | React.FunctionComponent<PWrapped & PHoc>;
export type PayloadWithPromises = {
  resolve: (argument: any) => void;
  reject: (argument: any) => void;
};

export type LoadableItem = {
  item: any;
  isFetching: boolean;
};


export type BindActionToPromiseActionType = (values: Partial<{}>, dispatch: Dispatch<any>, props: {}) => Promise<any>;
export interface ActionErrorType {
  error: {status: number; response: object};
}
