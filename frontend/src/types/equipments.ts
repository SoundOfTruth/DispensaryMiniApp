export interface CreateEquipment {
  name: string;
  image: string;
  type_id: number;
}

export interface SimpleEquipment extends CreateEquipment {
  id: number;
}

export interface Equipment {
  id: number;
  name: string;
  image: string;
  type: SimpleEquipmentType;
}

export interface CreateEquipmentType {
  name: string;
}

export interface SimpleEquipmentType extends CreateEquipmentType {
  id: number;
}

export interface EquipmentItem {
  id: number;
  name: string;
  image: string;
}

export interface EquipmentType extends SimpleEquipmentType {
  equipments: EquipmentItem[];
}
