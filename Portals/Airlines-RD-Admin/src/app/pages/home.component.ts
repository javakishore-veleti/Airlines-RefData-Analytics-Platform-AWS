import { Component } from '@angular/core';

@Component({
  selector: 'app-home',
  standalone: true,
  template: `
    <section class="panel">
      <h2>Overview</h2>
      <p>Manage market rules, watch CDC pipeline health, and administer users.</p>
      <ul>
        <li>Market rules UI — story #41</li>
        <li>Pipeline health — story #42</li>
        <li>User Management — story #61</li>
      </ul>
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
      h2 {
        margin: 0 0 0.5rem;
      }
      p,
      li {
        color: var(--arfd-muted);
      }
    `,
  ],
})
export class HomeComponent {}
