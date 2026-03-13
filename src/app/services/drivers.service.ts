import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';
import { PaginatedResponse } from '../models/api.models';
import { DriverDetail, DriverListItem, DriverQueryParams } from '../models/driver-api.model';

@Injectable({
  providedIn: 'root',
})
export class DriversService {
  private readonly baseUrl = `${environment.apiUrl}/drivers`;

  constructor(private readonly http: HttpClient) {}

  getDrivers(params?: DriverQueryParams): Observable<PaginatedResponse<DriverListItem>> {
    let httpParams = new HttpParams();

    if (params?.search) httpParams = httpParams.set('search', params.search);
    if (params?.nationality) httpParams = httpParams.set('nationality', params.nationality);
    if (params?.number !== undefined && params.number !== null) {
      httpParams = httpParams.set('number', params.number);
    }
    if (params?.is_active !== undefined) {
      httpParams = httpParams.set('is_active', String(params.is_active));
    }
    if (params?.limit !== undefined) httpParams = httpParams.set('limit', params.limit);
    if (params?.offset !== undefined) httpParams = httpParams.set('offset', params.offset);

    return this.http.get<PaginatedResponse<DriverListItem>>(`${this.baseUrl}/`, {
      params: httpParams,
    });
  }

  getDriverBySlug(slug: string): Observable<DriverDetail> {
    return this.http.get<DriverDetail>(`${this.baseUrl}/${slug}/`);
  }
}
