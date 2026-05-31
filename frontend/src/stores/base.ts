export interface BaseStore {
  count?: number;
  loadById: (id: number) => Promise<void>;
  loadList: (params?: Record<string, any>) => Promise<void>;
  create: (data: any) => Promise<any>;
  update: (id: number, data: any) => Promise<any>;
  deleteById: (id: number) => Promise<void>;
  deleteList: (ids: number[]) => Promise<void>;
}

export interface SearchFilters {
  search?: string;
}

export interface Filters extends SearchFilters {
  page?: number;
}
