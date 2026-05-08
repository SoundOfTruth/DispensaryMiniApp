import type { SimpleInspection } from "./inspections";

import { type Speciality } from "./specialities";
import { type Department } from "./departments";

export interface SimpleDoctor {
  id: number;
  firstname: string;
  lastname: string;
  middlename: string;
  qualification: string | null;
  photo: string | null;

  speciality: Speciality;
  department: Department;
}

export interface ApiDoctor extends SimpleDoctor {
  experience_start: number | null;
  experience_years: number | null;
  education: string[];
  extra_education: string[];
  inspections: SimpleInspection[];
}

export interface Doctor extends ApiDoctor {
  experience: string;
}

interface DoctorInspection {
  id: number;
}

interface CreateDoctorMixin {
  lastname: string;
  firstname: string;
  middlename: string;
  qualification: string | null;
  speciality_id: number;
  department_id: number;
  photo: string | null;
  education: string[];
  extra_education: string[];
}

export interface CreateDoctorForm extends CreateDoctorMixin {
  experience_start: string | number | null;
  inspections: SimpleInspection[];
}

export interface CreateDoctor extends CreateDoctorMixin {
  experience_start: number | null;
  inspections: DoctorInspection[];
}

export interface PaginatedDoctors {
  count: number;
  results: SimpleDoctor[];
}
