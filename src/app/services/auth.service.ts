import { Injectable } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable, throwError } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { ApiService } from './api.service';
import { TokenService } from './token.service';
import {
  AuthError,
  AuthUser,
  LoginRequest,
  RefreshResponse,
  RegisterRequest,
} from '../models/auth.models';
import { APP_ROUTES } from '../core/config/app.constants';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private readonly currentUserSubject = new BehaviorSubject<AuthUser | null>(null);
  readonly currentUser$ = this.currentUserSubject.asObservable();

  private readonly isAuthenticatedSubject = new BehaviorSubject<boolean>(false);
  readonly isAuthenticated$ = this.isAuthenticatedSubject.asObservable();

  constructor(
    private readonly apiService: ApiService,
    private readonly tokenService: TokenService,
    private readonly router: Router,
  ) {
    this.bootstrapAuth();
  }

  login(email: string, password: string): Observable<void> {
    const data: LoginRequest = { email, password };

    return this.apiService.login(data).pipe(
      tap(({ access, refresh }) => {
        this.tokenService.saveTokens(access, refresh);
        this.hydrateUserFromToken();
        this.isAuthenticatedSubject.next(true);
      }),
      map(() => void 0),
      catchError((error) => throwError(() => this.mapHttpError(error))),
    );
  }

  register(data: RegisterRequest, avatarFile: File): Observable<void> {
    return this.apiService.register(data, avatarFile).pipe(
      map(() => void 0),
      catchError((error) => throwError(() => this.mapHttpError(error))),
    );
  }

  logout(redirectToAuth = true): void {
    this.tokenService.clear();
    this.currentUserSubject.next(null);
    this.isAuthenticatedSubject.next(false);

    if (redirectToAuth) {
      this.router.navigate([APP_ROUTES.AUTH]);
    }
  }

  refreshToken(): Observable<string> {
    const refresh = this.tokenService.getRefreshToken();

    if (!refresh) {
      return throwError(
        () =>
          ({
            message: 'Session expired. Please sign in again.',
          }) as AuthError,
      );
    }

    return this.apiService.refreshToken(refresh).pipe(
      tap(({ access }) => {
        this.tokenService.saveTokens(access, refresh);
        this.hydrateUserFromToken();
        this.isAuthenticatedSubject.next(true);
      }),
      map((response: RefreshResponse) => response.access),
      catchError((error) => throwError(() => this.mapHttpError(error))),
    );
  }

  isAuthenticated(): boolean {
    return this.isAuthenticatedSubject.value;
  }

  getAccessToken(): string | null {
    return this.tokenService.getAccessToken();
  }

  getUserData(): AuthUser | null {
    return this.currentUserSubject.value ?? this.tokenService.getUserData();
  }

  private bootstrapAuth(): void {
    const accessValid = this.tokenService.isAccessTokenValid();
    const refreshToken = this.tokenService.getRefreshToken();

    if (accessValid) {
      this.hydrateUserFromToken();
      this.isAuthenticatedSubject.next(true);
      return;
    }

    if (refreshToken) {
      this.currentUserSubject.next(this.tokenService.getUserData());
      this.isAuthenticatedSubject.next(false);
      return;
    }

    this.tokenService.clear();
    this.currentUserSubject.next(null);
    this.isAuthenticatedSubject.next(false);
  }

  private hydrateUserFromToken(): void {
    const payload = this.tokenService.decodeAccessToken();

    if (!payload) {
      const storedUser = this.tokenService.getUserData();
      this.currentUserSubject.next(storedUser);
      return;
    }

    const user: AuthUser = {
      email: payload.email ?? '',
      user_id: payload.user_id,
      username: payload.username,
      first_name: payload.first_name,
      last_name: payload.last_name,
    };

    this.currentUserSubject.next(user);
    this.tokenService.saveUserData(user);
  }

  private mapHttpError(error: unknown): AuthError {
    if (!(error instanceof HttpErrorResponse)) {
      return { message: 'Unexpected error. Please try again.' };
    }

    const status = error.status;
    const backend = error.error;

    if (status === 0) {
      return {
        status,
        message: 'Cannot connect to the server. Please try again later.',
      };
    }

    if (status === 401) {
      return {
        status,
        message: 'Invalid email or password.',
      };
    }

    if (status === 403) {
      return {
        status,
        message: 'You do not have permission to perform this action.',
      };
    }

    if (status === 400 && backend && typeof backend === 'object') {
      const fieldErrors: Record<string, string> = {};

      Object.keys(backend).forEach((key) => {
        const value = backend[key];
        fieldErrors[key] = Array.isArray(value) ? value.join(', ') : String(value);
      });

      return {
        status,
        message: 'Please correct the highlighted fields.',
        fieldErrors,
      };
    }

    return {
      status,
      message: 'Something went wrong. Please try again.',
    };
  }
}
