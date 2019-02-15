export type PayloadWithPromises = {
  resolve: () => void,
  reject: () => void,
};

export type LoadableItem = {
  item: any,
  isFetching: boolean,
};
