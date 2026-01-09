import doctorsJson from "../data/doctors.json";

export default doctorsJson;

export interface BaseDoctor {
  id: number;
  firstname: string;
  lastname: string;
  middlename: string;
  fullname?: string;
}

interface DoctorInfo {
  speciality: string;
  qualification: string;
  department: string;
  education: string[];
  extra_education: string[];
}

interface InputDoctor extends DoctorInfo {
  id: number;
  firstname: string;
  lastname: string;
  middlename: string;
  experience: number;
}

export interface Doctor extends BaseDoctor, DoctorInfo {
  experience: string;
}

export const getDoctorPayload = (doctor: BaseDoctor | undefined): BaseDoctor | undefined => {
  if (!doctor){
    return undefined
  }
  return {
    ...doctor,
    fullname: `${doctor.lastname} ${doctor.firstname} ${doctor.middlename}`,
  };
};

export const getDoctorsPayload = (data: InputDoctor[]): Doctor[] => {
  return data.map((doctor) => ({
    ...doctor,
    fullname: `${doctor.lastname} ${doctor.firstname} ${doctor.middlename}`,
    experience: `${doctor.experience} лет`,
  }));
};

export const getDoctorsJsonPayload = (): Doctor[] => {
  return getDoctorsPayload(doctorsJson);
};
