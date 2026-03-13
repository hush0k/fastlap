export interface DriverStanding {
  position: number;
  driverId: string;
  driverName: string;
  teamId: string;
  teamName: string;
  points: number;
  wins: number;
  podiums: number;
}

export interface ConstructorStanding {
  position: number;
  teamId: string;
  teamName: string;
  points: number;
  wins: number;
}

export const DRIVER_STANDINGS_DATA: DriverStanding[] = [
  {
    position: 1,
    driverId: 'd1',
    driverName: 'Max Storm',
    teamId: 't1',
    teamName: 'Red Velocity Racing',
    points: 258,
    wins: 6,
    podiums: 10,
  },
  {
    position: 2,
    driverId: 'd2',
    driverName: 'Lewis Knight',
    teamId: 't2',
    teamName: 'Silver Arrow GP',
    points: 245,
    wins: 5,
    podiums: 9,
  },
  {
    position: 3,
    driverId: 'd3',
    driverName: 'Charles Leclerc',
    teamId: 't3',
    teamName: 'Scuderia Ferrari',
    points: 189,
    wins: 3,
    podiums: 7,
  },
];

export const CONSTRUCTOR_STANDINGS_DATA: ConstructorStanding[] = [
  {
    position: 1,
    teamId: 't1',
    teamName: 'Red Velocity Racing',
    points: 432,
    wins: 7,
  },
  {
    position: 2,
    teamId: 't2',
    teamName: 'Silver Arrow GP',
    points: 418,
    wins: 6,
  },
  {
    position: 3,
    teamId: 't3',
    teamName: 'Scuderia Ferrari',
    points: 302,
    wins: 3,
  },
];
