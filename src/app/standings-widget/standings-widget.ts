import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import {
  DriverStanding,
  ConstructorStanding,
  DRIVER_STANDINGS_DATA,
  CONSTRUCTOR_STANDINGS_DATA,
} from '../models/standing.model';

@Component({
  selector: 'app-standings-widget',
  imports: [CommonModule],
  templateUrl: './standings-widget.html',
  styleUrl: './standings-widget.css',
})
export class StandingsWidget {
  @Input() limit: number = 3;

  driverStandings: DriverStanding[] = DRIVER_STANDINGS_DATA.slice(0, this.limit);
  constructorStandings: ConstructorStanding[] = CONSTRUCTOR_STANDINGS_DATA.slice(0, 2);

  activeTab: 'drivers' | 'constructors' = 'drivers';

  setActiveTab(tab: 'drivers' | 'constructors') {
    this.activeTab = tab;
  }

  getTeamColor(teamName: string): string {
    const colors: { [key: string]: string } = {
      'Red Velocity Racing': '#e60000',
      'Silver Arrow GP': '#00d2be',
      'Scuderia Ferrari': '#dc0000',
    };
    return colors[teamName] || 'var(--accent-secondary)';
  }
}
