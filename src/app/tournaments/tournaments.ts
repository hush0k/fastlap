import {
  Component,
  OnInit,
  OnDestroy,
  ChangeDetectionStrategy,
  ChangeDetectorRef,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Subject, takeUntil, debounceTime, distinctUntilChanged } from 'rxjs';

import { TournamentsService } from '../services/tournaments.service';
import { TournamentListItem, TournamentDetail } from '../models/tournament-api.model';
import { resolveMediaUrl } from '../shared/utils/media.util';
import { formatShortDate } from '../shared/utils/date.util';

type StatusFilter = '' | 'upcoming' | 'live' | 'finished' | 'cancelled';

@Component({
  selector: 'app-tournaments',
  imports: [CommonModule, FormsModule],
  templateUrl: './tournaments.html',
  styleUrl: './tournaments.css',
})
export class Tournaments implements OnInit, OnDestroy {
  tournaments: TournamentListItem[] = [];
  loading = true;
  error = '';

  searchQuery = '';
  activeStatus: StatusFilter = '';
  private readonly search$ = new Subject<string>();

  totalCount = 0;
  pageSize = 12;
  currentOffset = 0;

  selectedTournament: TournamentDetail | null = null;
  modalLoading = false;
  modalError = '';
  isModalOpen = false;

  readonly statusFilters: { label: string; value: StatusFilter; icon: string }[] = [
    { label: 'All', value: '', icon: 'fa-list' },
    { label: 'Upcoming', value: 'upcoming', icon: 'fa-clock' },
    { label: 'Live', value: 'live', icon: 'fa-tower-broadcast' },
    { label: 'Finished', value: 'finished', icon: 'fa-flag-checkered' },
    { label: 'Cancelled', value: 'cancelled', icon: 'fa-ban' },
  ];

  private readonly destroy$ = new Subject<void>();

  constructor(
    private readonly tournamentsService: TournamentsService,
    private readonly cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.search$
      .pipe(debounceTime(350), distinctUntilChanged(), takeUntil(this.destroy$))
      .subscribe(() => {
        this.currentOffset = 0;
        this.loadTournaments();
      });

    this.loadTournaments();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  loadTournaments(): void {
    this.loading = true;
    this.error = '';
    this.cdr.markForCheck();

    this.tournamentsService
      .getTournaments({
        search: this.searchQuery || undefined,
        status: this.activeStatus || undefined,
        limit: this.pageSize,
        offset: this.currentOffset,
      })
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (res) => {
          this.tournaments = res.results;
          this.totalCount = res.count;
          this.loading = false;
          this.cdr.markForCheck();
        },
        error: () => {
          this.error = 'Failed to load tournaments. Please try again.';
          this.loading = false;
          this.cdr.markForCheck();
        },
      });
  }

  onSearchInput(): void {
    this.search$.next(this.searchQuery);
  }

  setStatus(status: StatusFilter): void {
    this.activeStatus = status;
    this.currentOffset = 0;
    this.loadTournaments();
  }

  openTournament(id: number): void {
    this.isModalOpen = true;
    this.modalLoading = true;
    this.modalError = '';
    this.selectedTournament = null;
    document.body.style.overflow = 'hidden';
    this.cdr.markForCheck();

    this.tournamentsService
      .getTournamentById(id)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (tournament) => {
          this.selectedTournament = tournament;
          this.modalLoading = false;
          this.cdr.markForCheck();
        },
        error: () => {
          this.modalError = 'Failed to load tournament.';
          this.modalLoading = false;
          this.cdr.markForCheck();
        },
      });
  }

  closeModal(): void {
    this.isModalOpen = false;
    this.selectedTournament = null;
    document.body.style.overflow = '';
    this.cdr.markForCheck();
  }

  onModalBackdropClick(event: MouseEvent): void {
    if ((event.target as HTMLElement).classList.contains('modal-backdrop')) {
      this.closeModal();
    }
  }

  goToPage(offset: number): void {
    this.currentOffset = offset;
    this.loadTournaments();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  get totalPages(): number {
    return Math.ceil(this.totalCount / this.pageSize);
  }

  get currentPage(): number {
    return Math.floor(this.currentOffset / this.pageSize) + 1;
  }

  get pageNumbers(): number[] {
    return Array.from({ length: this.totalPages }, (_, i) => i + 1);
  }

  get hasPrev(): boolean {
    return this.currentOffset > 0;
  }

  get hasNext(): boolean {
    return this.currentOffset + this.pageSize < this.totalCount;
  }

  resolveImage(path: string | null): string {
    return resolveMediaUrl(path);
  }

  formatDate(iso: string | null): string {
    if (!iso) return '';
    return formatShortDate(iso);
  }

  formatPrize(amount: string | null, currency: string): string {
    if (!amount) return '—';
    const num = parseFloat(amount);
    if (isNaN(num)) return '—';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency || 'USD',
      maximumFractionDigits: 0,
    }).format(num);
  }

  getStatusIcon(status: string): string {
    const icons: Record<string, string> = {
      upcoming: 'fa-clock',
      live: 'fa-tower-broadcast',
      finished: 'fa-flag-checkered',
      cancelled: 'fa-ban',
    };
    return icons[status] ?? 'fa-circle';
  }
}
