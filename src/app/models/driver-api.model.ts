export interface DriverListItem {
  id: number;
  first_name: string;
  last_name: string;
  slug: string;
  nationality: string;
  nationality_name: string;
  number: number | null;
  profile_image: string | null;
  is_active: boolean;
}

export interface DriverDetail {
  id: number;
  first_name: string;
  last_name: string;
  slug: string;
  nationality: string;
  nationality_name: string;
  number: number | null;
  profile_image: string | null;
  bio: string | null;
  is_active: boolean;
  date_of_birth: string | null;
  created_at: string;
  updated_at: string;
}

export interface DriverQueryParams {
  search?: string;
  nationality?: string;
  number?: number;
  is_active?: boolean;
  limit?: number;
  offset?: number;
}
