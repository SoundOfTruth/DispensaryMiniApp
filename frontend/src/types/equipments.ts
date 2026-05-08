export interface CreateEquipment {
  name: string;
  image: string;
  type_id: number;
}

export interface Equipment extends CreateEquipment {
  id: number;
}

export interface SimpleEquipment {
  id: number;
  name: string;
  image: string;
}
