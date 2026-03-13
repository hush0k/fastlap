import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';

interface LiveEvent {
  id: string;
  time: string;
  driverNumber: string;
  driverName: string;
  team: string;
  event: string;
  detail: string;
  type: 'fastest-lap' | 'pit-stop' | 'overtake' | 'incident' | 'qualifying' | 'flag';
} 

@Component({
  selector: 'app-live-timing',
  imports: [CommonModule],
  templateUrl: './live-timing.html',
  styleUrl: './live-timing.css',
})
export class LiveTiming implements OnInit, OnDestroy {
  isLive = true;
  sessionName = 'Qualifying - Q3';
  currentTime = '15:32:45';

  events: LiveEvent[] = [
    {
      id: '1',
      time: '15:32',
      driverNumber: '1',
      driverName: 'STORM',
      team: 'Red Velocity',
      event: 'FASTEST LAP',
      detail: '1:29.456 - New track record!',
      type: 'fastest-lap',
    },
    {
      id: '2',
      time: '15:30',
      driverNumber: '44',
      driverName: 'KNIGHT',
      team: 'Silver Arrow',
      event: 'SECTOR 3',
      detail: 'Purple sector - +0.087s',
      type: 'qualifying',
    },
    {
      id: '3',
      time: '15:28',
      driverNumber: '16',
      driverName: 'LECLERC',
      team: 'Ferrari',
      event: 'PIT STOP',
      detail: '2.3s - Front wing adjustment',
      type: 'pit-stop',
    },
    {
      id: '4',
      time: '15:25',
      driverNumber: '55',
      driverName: 'SAINZ',
      team: 'Ferrari',
      event: 'OVERTAKE',
      detail: 'Passed PEREZ at Turn 4',
      type: 'overtake',
    },
    {
      id: '5',
      time: '15:22',
      driverNumber: '11',
      driverName: 'PEREZ',
      team: 'Red Velocity',
      event: 'INCIDENT',
      detail: 'Wide at Turn 1 - Loses 0.3s',
      type: 'incident',
    },
  ];

  private interval: any;

  ngOnInit() {
    // Simulate live updates
    this.interval = setInterval(() => {
      this.addRandomEvent();
    }, 15000); // Add new event every 15 seconds
  }

  ngOnDestroy() {
    if (this.interval) {
      clearInterval(this.interval);
    }
  }

  private addRandomEvent() {
    const drivers = [
      { num: '1', name: 'STORM', team: 'Red Velocity' },
      { num: '44', name: 'KNIGHT', team: 'Silver Arrow' },
      { num: '16', name: 'LECLERC', team: 'Ferrari' },
      { num: '55', name: 'SAINZ', team: 'Ferrari' },
      { num: '11', name: 'PEREZ', team: 'Red Velocity' },
    ];

    const events = [
      { type: 'fastest-lap', event: 'FASTEST LAP', detail: 'Personal best sector' },
      { type: 'qualifying', event: 'SECTOR TIME', detail: 'Improving on previous lap' },
      { type: 'pit-stop', event: 'PIT STOP', detail: 'Boxing this lap' },
      { type: 'overtake', event: 'OVERTAKE', detail: 'Gaining positions' },
      { type: 'incident', event: 'INCIDENT', detail: 'Off track at Turn 9' },
    ];

    const randomDriver = drivers[Math.floor(Math.random() * drivers.length)];
    const randomEvent = events[Math.floor(Math.random() * events.length)];

    const now = new Date();
    const timeStr = `${now.getHours()}:${now.getMinutes().toString().padStart(2, '0')}`;

    const newEvent: LiveEvent = {
      id: Date.now().toString(),
      time: timeStr,
      driverNumber: randomDriver.num,
      driverName: randomDriver.name,
      team: randomDriver.team,
      event: randomEvent.event,
      detail: randomEvent.detail,
      type: randomEvent.type as any,
    };

    this.events.unshift(newEvent);
    if (this.events.length > 10) {
      this.events.pop();
    }
  }

  getEventIcon(type: string): string {
    const icons = {
      'fastest-lap': 'fa-bolt',
      'pit-stop': 'fa-wrench',
      overtake: 'fa-arrow-right-arrow-left',
      incident: 'fa-triangle-exclamation',
      qualifying: 'fa-clock',
      flag: 'fa-flag',
    };
    return icons[type as keyof typeof icons] || 'fa-circle-info';
  }

  getEventColor(type: string): string {
    const colors = {
      'fastest-lap': '#00ff00',
      'pit-stop': '#ffaa00',
      overtake: '#00aaff',
      incident: '#ff4444',
      qualifying: '#aa88ff',
      flag: '#ffffff',
    };
    return colors[type as keyof typeof colors] || 'var(--text-secondary)';
  }

  getTeamColor(team: string): string {
    const colors: { [key: string]: string } = {
      'Red Velocity': '#e60000',
      'Silver Arrow': '#00d2be',
      Ferrari: '#dc0000',
    };
    return colors[team] || 'var(--accent-secondary)';
  }
}
