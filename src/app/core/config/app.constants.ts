export const APP_ROUTES = {
  HOME: '/',
  AUTH: '/auth',
  TEAMS: '/teams',
  DRIVERS: '/drivers',
  NEWS: '/news',
  TOURNAMENTS: '/tournaments',
} as const;

export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'access_token',
  REFRESH_TOKEN: 'refresh_token',
  USER_DATA: 'user_data',
  THEME: 'theme',
} as const;
