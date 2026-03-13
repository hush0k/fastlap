export interface Driver {
  id: string;
  firstName: string;
  lastName: string;
  number: number;
  nationality: string;
  teamId: string;
  podiums: number;
  worldTitles: number;
  photoUrl: string;
}

export const DRIVERS_DATA: Driver[] = [
  {
    id: 'd1',
    firstName: 'Max',
    lastName: 'Storm',
    number: 1,
    nationality: 'Dutch',
    teamId: 't1',
    podiums: 95,
    worldTitles: 3,
    photoUrl: '/drivers/max-storm.jpg',
  },
  {
    id: 'd2',
    firstName: 'Lewis',
    lastName: 'Knight',
    number: 44,
    nationality: 'British',
    teamId: 't2',
    podiums: 180,
    worldTitles: 7,
    photoUrl: '/drivers/lewis-knight.jpg',
  },
];
