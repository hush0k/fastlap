import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { WeatherForecast, WEATHER_DATA } from '../models/weather.model';

type WeatherCondition = 'sunny' | 'cloudy' | 'rainy' | 'partly-cloudy' | 'stormy';

@Component({
  selector: 'app-weather-widget',
  imports: [CommonModule],
  templateUrl: './weather-widget.html',
  styleUrl: './weather-widget.css',
})
export class WeatherWidget {
  @Input() location: string = 'Yas Marina Circuit, Abu Dhabi';

  forecasts: WeatherForecast[] = WEATHER_DATA;
  currentConditions = {
    temperature: 24,
    humidity: 65,
    windSpeed: 12,
    condition: 'partly-cloudy' as WeatherCondition,
  };

  getWeatherIcon(condition: string): string {
    const icons: Record<string, string> = {
      sunny: 'fa-sun',
      cloudy: 'fa-cloud',
      rainy: 'fa-cloud-rain',
      'partly-cloudy': 'fa-cloud-sun',
      stormy: 'fa-cloud-bolt',
    };
    return icons[condition] || 'fa-cloud';
  }

  getWeatherColor(condition: string): string {
    const colors: Record<string, string> = {
      sunny: '#ffaa00',
      cloudy: '#a0a0a0',
      rainy: '#4d94ff',
      'partly-cloudy': '#ffaa00',
      stormy: '#6b4d8f',
    };
    return colors[condition] || 'var(--text-secondary)';
  }

  getTrackCondition(): string {
    switch (this.currentConditions.condition) {
      case 'sunny':
        return 'Perfect for racing';
      case 'rainy':
        return 'Wet race possible';
      case 'cloudy':
        return 'Good track conditions';
      case 'partly-cloudy':
        return 'Ideal conditions';
      case 'stormy':
        return 'Risk of delay';
      default:
        return 'Normal conditions';
    }
  }

  isRainy(): boolean {
    return this.currentConditions.condition === 'rainy';
  }
}
