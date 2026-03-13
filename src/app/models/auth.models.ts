export interface AuthUser {
  email: string;
  username?: string;
  first_name?: string;
  last_name?: string;
  user_id?: number;
}

export interface JwtPayload {
  exp: number;
  email?: string;
  user_id?: number;
  username?: string;
  first_name?: string;
  last_name?: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
  first_name: string;
  last_name: string;
}

export interface RegisterResponse {
  email: string;
  username: string;
  first_name: string;
  last_name: string;
}

export interface RefreshResponse {
  access: string;
}

export interface ApiValidationErrors {
  [key: string]: string | string[];
}

export interface AuthError {
  message: string;
  fieldErrors?: Record<string, string>;
  status?: number;
}
