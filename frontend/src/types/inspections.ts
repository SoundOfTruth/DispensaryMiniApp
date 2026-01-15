import type { SimpleDoctor } from "./doctors";

export interface SimpleInspection {
  id: number;
  title: string;
}

export interface Inspection {
  id: number;
  title: string;
  description: string;
  preparation: string;
  doctors: SimpleDoctor[];
}

export interface CreateInspectionDoctor {
  id: number;
}

export interface CreateInspection {
  title: string;
  description: string;
  preparation: string;
  doctors: CreateInspectionDoctor[];
}


export const getInspectionsPayload = (data: Inspection[]): Inspection[] => {
  return data;
};
