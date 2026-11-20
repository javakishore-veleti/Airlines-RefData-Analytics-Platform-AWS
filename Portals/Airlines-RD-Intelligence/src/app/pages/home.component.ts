import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [RouterLink],
  template: `
    <section class="panel">
      <h2>Intelligence overview</h2>
      <p>Browse lake-backed reference data and save analyst views.</p>
      <ul>
        <li><a routerLink="/app/browse">Browse / filter</a></li>
        <li><a routerLink="/app/saved-views">Saved views</a></li>
      </ul>
      <p class="meta">AccountService: <code>{{ account }}</code> · MasterData: <code>{{ master }}</code></p>
    </section>
  `,
  styles: [`
    .panel { background: var(--arfd-white); border: 1px solid var(--arfd-border); border-radius: .85rem; padding: 1.25rem 1.5rem; }
    h2 { margin: 0 0 .5rem; }
    p, li { color: var(--arfd-muted); }
    .meta { margin-top: 1rem; font-size: .85rem; }
    code { background: #e0f2fe; padding: .1rem .35rem; border-radius: .25rem; }
  `],
})
export class HomeComponent {
  readonly account = environment.accountApiBase;
  readonly master = environment.masterDataApiBase;
}
