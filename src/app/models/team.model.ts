export interface Team {
  id: string;
  name: string;
  base: string;
  teamPrincipal: string;
  championships: number;
  logoUrl: string;
}

export const TEAMS_DATA: Team[] = [
  {
    id: 't1',
    name: 'Red Velocity Racing',
    base: 'Milton Keynes, UK',
    teamPrincipal: 'Christian Wolfe',
    championships: 6,
    logoUrl: '/teams/red-velocity.png',
  },
  {
    id: 't2',
    name: 'Silver Arrow GP',
    base: 'Brackley, UK',
    teamPrincipal: 'Toto Schneider',
    championships: 8,
    logoUrl: '/teams/silver-arrow.png',
  },
];
