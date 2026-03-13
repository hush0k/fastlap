export interface WeatherForecast {
  day: string;
  condition: 'sunny' | 'cloudy' | 'rainy' | 'partly-cloudy' | 'stormy';
  temperature: number;
  humidity?: number;
  windSpeed?: number;
}

export const WEATHER_DATA: WeatherForecast[] = [
  {
    day: 'Friday',
    condition: 'sunny',
    temperature: 24,
  },
  {
    day: 'Saturday',
    condition: 'rainy',
    temperature: 21,
  },
  {
    day: 'Sunday',
    condition: 'partly-cloudy',
    temperature: 23,
  },
];
