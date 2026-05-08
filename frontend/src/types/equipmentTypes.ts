import type { Equipment } from "./equipments";

export interface CreateEquipmentType {
  name: string;
}

export interface SimpleEquipmentType extends CreateEquipmentType {
  id: number;
}

export interface EquipmentType extends SimpleEquipmentType {
  equipments: Equipment[];
}
