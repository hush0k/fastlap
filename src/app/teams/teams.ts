import { ChangeDetectorRef, Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { Subject, Subscription } from 'rxjs';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';

import { TeamsService } from '../services/teams.service';
import { TeamListItem } from '../models/team-api.model';
import { environment } from '../../environments/environment';

interface CountryOption {
  code: string;
  name: string;
}

@Component({
  selector: 'app-teams',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './teams.html',
  styleUrl: './teams.css',
})
export class Teams implements OnInit, OnDestroy {
  teams: TeamListItem[] = [];

  loading = false;
  errorMessage = '';

  searchTerm = '';
  selectedCountry = '';
  selectedOrdering = 'name';

  total = 0;
  readonly pageSize = 20;
  offset = 0;

  availableCountries: CountryOption[] = [];

  readonly orderingOptions = [
    { value: 'name', label: 'Name (A → Z)' },
    { value: '-name', label: 'Name (Z → A)' },
    { value: 'founded_year', label: 'Founded (Oldest first)' },
    { value: '-founded_year', label: 'Founded (Newest first)' },
  ];

  readonly mediaUrl = environment.mediaUrl;

  private readonly searchSubject = new Subject<string>();
  private readonly subscriptions = new Subscription();

  constructor(
    private readonly teamsService: TeamsService,
    private readonly cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.subscriptions.add(
      this.searchSubject.pipe(debounceTime(400), distinctUntilChanged()).subscribe((term) => {
        this.searchTerm = term;
        this.offset = 0;
        this.loadTeams();
      }),
    );

    this.loadTeams();
  }

  ngOnDestroy(): void {
    this.subscriptions.unsubscribe();
  }

  loadTeams(): void {
    this.loading = true;
    this.errorMessage = '';

    this.teamsService
      .getTeams({
        search: this.searchTerm || undefined,
        country: this.selectedCountry || undefined,
        ordering: this.selectedOrdering,
        limit: this.pageSize,
        offset: this.offset,
      })
      .subscribe({
        next: (response) => {
          this.teams = response.results;
          this.total = response.count;
          this.loading = false;
          this.buildCountryOptions(response.results);
          this.cdr.markForCheck();
        },
        error: () => {
          this.errorMessage = 'Failed to load teams. Please try again.';
          this.loading = false;
          this.cdr.markForCheck();
        },
      });
  }

  private buildCountryOptions(teams: TeamListItem[]): void {
    const existing = new Set(this.availableCountries.map((c) => c.code));

    teams.forEach((team) => {
      if (team.country && team.country_name && !existing.has(team.country)) {
        existing.add(team.country);
        this.availableCountries.push({ code: team.country, name: team.country_name });
      }
    });

    this.availableCountries.sort((a, b) => a.name.localeCompare(b.name));
  }

  onSearchInput(value: string): void {
    this.searchSubject.next(value);
  }

  onFilterChange(): void {
    this.offset = 0;
    this.loadTeams();
  }

  clearFilters(): void {
    this.searchTerm = '';
    this.selectedCountry = '';
    this.selectedOrdering = 'name';
    this.offset = 0;
    this.loadTeams();
  }

  nextPage(): void {
    if (this.hasNext) {
      this.offset += this.pageSize;
      this.loadTeams();
    }
  }

  prevPage(): void {
    if (this.hasPrev) {
      this.offset = Math.max(0, this.offset - this.pageSize);
      this.loadTeams();
    }
  }

  get hasNext(): boolean {
    return this.offset + this.pageSize < this.total;
  }
  get hasPrev(): boolean {
    return this.offset > 0;
  }
  get currentPage(): number {
    return Math.floor(this.offset / this.pageSize) + 1;
  }
  get totalPages(): number {
    return Math.ceil(this.total / this.pageSize);
  }
  get showingFrom(): number {
    return this.total === 0 ? 0 : this.offset + 1;
  }
  get showingTo(): number {
    return Math.min(this.offset + this.pageSize, this.total);
  }
  get hasActiveFilters(): boolean {
    return !!(this.searchTerm || this.selectedCountry || this.selectedOrdering !== 'name');
  }

  getLogo(path: string | null): string {
    if (!path) return 'placeholders/team-placeholder.jpg';
    if (path.startsWith('http')) return path;
    return `${this.mediaUrl}${path}`;
  }

  getBanner(path: string | null): string {
    if (!path) return '';
    if (path.startsWith('http')) return path;
    return `${this.mediaUrl}${path}`;
  }
}
