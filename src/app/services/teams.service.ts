import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { PaginatedResponse } from '../models/api.models';
import { TeamDetail, TeamListItem, TeamQueryParams, TeamStanding } from '../models/team-api.model';

@Injectable({
  providedIn: 'root',
})
export class TeamsService {
  private readonly baseUrl = `${environment.apiUrl}/teams`;

  constructor(private readonly http: HttpClient) {}

  getTeams(params?: TeamQueryParams): Observable<PaginatedResponse<TeamListItem>> {
    let httpParams = new HttpParams();

    if (params?.search) httpParams = httpParams.set('search', params.search);
    if (params?.country) httpParams = httpParams.set('country', params.country);
    if (params?.founded_year) httpParams = httpParams.set('founded_year', params.founded_year);
    if (params?.ordering) httpParams = httpParams.set('ordering', params.ordering);
    if (params?.limit !== undefined) httpParams = httpParams.set('limit', params.limit);
    if (params?.offset !== undefined) httpParams = httpParams.set('offset', params.offset);

    return this.http.get<PaginatedResponse<TeamListItem>>(`${this.baseUrl}/`, {
      params: httpParams,
    });
  }

  getTeamBySlug(slug: string): Observable<TeamDetail> {
    return this.http.get<TeamDetail>(`${this.baseUrl}/${slug}/`);
  }

  getTeamStandings(slug: string): Observable<TeamStanding[]> {
    return this.http.get<TeamStanding[]>(`${this.baseUrl}/${slug}/standings/`);
  }
}
