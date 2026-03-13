import { CommonModule } from '@angular/common';
import { Component, ViewEncapsulation } from '@angular/core';
import { RouterLink } from '@angular/router';
import { NewsItem, NEWS_DATA } from '../models/news.model';
import { NextRace } from '../next-race/next-race';
import { StandingsWidget } from '../standings-widget/standings-widget';
import { LiveTiming } from '../live-timing/live-timing';
import { DriverVote } from '../driver-vote/driver-vote';
import { WeatherWidget } from '../weather-widget/weather-widget';
import { TrackSpotlight } from '../track-spotlight/track-spotlight';

@Component({
  selector: 'app-home-page',
  imports: [
    CommonModule,
    RouterLink,
    NextRace,
    StandingsWidget,
    LiveTiming,
    DriverVote,
    WeatherWidget,
    TrackSpotlight,
  ],
  templateUrl: './home-page.html',
  styleUrl: './home-page.css',
  encapsulation: ViewEncapsulation.None,
})
export class HomePage {
  topNews: NewsItem[] = NEWS_DATA.slice(0, 2);

  formatDate(iso: string): string {
    const d = new Date(iso);
    return d.toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: '2-digit',
    });
  }

  getTagIcon(tag: string): string {
    const icons = {
      Breaking: 'fa-bolt',
      Rumor: 'fa-circle-exclamation',
      Official: 'fa-check-circle',
      Analysis: 'fa-chart-line',
    };
    return icons[tag as keyof typeof icons] || 'fa-newspaper';
  }
}
