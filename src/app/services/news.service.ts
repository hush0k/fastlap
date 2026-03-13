import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';
import { PaginatedResponse } from '../models/api.models';
import { ArticleDetail, ArticleListItem, ArticleQueryParams } from '../models/news-api.model';

@Injectable({
  providedIn: 'root',
})
export class NewsService {
  private readonly baseUrl = `${environment.apiUrl}/news`;

  constructor(private readonly http: HttpClient) {}

  getArticles(params?: ArticleQueryParams): Observable<PaginatedResponse<ArticleListItem>> {
    let httpParams = new HttpParams();

    if (params?.limit !== undefined) httpParams = httpParams.set('limit', params.limit);
    if (params?.offset !== undefined) httpParams = httpParams.set('offset', params.offset);

    return this.http.get<PaginatedResponse<ArticleListItem>>(`${this.baseUrl}/`, {
      params: httpParams,
    });
  }

  getArticleBySlug(slug: string): Observable<ArticleDetail> {
    return this.http.get<ArticleDetail>(`${this.baseUrl}/${slug}/`);
  }
}
