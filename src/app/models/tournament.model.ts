export interface Tournament {
  id: string;
  name: string;
  season: number;
  races: number;
  championTeam: string;
  championDriver: string;
}

export const TOURNAMENTS_DATA: Tournament[] = [
  {
    id: '2026',
    name: 'Formula 1 World Championship',
    season: 2026,
    races: 24,
    championTeam: 'Red Velocity Racing',
    championDriver: 'Max Storm',
  },
  {
    id: '2025',
    name: 'Formula 1 World Championship',
    season: 2025,
    races: 23,
    championTeam: 'Silver Arrow GP',
    championDriver: 'Lewis Knight',
  },
];
