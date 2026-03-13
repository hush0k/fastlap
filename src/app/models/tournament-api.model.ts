export interface TournamentSeries {
  id: number;
  name: string;
  slug?: string;
}

export interface TournamentListItem {
  id: number;
  name: string;
  slug: string;
  series: TournamentSeries;
  year: number;
  status: 'upcoming' | 'live' | 'finished' | 'cancelled';
  is_active: boolean;
  logo: string | null;
  start_date: string;
  end_date: string;
  total_rounds: number;
  prize_fund: string | null;
  currency: string;
}

export interface TournamentDetail {
  id: number;
  name: string;
  slug: string;
  series: TournamentSeries;
  year: number;
  status: 'upcoming' | 'live' | 'finished' | 'cancelled';
  is_active: boolean;
  logo: string | null;
  description: string;
  start_date: string;
  end_date: string;
  total_rounds: number;
  prize_fund: string | null;
  currency: string;
  regulations_url: string;
  created_at: string;
  updated_at: string;
}

export interface TournamentQueryParams {
  search?: string;
  status?: string;
  limit?: number;
  offset?: number;
}
