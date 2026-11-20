import { Component, inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-placeholder',
  standalone: true,
  template: `
    <section class="panel">
      <h2>{{ title }}</h2>
      <p>{{ blurb }}</p>
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
      p {
        color: var(--arfd-muted);
        margin: 0;
      }
    `,
  ],
})
export class PlaceholderComponent {
  private readonly route = inject(ActivatedRoute);
  readonly title = this.route.snapshot.data['title'] ?? 'Coming soon';
  readonly blurb = this.route.snapshot.data['blurb'] ?? '';
}
