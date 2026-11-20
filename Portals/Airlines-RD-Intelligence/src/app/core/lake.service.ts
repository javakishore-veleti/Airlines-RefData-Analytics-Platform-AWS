import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';
import { environment } from '../../environments/environment';

export interface LakeRule {
  rule_id?: number;
  name?: string;
  status?: string;
  market_from?: string;
  market_to?: string;
  weight?: number;
  [key: string]: unknown;
}

@Injectable({ providedIn: 'root' })
export class LakeService {
  constructor(private readonly http: HttpClient) {}

  list(limit = 200): Observable<LakeRule[]> {
    return this.http
      .get<{ items: LakeRule[] }>(`${environment.masterDataApiBase}/lake/market-rules`, {
        params: { limit },
      })
      .pipe(map((r) => r.items ?? []));
  }
}
