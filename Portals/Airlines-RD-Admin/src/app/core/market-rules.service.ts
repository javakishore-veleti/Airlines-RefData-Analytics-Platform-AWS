import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { environment } from '../../environments/environment';

export interface MarketRule {
  rule_id: number;
  name: string;
  weight: number;
  status: string;
  market_from: string;
  market_to: string;
  updated_at?: string;
}

@Injectable({ providedIn: 'root' })
export class MarketRulesService {
  constructor(private readonly http: HttpClient) {}

  list(limit = 100): Observable<MarketRule[]> {
    return this.http
      .get<{ items: MarketRule[] }>(`${environment.masterDataApiBase}/admin/market-rules`, {
        params: { limit },
      })
      .pipe(map((r) => r.items ?? []));
  }

  create(body: Partial<MarketRule> & { name: string }): Observable<{ rule_id: number }> {
    return this.http.post<{ rule_id: number }>(`${environment.masterDataApiBase}/admin/market-rules`, body);
  }

  update(ruleId: number, body: Partial<MarketRule>): Observable<{ ok: boolean }> {
    return this.http.put<{ ok: boolean }>(
      `${environment.masterDataApiBase}/admin/market-rules/${ruleId}`,
      body,
    );
  }

  deactivate(ruleId: number): Observable<{ ok: boolean }> {
    return this.http.post<{ ok: boolean }>(
      `${environment.masterDataApiBase}/admin/market-rules/${ruleId}/deactivate`,
      {},
    );
  }

  generateCdc(count: number): Observable<unknown> {
    return this.http.post(`${environment.masterDataApiBase}/admin/cdc/generate`, { count });
  }
}
