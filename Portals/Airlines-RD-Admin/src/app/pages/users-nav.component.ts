import { Component, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { DialogModule } from 'primeng/dialog';
import { SelectModule } from 'primeng/select';
import { MessageModule } from 'primeng/message';
import { AccountUser, UsersService } from '../core/users.service';

@Component({
  selector: 'app-users-nav',
  standalone: true,
  imports: [
    FormsModule,
    TableModule,
    ButtonModule,
    InputTextModule,
    DialogModule,
    SelectModule,
    MessageModule,
  ],
  template: `
    <section class="panel">
      <div class="header-row">
        <div>
          <h2>User Management</h2>
          <p>Operators managed through AccountService-API.</p>
        </div>
        <p-button label="Add user" icon="pi pi-plus" (onClick)="openCreate()" />
      </div>

      @if (error()) {
        <p-message severity="error" [text]="error()!" />
      }

      <p-table [value]="users()" [loading]="loading()" styleClass="p-datatable-sm">
        <ng-template pTemplate="header">
          <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Display name</th>
            <th>Role</th>
            <th></th>
          </tr>
        </ng-template>
        <ng-template pTemplate="body" let-u>
          <tr>
            <td>{{ u.user_id }}</td>
            <td>{{ u.username }}</td>
            <td>{{ u.display_name }}</td>
            <td>{{ u.role }}</td>
            <td class="actions">
              <p-button label="Edit" [text]="true" (onClick)="openEdit(u)" />
              <p-button label="Deactivate" [text]="true" severity="danger" (onClick)="deactivate(u)" />
            </td>
          </tr>
        </ng-template>
        <ng-template pTemplate="emptymessage">
          <tr>
            <td colspan="5">No users yet — start AccountService or seed via sign-in.</td>
          </tr>
        </ng-template>
      </p-table>
    </section>

    <p-dialog
      [(visible)]="dialogOpen"
      [header]="editingId ? 'Edit user' : 'Add user'"
      [modal]="true"
      [style]="{ width: '28rem' }"
    >
      <div class="form-grid">
        @if (!editingId) {
          <label>
            Username
            <input pInputText [(ngModel)]="form.username" />
          </label>
          <label>
            Password
            <input pInputText type="password" [(ngModel)]="form.password" />
          </label>
        } @else {
          <label>
            New password (optional)
            <input pInputText type="password" [(ngModel)]="form.password" />
          </label>
        }
        <label>
          Display name
          <input pInputText [(ngModel)]="form.display_name" />
        </label>
        <label>
          Role
          <p-select [options]="roles" [(ngModel)]="form.role" optionLabel="label" optionValue="value" />
        </label>
      </div>
      <ng-template pTemplate="footer">
        <p-button label="Cancel" [text]="true" (onClick)="dialogOpen = false" />
        <p-button label="Save" (onClick)="save()" [loading]="saving()" />
      </ng-template>
    </p-dialog>
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
        align-items: flex-start;
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
      .actions {
        display: flex;
        gap: 0.25rem;
        justify-content: flex-end;
      }
      .form-grid {
        display: grid;
        gap: 0.85rem;
      }
      label {
        display: grid;
        gap: 0.3rem;
        font-size: 0.85rem;
        font-weight: 600;
      }
    `,
  ],
})
export class UsersNavComponent implements OnInit {
  readonly users = signal<AccountUser[]>([]);
  readonly loading = signal(false);
  readonly saving = signal(false);
  readonly error = signal<string | null>(null);
  dialogOpen = false;
  editingId: number | null = null;
  form = { username: '', password: '', display_name: '', role: 'operator' };
  readonly roles = [
    { label: 'operator', value: 'operator' },
    { label: 'admin', value: 'admin' },
  ];

  constructor(private readonly usersApi: UsersService) {}

  ngOnInit(): void {
    this.reload();
  }

  reload(): void {
    this.loading.set(true);
    this.error.set(null);
    this.usersApi.list().subscribe({
      next: (rows) => {
        this.users.set(rows);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
        this.error.set('Could not load users. Is AccountService-API on :8111?');
      },
    });
  }

  openCreate(): void {
    this.editingId = null;
    this.form = { username: '', password: '', display_name: '', role: 'operator' };
    this.dialogOpen = true;
  }

  openEdit(u: AccountUser): void {
    this.editingId = u.user_id;
    this.form = {
      username: u.username,
      password: '',
      display_name: u.display_name,
      role: u.role,
    };
    this.dialogOpen = true;
  }

  save(): void {
    this.saving.set(true);
    const done = () => {
      this.saving.set(false);
      this.dialogOpen = false;
      this.reload();
    };
    if (this.editingId) {
      this.usersApi
        .update(this.editingId, {
          display_name: this.form.display_name,
          role: this.form.role,
          password: this.form.password || undefined,
        })
        .subscribe({ next: done, error: () => this.saving.set(false) });
    } else {
      this.usersApi
        .create({
          username: this.form.username,
          password: this.form.password,
          display_name: this.form.display_name || this.form.username,
          role: this.form.role,
        })
        .subscribe({ next: done, error: () => this.saving.set(false) });
    }
  }

  deactivate(u: AccountUser): void {
    // AccountService has delete; treat as deactivate for Admin UX.
    if (!confirm(`Remove user ${u.username}?`)) {
      return;
    }
    this.usersApi.remove(u.user_id).subscribe({ next: () => this.reload() });
  }
}
