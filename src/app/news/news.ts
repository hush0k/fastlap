import {
  Component,
  OnInit,
  OnDestroy,
  ChangeDetectionStrategy,
  ChangeDetectorRef,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { Subject, takeUntil } from 'rxjs';

import { NewsService } from '../services/news.service';
import { ArticleListItem, ArticleDetail } from '../models/news-api.model';
import { resolveMediaUrl } from '../shared/utils/media.util';
import { formatShortDate } from '../shared/utils/date.util';

@Component({
  selector: 'app-news',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './news.html',
  styleUrl: './news.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class News implements OnInit, OnDestroy {
  articles: ArticleListItem[] = [];
  loading = true;
  error = '';

  totalCount = 0;
  pageSize = 12;
  currentOffset = 0;

  selectedArticle: ArticleDetail | null = null;
  modalLoading = false;
  modalError = '';
  isModalOpen = false;

  private readonly destroy$ = new Subject<void>();

  constructor(
    private readonly newsService: NewsService,
    private readonly cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.loadArticles();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  loadArticles(): void {
    this.loading = true;
    this.error = '';
    this.cdr.markForCheck();

    this.newsService
      .getArticles({ limit: this.pageSize, offset: this.currentOffset })
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (res) => {
          this.articles = res.results;
          this.totalCount = res.count;
          this.loading = false;
          this.cdr.markForCheck();
        },
        error: () => {
          this.error = 'Failed to load articles. Please try again.';
          this.loading = false;
          this.cdr.markForCheck();
        },
      });
  }

  openArticle(slug: string): void {
    this.isModalOpen = true;
    this.modalLoading = true;
    this.modalError = '';
    this.selectedArticle = null;
    document.body.style.overflow = 'hidden';
    this.cdr.markForCheck();

    this.newsService
      .getArticleBySlug(slug)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (article) => {
          this.selectedArticle = article;
          this.modalLoading = false;
          this.cdr.markForCheck();
        },
        error: () => {
          this.modalError = 'Failed to load article.';
          this.modalLoading = false;
          this.cdr.markForCheck();
        },
      });
  }

  closeModal(): void {
    this.isModalOpen = false;
    this.selectedArticle = null;
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
    this.loadArticles();
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

  getAuthorName(article: ArticleListItem | ArticleDetail): string {
    if (article.author.first_name) {
      return `${article.author.first_name} ${article.author.last_name ?? ''}`.trim();
    }
    return article.author.username;
  }
}
