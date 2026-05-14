export interface CreateUser {
  email: string;
  lastname: string;
  firstname: string;
  middlename: string;
  password: string;
  role: "user" | "admin" | "superuser";
}

export interface User extends CreateUser {
  id: number;
}

export interface PaginatedUsers {
  count: number;
  results: User[];
}
