import { Component, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { InputNumberModule } from 'primeng/inputnumber';
import { DialogModule } from 'primeng/dialog';
import { MessageModule } from 'primeng/message';
import { MarketRule, MarketRulesService } from '../core/market-rules.service';

@Component({
  selector: 'app-market-rules-nav',
  standalone: true,
  imports: [FormsModule, TableModule, ButtonModule, InputTextModule, InputNumberModule, DialogModule, MessageModule],
  template: `
    <section class="panel">
      <div class="header-row">
        <div>
          <h2>Market rules</h2>
          <p>Operational MySQL reference data (MasterData-API).</p>
        </div>
        <div class="header-actions">
          <p-button label="Generate CDC" [outlined]="true" (onClick)="genCdc()" />
          <p-button label="Add rule" (onClick)="openCreate()" />
        </div>
      </div>
      @if (error()) { <p-message severity="error" [text]="error()!" /> }
      <p-table [value]="rules()" [loading]="loading()" styleClass="p-datatable-sm">
        <ng-template pTemplate="header">
          <tr>
            <th>ID</th><th>Name</th><th>From</th><th>To</th><th>Weight</th><th>Status</th><th></th>
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
            <td class="actions">
              <p-button label="Edit" [text]="true" (onClick)="openEdit(r)" />
              <p-button label="Deactivate" [text]="true" severity="danger" (onClick)="deactivate(r)" />
            </td>
          </tr>
        </ng-template>
      </p-table>
    </section>

    <p-dialog [(visible)]="dialogOpen" [header]="editingId ? 'Edit rule' : 'Add rule'" [modal]="true" [style]="{width:'30rem'}">
      <div class="form-grid">
        <label>Name <input pInputText [(ngModel)]="form.name" /></label>
        <label>From <input pInputText [(ngModel)]="form.market_from" /></label>
        <label>To <input pInputText [(ngModel)]="form.market_to" /></label>
        <label>Weight <p-inputNumber [(ngModel)]="form.weight" [min]="0" /></label>
        <label>Status <input pInputText [(ngModel)]="form.status" /></label>
      </div>
      <ng-template pTemplate="footer">
        <p-button label="Cancel" [text]="true" (onClick)="dialogOpen=false" />
        <p-button label="Save" (onClick)="save()" [loading]="saving()" />
      </ng-template>
    </p-dialog>
  `,
  styles: [`
    .panel { background: var(--arfd-white); border: 1px solid var(--arfd-border); border-radius: .85rem; padding: 1.25rem 1.5rem; }
    .header-row { display:flex; justify-content:space-between; gap:1rem; margin-bottom:1rem; }
    .header-actions { display:flex; gap:.5rem; }
    h2 { margin:0 0 .25rem; } p { margin:0; color: var(--arfd-muted); }
    .actions { display:flex; justify-content:flex-end; gap:.25rem; }
    .form-grid { display:grid; gap:.85rem; }
    label { display:grid; gap:.3rem; font-size:.85rem; font-weight:600; }
  `],
})
export class MarketRulesNavComponent implements OnInit {
  readonly rules = signal<MarketRule[]>([]);
  readonly loading = signal(false);
  readonly saving = signal(false);
  readonly error = signal<string | null>(null);
  dialogOpen = false;
  editingId: number | null = null;
  form = { name: '', market_from: 'ORD', market_to: 'SFO', weight: 1, status: 'ACTIVE' };

  constructor(private readonly api: MarketRulesService) {}

  ngOnInit(): void { this.reload(); }

  reload(): void {
    this.loading.set(true);
    this.error.set(null);
    this.api.list().subscribe({
      next: (rows) => { this.rules.set(rows); this.loading.set(false); },
      error: () => { this.loading.set(false); this.error.set('Could not load market rules. Is MasterData-API on :8110?'); },
    });
  }

  openCreate(): void {
    this.editingId = null;
    this.form = { name: '', market_from: 'ORD', market_to: 'SFO', weight: 1, status: 'ACTIVE' };
    this.dialogOpen = true;
  }

  openEdit(r: MarketRule): void {
    this.editingId = r.rule_id;
    this.form = {
      name: r.name,
      market_from: r.market_from,
      market_to: r.market_to,
      weight: r.weight,
      status: r.status,
    };
    this.dialogOpen = true;
  }

  save(): void {
    this.saving.set(true);
    const done = () => { this.saving.set(false); this.dialogOpen = false; this.reload(); };
    if (this.editingId) {
      this.api.update(this.editingId, this.form).subscribe({ next: done, error: () => this.saving.set(false) });
    } else {
      this.api.create(this.form).subscribe({ next: done, error: () => this.saving.set(false) });
    }
  }

  deactivate(r: MarketRule): void {
    if (!confirm(`Deactivate rule ${r.rule_id}?`)) return;
    this.api.deactivate(r.rule_id).subscribe({ next: () => this.reload() });
  }

  genCdc(): void {
    this.api.generateCdc(5).subscribe({
      next: () => this.reload(),
      error: () => this.error.set('CDC generate failed'),
    });
  }
}
