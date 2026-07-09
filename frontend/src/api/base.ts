const apiUrl = import.meta.env.VITE_API_URL;
const mediaUrl = import.meta.env.VITE_MEDIA_URL;
export const baseApiUrl = apiUrl ? apiUrl : 'http://localhost:8000/api';
export const baseMediaUrl = mediaUrl !== undefined ? mediaUrl : 'http://localhost:8000';

export interface ApiSearchParams {
  search?: string;
}

export interface PaginationParams {
  limit: number;
  offset: number;
}

export interface ApiParams extends ApiSearchParams, PaginationParams {}
