import { Injectable, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, tap, catchError, of, map } from 'rxjs';
import { environment } from '../../environments/environment';

export interface AuthSession {
  token: string;
  username: string;
  role: string;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly storageKey = 'arfd.admin.session';
  private readonly session = signal<AuthSession | null>(this.readSession());

  readonly current = this.session.asReadonly();
  readonly isSignedIn = computed(() => !!this.session()?.token);

  constructor(
    private readonly http: HttpClient,
    private readonly router: Router,
  ) {}

  signin(username: string, password: string): Observable<boolean> {
    return this.http
      .post<{ ok: boolean; token: string; username: string; role: string }>(
        `${environment.accountApiBase}/auth/signin`,
        { username, password },
      )
      .pipe(
        tap((res) => this.persist({ token: res.token, username: res.username, role: res.role })),
        map(() => true),
        catchError(() => of(false)),
      );
  }

  signup(username: string, password: string, displayName: string): Observable<boolean> {
    return this.http
      .post<{ ok: boolean; token: string; username: string; role: string }>(
        `${environment.accountApiBase}/auth/signup`,
        { username, password, display_name: displayName },
      )
      .pipe(
        tap((res) => this.persist({ token: res.token, username: res.username, role: res.role })),
        map(() => true),
        catchError(() => of(false)),
      );
  }

  signout(): void {
    const token = this.session()?.token;
    if (token) {
      this.http.post(`${environment.accountApiBase}/auth/signout`, { token }).subscribe({
        error: () => undefined,
      });
    }
    localStorage.removeItem(this.storageKey);
    this.session.set(null);
    void this.router.navigateByUrl('/signin');
  }

  private persist(s: AuthSession): void {
    localStorage.setItem(this.storageKey, JSON.stringify(s));
    this.session.set(s);
  }

  private readSession(): AuthSession | null {
    try {
      const raw = localStorage.getItem(this.storageKey);
      return raw ? (JSON.parse(raw) as AuthSession) : null;
    } catch {
      return null;
    }
  }
}
