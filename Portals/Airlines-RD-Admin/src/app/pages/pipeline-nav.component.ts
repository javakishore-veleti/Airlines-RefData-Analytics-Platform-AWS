import { Component, OnInit, signal } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { TagModule } from 'primeng/tag';
import { HealthProbe, PipelineService } from '../core/pipeline.service';

@Component({
  selector: 'app-pipeline-nav',
  standalone: true,
  imports: [ButtonModule, TagModule],
  template: `
    <section class="panel">
      <div class="header-row">
        <div>
          <h2>Pipeline health</h2>
          <p>Local MasterData, AccountService, and lake read probes.</p>
        </div>
        <p-button label="Refresh" [loading]="loading()" (onClick)="reload()" />
      </div>
      <div class="cards">
        @for (p of probes(); track p.name) {
          <article class="card">
            <div class="card-top">
              <h3>{{ p.name }}</h3>
              <p-tag [severity]="p.ok ? 'success' : 'danger'" [value]="p.ok ? 'OK' : 'Down'" />
            </div>
            <p>{{ p.detail }}</p>
          </article>
        }
      </div>
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
      .header-row {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 1rem;
      }
      h2 {
        margin: 0 0 0.25rem;
      }
      p {
        margin: 0;
        color: var(--arfd-muted);
      }
      .cards {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 0.85rem;
      }
      .card {
        border: 1px solid var(--arfd-border);
        border-radius: 0.75rem;
        padding: 1rem;
        background: var(--arfd-ice);
      }
      .card-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
      }
      h3 {
        margin: 0;
        font-size: 1rem;
      }
    `,
  ],
})
export class PipelineNavComponent implements OnInit {
  readonly probes = signal<HealthProbe[]>([]);
  readonly loading = signal(false);

  constructor(private readonly pipeline: PipelineService) {}

  ngOnInit(): void {
    this.reload();
  }

  reload(): void {
    this.loading.set(true);
    this.pipeline.summary().subscribe((rows) => {
      this.probes.set(rows);
      this.loading.set(false);
    });
  }
}
