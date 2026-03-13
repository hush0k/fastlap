export interface Race {
  id: string;
  name: string;
  circuit: string;
  country: string;
  flag: string;
  date: Date;
  time: string;
  round: number;
  season: number;
  status: 'upcoming' | 'ongoing' | 'completed';
  winner?: {
    driverId: string;
    teamId: string;
  };
}

export const RACES_DATA: Race[] = [
  {
    id: 'r1',
    name: 'Abu Dhabi Grand Prix',
    circuit: 'Yas Marina Circuit',
    country: 'UAE',
    flag: '🇦🇪',
    date: new Date('2026-11-24'),
    time: '15:00 GST',
    round: 24,
    season: 2026,
    status: 'upcoming',
  },
  {
    id: 'r2',
    name: 'Las Vegas Grand Prix',
    circuit: 'Las Vegas Strip Circuit',
    country: 'USA',
    flag: '🇺🇸',
    date: new Date('2026-11-17'),
    time: '22:00 PST',
    round: 23,
    season: 2026,
    status: 'upcoming',
  },
];
