export type Item = Record<string, any>;

export type Passenger = {
  name: string;
  age: number;
  gender: string;
  phone: string;
  email: string;
};

export type Cart = Item & {
  cart_id: string;
  passenger_count: number;
  passengers: Passenger[];
  price_snapshot?: Item;
};
