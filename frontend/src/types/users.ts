export interface CreateUser {
  email: string;
  lastname: string;
  firstname: string;
  middlename: string;
  password: string;
  is_superuser: boolean;
}

export interface User extends CreateUser {
  id: number;
}

export interface PaginatedUsers {
  count: number;
  results: User[];
}
