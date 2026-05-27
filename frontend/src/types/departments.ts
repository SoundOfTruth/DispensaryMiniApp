export interface CreateDepartment {
  name: string;
}

export interface Department extends CreateDepartment {
  id: number;
}
