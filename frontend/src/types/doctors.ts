import doctorsJson from "../data/doctors.json";

import type { SimpleInspection } from "./inspections";
export default doctorsJson;

export interface BaseDoctor {
  id: number;
  firstname: string;
  lastname: string;
  middlename: string;
}

export interface InputDoctorList extends BaseDoctor {
  qualification: string | null;
  speciality: string | null;
  department: string;
}

export interface InputDoctor extends InputDoctorList {
  experience: number;
  education: string[];
  extra_education: string[];
  inspections: [SimpleInspection];
}

export interface SimpleDoctor extends BaseDoctor {
  fullname: string;
  qualification: string | null;
  speciality: string | null;
  department: string;
}

export interface Doctor extends SimpleDoctor {
  experience: string;
  education: string[];
  extra_education: string[];
  inspections: [SimpleInspection];
}

export interface CreateDoctor {
  firstname: string;
  lastname: string;
  middlename: string;
  qualification: string | null;
  experience_start: number | null;
  speciality_id: number;
  department_id: number;
  education: string[];
  extra_education: string[];
}
