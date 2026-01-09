import inspectionsJson from "../data/inspections.json";

import type { BaseDoctor } from "./doctors";

export default inspectionsJson;

export interface Inspection {
  id: number;
  title: string;
  description: string;
  preparation: string;
  doctor: BaseDoctor;
}

export const getInspectionsPayload = (data: Inspection[]): Inspection[] => {
  return data;
};

export const getInspectionsJsonPayload = (): Inspection[] => {
  return inspectionsJson;
};
