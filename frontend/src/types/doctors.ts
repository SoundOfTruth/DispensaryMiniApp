import doctorsJson from "../data/doctors.json";

export default doctorsJson;

export interface BaseDoctor {
  id: number;
  firstname: string;
  lastname: string;
  middlename: string;
}

interface InputDoctorList extends BaseDoctor {
  qualification: string | null;
  speciality: string | null;
  department: string;
}

interface InputDoctor extends InputDoctorList {
  experience: number;
  education: string[];
  extra_education: string[];
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
}

function getYearsWord(years: number | undefined): string {
  if (!years) {
    return "";
  }
  if (years % 10 === 1 && years % 100 !== 11) {
    return `${years}год`;
  } else if (
    years % 10 >= 2 &&
    years % 10 <= 4 &&
    (years % 100 < 10 || years % 100 >= 20)
  ) {
    return `${years}года`;
  } else {
    return `${years} лет`;
  }
}

export const getComputedDoctor = (doctor: InputDoctor): Doctor => {
  return {
    ...doctor,
    fullname: `${doctor.lastname} ${doctor.firstname} ${doctor.middlename}`,
    experience: getYearsWord(doctor.experience),
  };
};

export const getComputedDoctors = (data: InputDoctorList[]): SimpleDoctor[] => {
  return data.map((doctor) => ({
    ...doctor,
    fullname: `${doctor.lastname} ${doctor.firstname} ${doctor.middlename}`,
  }));
};
