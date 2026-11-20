import { Component, Input } from '@angular/core';

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
  @Input({ required: true }) title!: string;
  @Input({ required: true }) blurb!: string;
}
