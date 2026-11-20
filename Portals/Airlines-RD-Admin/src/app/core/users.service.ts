import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { environment } from '../../environments/environment';

export interface AccountUser {
  user_id: number;
  username: string;
  display_name: string;
  role: string;
}

@Injectable({ providedIn: 'root' })
export class UsersService {
  constructor(private readonly http: HttpClient) {}

  list(): Observable<AccountUser[]> {
    return this.http
      .get<{ users: AccountUser[] }>(`${environment.accountApiBase}/users`)
      .pipe(map((r) => r.users ?? []));
  }

  create(body: {
    username: string;
    password: string;
    display_name: string;
    role: string;
  }): Observable<{ ok: boolean; user_id: number }> {
    return this.http.post<{ ok: boolean; user_id: number }>(
      `${environment.accountApiBase}/users`,
      body,
    );
  }

  update(
    userId: number,
    body: { display_name: string; role: string; password?: string },
  ): Observable<{ ok: boolean }> {
    return this.http.put<{ ok: boolean }>(`${environment.accountApiBase}/users/${userId}`, body);
  }

  remove(userId: number): Observable<{ ok: boolean }> {
    return this.http.delete<{ ok: boolean }>(`${environment.accountApiBase}/users/${userId}`);
  }
}
