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

export const getInspectionsPayload = (data: Inspection[]): Inspection[] => {
  return data;
};
