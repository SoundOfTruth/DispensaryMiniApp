export interface BaseStore {
  limit: number;
  count: number;
  setLimit: CallableFunction;
  loadById: CallableFunction;
  loadList: CallableFunction;
}
