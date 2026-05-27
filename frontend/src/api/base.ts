const apiUrl = import.meta.env.VITE_API_URL;
export const baseApiUrl = apiUrl ? apiUrl : 'http://localhost:8000/api';

export interface ApiSearchParams {
  search?: string;
}

export interface PaginationParams {
  limit: number;
  offset: number;
}

export interface ApiParams extends ApiSearchParams, PaginationParams {}
