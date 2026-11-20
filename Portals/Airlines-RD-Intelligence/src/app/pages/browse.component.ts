import { Component, OnInit, computed, signal } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { TableModule } from 'primeng/table';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { MessageModule } from 'primeng/message';
import { LakeRule, LakeService } from '../core/lake.service';

@Component({
  selector: 'app-browse',
  standalone: true,
  imports: [FormsModule, TableModule, InputTextModule, ButtonModule, MessageModule],
  template: `
    <section class="panel">
      <div class="header-row">
        <div>
          <h2>Browse / filter</h2>
          <p>Lake-backed market_rule objects from MasterData-API.</p>
        </div>
        <p-button label="Refresh" [loading]="loading()" (onClick)="reload()" />
      </div>
      <div class="filters">
        <input pInputText placeholder="From airport" [ngModel]="fromFilter()" (ngModelChange)="fromFilter.set($event)" />
        <input pInputText placeholder="To airport" [ngModel]="toFilter()" (ngModelChange)="toFilter.set($event)" />
        <input pInputText placeholder="Status" [ngModel]="statusFilter()" (ngModelChange)="statusFilter.set($event)" />
        <input pInputText placeholder="Name contains" [ngModel]="nameFilter()" (ngModelChange)="nameFilter.set($event)" />
      </div>
      @if (error()) {
        <p-message severity="warn" [text]="error()!" />
      }
      <p-table [value]="filtered()" [loading]="loading()" styleClass="p-datatable-sm">
        <ng-template pTemplate="header">
          <tr>
            <th>ID</th><th>Name</th><th>From</th><th>To</th><th>Weight</th><th>Status</th>
          </tr>
        </ng-template>
        <ng-template pTemplate="body" let-r>
          <tr>
            <td>{{ r.rule_id }}</td>
            <td>{{ r.name }}</td>
            <td>{{ r.market_from }}</td>
            <td>{{ r.market_to }}</td>
            <td>{{ r.weight }}</td>
            <td>{{ r.status }}</td>
          </tr>
        </ng-template>
        <ng-template pTemplate="emptymessage">
          <tr><td colspan="6">No lake rows match filters (or lake is empty).</td></tr>
        </ng-template>
      </p-table>
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
        margin-bottom: 1rem;
      }
      h2 {
        margin: 0 0 0.25rem;
      }
      p {
        margin: 0;
        color: var(--arfd-muted);
      }
      .filters {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 0.5rem;
        margin-bottom: 1rem;
      }
    `,
  ],
})
export class BrowseComponent implements OnInit {
  readonly rows = signal<LakeRule[]>([]);
  readonly loading = signal(false);
  readonly error = signal<string | null>(null);
  readonly fromFilter = signal('');
  readonly toFilter = signal('');
  readonly statusFilter = signal('');
  readonly nameFilter = signal('');

  readonly filtered = computed(() => {
    const from = this.fromFilter().trim().toUpperCase();
    const to = this.toFilter().trim().toUpperCase();
    const status = this.statusFilter().trim().toUpperCase();
    const name = this.nameFilter().trim().toLowerCase();
    return this.rows().filter((r) => {
      if (from && String(r.market_from || '').toUpperCase() !== from) return false;
      if (to && String(r.market_to || '').toUpperCase() !== to) return false;
      if (status && String(r.status || '').toUpperCase() !== status) return false;
      if (name && !String(r.name || '').toLowerCase().includes(name)) return false;
      return true;
    });
  });

  constructor(private readonly lake: LakeService, private readonly route: ActivatedRoute) {}

  ngOnInit(): void {
    const q = this.route.snapshot.queryParamMap;
    this.fromFilter.set(q.get('from') || '');
    this.toFilter.set(q.get('to') || '');
    this.statusFilter.set(q.get('status') || '');
    this.nameFilter.set(q.get('name') || '');
    this.reload();
  }

  reload(): void {
    this.loading.set(true);
    this.error.set(null);
    this.lake.list().subscribe({
      next: (items) => {
        this.rows.set(items);
        this.loading.set(false);
        if (!items.length) {
          this.error.set('Lake returned 0 rows — run CDC apply or Admin Generate CDC first.');
        }
      },
      error: () => {
        this.loading.set(false);
        this.error.set('Could not load lake data. Is MasterData-API on :8110?');
      },
    });
  }
}
