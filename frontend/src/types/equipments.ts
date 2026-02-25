export interface Equiment {
  id: number;
  name: string;
  image: string;
}

export interface EquipmentsGroupedByType {
  type: string;
  equipments: Equiment[];
}
