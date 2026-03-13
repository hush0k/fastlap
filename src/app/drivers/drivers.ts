import { ChangeDetectorRef, Component, OnDestroy, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { Subject, Subscription } from 'rxjs';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';

import { DriversService } from '../services/drivers.service';
import { DriverListItem } from '../models/driver-api.model';
import { environment } from '../../environments/environment';

interface NationalityOption {
  code: string;
  name: string;
}

@Component({
  selector: 'app-drivers',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './drivers.html',
  styleUrl: './drivers.css',
})
export class Drivers implements OnInit, OnDestroy {
  drivers: DriverListItem[] = [];

  loading = false;
  errorMessage = '';

  searchTerm = '';
  selectedNationality = '';
  numberInput = '';
  selectedActive: '' | 'true' | 'false' = '';

  total = 0;
  readonly pageSize = 20;
  offset = 0;

  availableNationalities: NationalityOption[] = [];

  readonly activeOptions = [
    { value: '', label: 'All Drivers' },
    { value: 'true', label: 'Active' },
    { value: 'false', label: 'Retired' },
  ];

  readonly mediaUrl = environment.mediaUrl;

  private readonly searchSubject = new Subject<string>();
  private readonly numberSubject = new Subject<string>();
  private readonly subscriptions = new Subscription();

  constructor(
    private readonly driversService: DriversService,
    private readonly cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.subscriptions.add(
      this.searchSubject.pipe(debounceTime(400), distinctUntilChanged()).subscribe((term) => {
        this.searchTerm = term;
        this.offset = 0;
        this.loadDrivers();
      }),
    );

    this.subscriptions.add(
      this.numberSubject.pipe(debounceTime(400), distinctUntilChanged()).subscribe((val) => {
        this.numberInput = val;
        this.offset = 0;
        this.loadDrivers();
      }),
    );

    this.loadDrivers();
  }

  ngOnDestroy(): void {
    this.subscriptions.unsubscribe();
  }

  loadDrivers(): void {
    this.loading = true;
    this.errorMessage = '';

    const parsedNumber = this.numberInput ? parseInt(this.numberInput, 10) : undefined;

    this.driversService
      .getDrivers({
        search: this.searchTerm || undefined,
        nationality: this.selectedNationality || undefined,
        number: !isNaN(parsedNumber!) ? parsedNumber : undefined,
        is_active: this.selectedActive === '' ? undefined : this.selectedActive === 'true',
        limit: this.pageSize,
        offset: this.offset,
      })
      .subscribe({
        next: (response) => {
          this.drivers = response.results;
          this.total = response.count;
          this.loading = false;
          this.buildNationalityOptions(response.results);
          this.cdr.markForCheck();
        },
        error: () => {
          this.errorMessage = 'Failed to load drivers. Please try again.';
          this.loading = false;
          this.cdr.markForCheck();
        },
      });
  }

  private buildNationalityOptions(drivers: DriverListItem[]): void {
    const existing = new Set(this.availableNationalities.map((n) => n.code));

    drivers.forEach((d) => {
      if (d.nationality && d.nationality_name && !existing.has(d.nationality)) {
        existing.add(d.nationality);
        this.availableNationalities.push({
          code: d.nationality,
          name: d.nationality_name,
        });
      }
    });

    this.availableNationalities.sort((a, b) => a.name.localeCompare(b.name));
  }

  onSearchInput(value: string): void {
    this.searchSubject.next(value);
  }
  onNumberInput(value: string): void {
    this.numberSubject.next(value);
  }

  onFilterChange(): void {
    this.offset = 0;
    this.loadDrivers();
  }

  clearFilters(): void {
    this.searchTerm = '';
    this.selectedNationality = '';
    this.numberInput = '';
    this.selectedActive = '';
    this.offset = 0;
    this.loadDrivers();
  }

  nextPage(): void {
    if (this.hasNext) {
      this.offset += this.pageSize;
      this.loadDrivers();
    }
  }

  prevPage(): void {
    if (this.hasPrev) {
      this.offset = Math.max(0, this.offset - this.pageSize);
      this.loadDrivers();
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
    return !!(
      this.searchTerm ||
      this.selectedNationality ||
      this.numberInput ||
      this.selectedActive
    );
  }

  getProfileImage(path: string | null): string {
    if (!path) return 'placeholders/driver-placeholder.jpg';
    if (path.startsWith('http')) return path;
    return `${this.mediaUrl}${path}`;
  }

  getInitials(driver: DriverListItem): string {
    return `${driver.first_name[0] ?? ''}${driver.last_name[0] ?? ''}`.toUpperCase();
  }
}
