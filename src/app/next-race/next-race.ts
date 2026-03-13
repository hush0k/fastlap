import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { Race, RACES_DATA } from '../models/race.model';

@Component({
  selector: 'app-next-race',
  imports: [CommonModule, RouterLink],
  templateUrl: './next-race.html',
  styleUrl: './next-race.css',
})
export class NextRace implements OnInit, OnDestroy {
  nextRace: Race | null = null;
  countdown: { days: number; hours: number; minutes: number; seconds: number } = {
    days: 0,
    hours: 0,
    minutes: 0,
    seconds: 0,
  };
  reminderSet = false;
  private interval: any;

  ngOnInit() {
    this.findNextRace();
    this.startCountdown();
  }

  ngOnDestroy() {
    if (this.interval) {
      clearInterval(this.interval);
    }
  }

  private findNextRace() {
    const now = new Date();
    const upcomingRaces = RACES_DATA.filter(
      (race) => race.status === 'upcoming' && race.date > now,
    ).sort((a, b) => a.date.getTime() - b.date.getTime());

    this.nextRace = upcomingRaces[0] || null;
  }

  private startCountdown() {
    this.updateCountdown();
    this.interval = setInterval(() => this.updateCountdown(), 1000);
  }

  private updateCountdown() {
    if (!this.nextRace) return;

    const now = new Date().getTime();
    const raceDate = this.nextRace.date.getTime();
    const distance = raceDate - now;

    if (distance < 0) {
      this.countdown = { days: 0, hours: 0, minutes: 0, seconds: 0 };
      return;
    }

    this.countdown = {
      days: Math.floor(distance / (1000 * 60 * 60 * 24)),
      hours: Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)),
      minutes: Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60)),
      seconds: Math.floor((distance % (1000 * 60)) / 1000),
    };
  }

  setReminder(): void {
    this.reminderSet = !this.reminderSet;

    if (this.reminderSet && this.nextRace) {
      console.log(`Reminder set for: ${this.nextRace.name}`);

      alert(`🔔 Reminder set for ${this.nextRace.name}!`);
    } else {
      console.log('Reminder removed');
    }
  }

  getWeatherIcon(): string {
    if (!this.nextRace) return 'fa-calendar';

    const icons: { [key: string]: string } = {
      UAE: 'fa-sun',
      USA: 'fa-cloud-sun',
      default: 'fa-cloud',
    };

    return icons[this.nextRace.country] || icons['default'];
  }
}
