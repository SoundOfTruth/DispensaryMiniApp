import doctorsJson from "../data/doctors.json";

import type { SimpleInspection } from "./inspections";
export default doctorsJson;

export interface BaseDoctor {
  id: number;
  firstname: string;
  lastname: string;
  middlename: string;
}

export interface SimpleDoctor extends BaseDoctor {
  qualification: string | null;
  speciality: string | null;
  department: string;
}

export interface ApiDoctor extends SimpleDoctor {
  experience_start: number;
  education: string[];
  extra_education: string[];
  inspections: [SimpleInspection];
}

export interface Doctor extends ApiDoctor {
  experience: string;
}

export interface CreateEducation {
  title: string;
}

export interface CreateExtraEducation extends CreateEducation {}

export interface CreateDoctor {
  firstname: string;
  lastname: string;
  middlename: string;
  qualification: string | null;
  experience_start: number | null;
  speciality_id: number;
  department_id: number;
  education: CreateEducation[];
  extra_education: CreateExtraEducation[];
}

export interface PaginatedDoctors {
  count: number;
  results: SimpleDoctor[];
}
