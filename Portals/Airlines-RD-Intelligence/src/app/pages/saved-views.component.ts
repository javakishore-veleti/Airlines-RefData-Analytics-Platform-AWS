import { Component, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { TableModule } from 'primeng/table';

export interface SavedView {
  id: string;
  name: string;
  from: string;
  to: string;
  status: string;
  nameContains: string;
}

const STORAGE_KEY = 'arfd.intelligence.savedViews';

@Component({
  selector: 'app-saved-views',
  standalone: true,
  imports: [FormsModule, ButtonModule, InputTextModule, TableModule],
  template: `
    <section class="panel">
      <h2>Saved views</h2>
      <p>Persist browse filters locally for analysts (Phase 1 — browser storage).</p>

      <div class="form-grid">
        <input pInputText placeholder="View name" [(ngModel)]="draft.name" />
        <input pInputText placeholder="From" [(ngModel)]="draft.from" />
        <input pInputText placeholder="To" [(ngModel)]="draft.to" />
        <input pInputText placeholder="Status" [(ngModel)]="draft.status" />
        <input pInputText placeholder="Name contains" [(ngModel)]="draft.nameContains" />
        <p-button label="Save view" (onClick)="save()" />
      </div>

      <p-table [value]="views()" styleClass="p-datatable-sm">
        <ng-template pTemplate="header">
          <tr>
            <th>Name</th><th>From</th><th>To</th><th>Status</th><th>Contains</th><th></th>
          </tr>
        </ng-template>
        <ng-template pTemplate="body" let-v>
          <tr>
            <td>{{ v.name }}</td>
            <td>{{ v.from || '—' }}</td>
            <td>{{ v.to || '—' }}</td>
            <td>{{ v.status || '—' }}</td>
            <td>{{ v.nameContains || '—' }}</td>
            <td class="actions">
              <p-button label="Open" [text]="true" (onClick)="open(v)" />
              <p-button label="Delete" [text]="true" severity="danger" (onClick)="remove(v)" />
            </td>
          </tr>
        </ng-template>
        <ng-template pTemplate="emptymessage">
          <tr><td colspan="6">No saved views yet.</td></tr>
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
      h2 {
        margin: 0 0 0.25rem;
      }
      p {
        color: var(--arfd-muted);
        margin: 0 0 1rem;
      }
      .form-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 0.5rem;
        margin-bottom: 1rem;
        align-items: center;
      }
      .actions {
        display: flex;
        justify-content: flex-end;
        gap: 0.25rem;
      }
    `,
  ],
})
export class SavedViewsComponent implements OnInit {
  readonly views = signal<SavedView[]>([]);
  draft = { name: '', from: '', to: '', status: '', nameContains: '' };

  constructor(private readonly router: Router) {}

  ngOnInit(): void {
    this.views.set(this.read());
  }

  save(): void {
    if (!this.draft.name.trim()) {
      return;
    }
    const next: SavedView = {
      id: crypto.randomUUID(),
      name: this.draft.name.trim(),
      from: this.draft.from.trim(),
      to: this.draft.to.trim(),
      status: this.draft.status.trim(),
      nameContains: this.draft.nameContains.trim(),
    };
    const all = [...this.views(), next];
    localStorage.setItem(STORAGE_KEY, JSON.stringify(all));
    this.views.set(all);
    this.draft = { name: '', from: '', to: '', status: '', nameContains: '' };
  }

  open(v: SavedView): void {
    void this.router.navigate(['/app/browse'], {
      queryParams: {
        from: v.from || null,
        to: v.to || null,
        status: v.status || null,
        name: v.nameContains || null,
      },
    });
  }

  remove(v: SavedView): void {
    const all = this.views().filter((x) => x.id !== v.id);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(all));
    this.views.set(all);
  }

  private read(): SavedView[] {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]') as SavedView[];
    } catch {
      return [];
    }
  }
}
