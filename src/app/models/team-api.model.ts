export interface TeamListItem {
  id: number;
  name: string;
  slug: string;
  short_name: string;
  logo: string | null;
  banner: string | null;
  country: string;
  country_name: string;
}

export interface TeamStanding {
  id: number;
  team: number;
  tournament: number;
  tournament_name: string;
  tournament_slug: string;
  points: number;
  position: number | null;
}

export interface TeamDetail {
  id: number;
  name: string;
  slug: string;
  short_name: string;
  logo: string | null;
  banner: string | null;
  country: string;
  country_name: string;
  founded_year: number | null;
  description: string;
  budget: string | null;
  budget_currency: string;
  main_sponsor: string;
  secondary_sponsor: string;
  standings: TeamStanding[];
  created_at: string;
  updated_at: string;
}

export interface TeamQueryParams {
  search?: string;
  country?: string;
  founded_year?: number;
  ordering?: string;
  limit?: number;
  offset?: number;
}
