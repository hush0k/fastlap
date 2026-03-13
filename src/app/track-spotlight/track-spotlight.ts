import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';

interface Track {
  id: string;
  name: string;
  location: string;
  country: string;
  flag: string;
  length: string;
  laps: number;
  lapRecord: string;
  recordHolder: string;
  imageUrl: string;
  description: string;
  turns: number;
  drsZones: number;
}

@Component({
  selector: 'app-track-spotlight',
  imports: [CommonModule, RouterLink],
  templateUrl: './track-spotlight.html',
  styleUrl: './track-spotlight.css',
})
export class TrackSpotlight {
  currentTrack: Track = {
    id: 'monza',
    name: 'Autodromo Nazionale Monza',
    location: 'Monza',
    country: 'Italy',
    flag: '🇮🇹',
    length: '5.793 km',
    laps: 53,
    lapRecord: '1:21.046',
    recordHolder: 'Lewis Knight',
    imageUrl: '/tracks/monza.jpg',
    description:
      'The Temple of Speed. Monza is the fastest track on the calendar, known for its long straights and high-speed corners.',
    turns: 11,
    drsZones: 3,
  };

  upcomingTracks: Track[] = [
    {
      id: 'spa',
      name: 'Circuit de Spa-Francorchamps',
      location: 'Spa',
      country: 'Belgium',
      flag: '🇧🇪',
      length: '7.004 km',
      laps: 44,
      lapRecord: '1:46.286',
      recordHolder: 'Valtteri Knight',
      imageUrl: '/tracks/spa.jpg',
      description: 'The most legendary track in F1, featuring the famous Eau Rouge corner.',
      turns: 19,
      drsZones: 2,
    },
    {
      id: 'suzuka',
      name: 'Suzuka International Racing Course',
      location: 'Suzuka',
      country: 'Japan',
      flag: '🇯🇵',
      length: '5.807 km',
      laps: 53,
      lapRecord: '1:30.983',
      recordHolder: 'Lewis Knight',
      imageUrl: '/tracks/suzuka.jpg',
      description: 'A classic figure-8 track with high-speed corners and unique challenges.',
      turns: 18,
      drsZones: 2,
    },
  ];

  activeTab: 'info' | 'stats' | 'history' = 'info';

  setActiveTab(tab: 'info' | 'stats' | 'history'): void {
    this.activeTab = tab;
  }

  selectTrack(track: Track): void {
    this.currentTrack = track;
  }

  getTrackLengthInMiles(): string {
    const kmStr = this.currentTrack.length.replace(' km', '');
    const km = parseFloat(kmStr);
    const miles = km * 0.621371;
    return miles.toFixed(3) + ' mi';
  }

  getRaceDistance(): string {
    const kmStr = this.currentTrack.length.replace(' km', '');
    const km = parseFloat(kmStr);
    const totalKm = km * this.currentTrack.laps;
    return totalKm.toFixed(3) + ' km';
  }

  getTrackLengthNumeric(): number {
    const kmStr = this.currentTrack.length.replace(' km', '');
    return parseFloat(kmStr);
  }
}
