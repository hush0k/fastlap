import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';
import {
  LoginRequest,
  LoginResponse,
  RegisterRequest,
  RegisterResponse,
} from '../models/auth.models';

export interface AvatarResponse {
  avatar: string;
}

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private readonly baseUrl = environment.apiUrl;

  constructor(private readonly http: HttpClient) {}

  login(data: LoginRequest): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.baseUrl}/auth/login/`, data);
  }

  register(data: RegisterRequest, avatarFile: File): Observable<RegisterResponse> {
    const formData = new FormData();
    formData.append('email', data.email);
    formData.append('username', data.username);
    formData.append('password', data.password);
    formData.append('first_name', data.first_name);
    formData.append('last_name', data.last_name);
    formData.append('avatar', avatarFile);

    return this.http.post<RegisterResponse>(`${this.baseUrl}/auth/register/`, formData);
  }

  refreshToken(refreshToken: string): Observable<{ access: string }> {
    return this.http.post<{ access: string }>(`${this.baseUrl}/auth/refresh/`, {
      refresh: refreshToken,
    });
  }

  getAvatar(): Observable<AvatarResponse> {
    return this.http.get<AvatarResponse>(`${this.baseUrl}/auth/avatar/`);
  }

  uploadAvatar(file: File): Observable<AvatarResponse> {
    const formData = new FormData();
    formData.append('avatar', file);
    return this.http.post<AvatarResponse>(`${this.baseUrl}/auth/avatar/upload/`, formData);
  }

  deleteAvatar(): Observable<{ message: string }> {
    return this.http.delete<{ message: string }>(`${this.baseUrl}/auth/avatar/delete/`);
  }
}
