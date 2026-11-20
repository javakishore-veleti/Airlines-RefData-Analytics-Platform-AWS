import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [RouterLink],
  template: `
    <section class="panel">
      <h2>Overview</h2>
      <p>Admin is wired to local MasterData-API and AccountService-API.</p>
      <ul>
        <li><a routerLink="/app/market-rules">Market rules</a> → {{ master }}</li>
        <li><a routerLink="/app/pipeline">Pipeline health</a> → health + lake probes</li>
        <li><a routerLink="/app/users">User Management</a> → {{ account }}</li>
      </ul>
      <p class="meta">AccountService: <code>{{ account }}</code> · MasterData: <code>{{ master }}</code></p>
    </section>
  `,
  styles: [
    `
      .panel {
        background: var(--arfd-white);
        border: 1px solid var(--arfd-border);
        border-radius: 0.85rem;
        padding: 1.25rem 1.5rem;
      }
      h2 { margin: 0 0 0.5rem; }
      p, li { color: var(--arfd-muted); }
      .meta { margin-top: 1rem; font-size: 0.85rem; }
      code { background: #e0f2fe; padding: 0.1rem 0.35rem; border-radius: 0.25rem; }
    `,
  ],
})
export class HomeComponent {
  readonly account = environment.accountApiBase;
  readonly master = environment.masterDataApiBase;
}
