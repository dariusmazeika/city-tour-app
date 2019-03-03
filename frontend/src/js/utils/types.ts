import { Dispatch } from 'redux';

export type PayloadWithPromises = {
  resolve: () => void,
  reject: () => void,
};

export type LoadableItem = {
  item: any,
  isFetching: boolean,
};
export interface ReduxFormBase {
  handleSubmit: (submit) => void;
  submitting: boolean;
  error: any;
}

export type BindActionToPromiseActionType = (values: Partial<{}>, dispatch: Dispatch<any>, props: {}) => Promise<any>;
