import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, catchError, forkJoin, map, of } from 'rxjs';
import { environment } from '../../environments/environment';

export interface HealthProbe {
  name: string;
  ok: boolean;
  detail: string;
}

@Injectable({ providedIn: 'root' })
export class PipelineService {
  constructor(private readonly http: HttpClient) {}

  summary(): Observable<HealthProbe[]> {
    const master$ = this.http.get<{ status: string; mysql?: boolean; detail?: string }>(
      `${environment.masterDataApiBase}/health`,
    ).pipe(
      map((r) => ({
        name: 'MasterData-API',
        ok: r.status === 'ok',
        detail: r.mysql ? 'MySQL reachable' : r.detail || r.status,
      })),
      catchError((e) => of({ name: 'MasterData-API', ok: false, detail: String(e.message || e) })),
    );

    const account$ = this.http.get<{ status: string; mysql?: boolean; detail?: string }>(
      `${environment.accountApiBase}/health`,
    ).pipe(
      map((r) => ({
        name: 'AccountService-API',
        ok: r.status === 'ok',
        detail: r.mysql ? 'MySQL reachable' : r.detail || r.status,
      })),
      catchError((e) => of({ name: 'AccountService-API', ok: false, detail: String(e.message || e) })),
    );

    const lake$ = this.http.get<{ count: number }>(`${environment.masterDataApiBase}/lake/market-rules`, {
      params: { limit: 5 },
    }).pipe(
      map((r) => ({
        name: 'Lake market_rule',
        ok: true,
        detail: `${r.count} object(s) visible via lake read API`,
      })),
      catchError((e) => of({ name: 'Lake market_rule', ok: false, detail: String(e.message || e) })),
    );

    return forkJoin([master$, account$, lake$]);
  }
}
