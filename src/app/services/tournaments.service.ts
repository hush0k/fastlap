import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';
import { PaginatedResponse } from '../models/api.models';
import {
  TournamentDetail,
  TournamentListItem,
  TournamentQueryParams,
} from '../models/tournament-api.model';

@Injectable({
  providedIn: 'root',
})
export class TournamentsService {
  private readonly baseUrl = `${environment.apiUrl}/tournaments`;

  constructor(private readonly http: HttpClient) {}

  getTournaments(
    params?: TournamentQueryParams,
  ): Observable<PaginatedResponse<TournamentListItem>> {
    let httpParams = new HttpParams();

    if (params?.search) httpParams = httpParams.set('search', params.search);
    if (params?.status) httpParams = httpParams.set('status', params.status);
    if (params?.limit !== undefined) httpParams = httpParams.set('limit', params.limit);
    if (params?.offset !== undefined) httpParams = httpParams.set('offset', params.offset);

    return this.http.get<PaginatedResponse<TournamentListItem>>(`${this.baseUrl}/`, {
      params: httpParams,
    });
  }

  getTournamentById(id: number): Observable<TournamentDetail> {
    return this.http.get<TournamentDetail>(`${this.baseUrl}/${id}/detail/`);
  }
}
