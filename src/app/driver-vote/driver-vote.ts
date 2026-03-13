import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Driver, DRIVERS_DATA } from '../models/driver.model';

interface DriverWithVotes extends Driver {
  votes: number;
  hasVoted: boolean;
}

@Component({
  selector: 'app-driver-vote',
  imports: [CommonModule],
  templateUrl: './driver-vote.html',
  styleUrl: './driver-vote.css',
})
export class DriverVote implements OnInit {
  drivers: DriverWithVotes[] = [];
  totalVotes: number = 0;
  userVoted: boolean = false;
  votingEndsIn = '02:34:15';
  private votingEndTimer: any;

  ngOnInit() {
    this.drivers = DRIVERS_DATA.slice(0, 3)
      .map((driver, index) => ({
        ...driver,
        votes: Math.floor(Math.random() * 15000) + 5000,
        hasVoted: false,
      }))
      .sort((a, b) => b.votes - a.votes);

    this.calculateTotalVotes();
    this.startVotingTimer();
  }

  ngOnDestroy() {
    if (this.votingEndTimer) {
      clearInterval(this.votingEndTimer);
    }
  }

  voteForDriver(driver: DriverWithVotes): void {
    if (this.userVoted) return;

    driver.votes += 1;
    driver.hasVoted = true;
    this.userVoted = true;
    this.calculateTotalVotes();

    this.drivers.sort((a, b) => b.votes - a.votes);

    const votedDrivers = JSON.parse(localStorage.getItem('votedDrivers') || '[]');
    votedDrivers.push(driver.id);
    localStorage.setItem('votedDrivers', JSON.stringify(votedDrivers));
    localStorage.setItem('votingTimestamp', Date.now().toString());

    alert(`✅ You voted for ${driver.firstName} ${driver.lastName}!`);
  }

  private calculateTotalVotes(): void {
    this.totalVotes = this.drivers.reduce((sum, driver) => sum + driver.votes, 0);
  }

  private startVotingTimer(): void {
    let seconds = 2 * 60 * 60 + 34 * 60 + 15;

    this.votingEndTimer = setInterval(() => {
      if (seconds > 0) {
        seconds--;
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        this.votingEndsIn = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
      } else {
        clearInterval(this.votingEndTimer);
        this.votingEndsIn = 'VOTING CLOSED';
      }
    }, 1000);
  }

  getVotePercentage(votes: number): number {
    return (votes / this.totalVotes) * 100;
  }

  getDriverInitials(driver: Driver): string {
    return `${driver.firstName[0]}${driver.lastName[0]}`;
  }
}