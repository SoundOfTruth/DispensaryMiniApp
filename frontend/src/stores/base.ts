import type { ApiError } from "@/utils/api";

export interface BaseStore {
  limit?: number;
  count: number;
  errors: ApiError[];
  setLimit?: (limit: number) => void;
  loadById: (id: number) => Promise<void>;
  loadList: (params?: Record<string, any>) => Promise<void>;
  create: (data: any) => Promise<any>;
  update: (id: number, data: any) => Promise<any>;
  deleteById: (id: number) => Promise<void>;
  deleteList: (ids: number[]) => Promise<void>;
}
