import { Injectable } from '@angular/core';
import { AuthUser, JwtPayload } from '../models/auth.models';
import { STORAGE_KEYS } from '../core/config/app.constants';

@Injectable({
  providedIn: 'root',
})
export class TokenService {
  saveTokens(access: string, refresh: string): void {
    localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, access);
    localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, refresh);
  }

  getAccessToken(): string | null {
    return localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN);
  }

  getRefreshToken(): string | null {
    return localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);
  }

  saveUserData(user: AuthUser): void {
    localStorage.setItem(STORAGE_KEYS.USER_DATA, JSON.stringify(user));
  }

  getUserData(): AuthUser | null {
    const raw = localStorage.getItem(STORAGE_KEYS.USER_DATA);
    if (!raw) return null;

    try {
      return JSON.parse(raw) as AuthUser;
    } catch {
      this.removeUserData();
      return null;
    }
  }

  removeUserData(): void {
    localStorage.removeItem(STORAGE_KEYS.USER_DATA);
  }

  clear(): void {
    localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN);
    localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN);
    localStorage.removeItem(STORAGE_KEYS.USER_DATA);
  }

  decodeAccessToken(): JwtPayload | null {
    const token = this.getAccessToken();
    if (!token) return null;

    try {
      const payload = token.split('.')[1];
      return JSON.parse(atob(payload)) as JwtPayload;
    } catch {
      return null;
    }
  }

  isAccessTokenValid(): boolean {
    const payload = this.decodeAccessToken();
    if (!payload?.exp) return false;
    return Date.now() < payload.exp * 1000;
  }
}
