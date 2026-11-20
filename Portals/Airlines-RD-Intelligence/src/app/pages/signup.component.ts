import { Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { PasswordModule } from 'primeng/password';
import { MessageModule } from 'primeng/message';
import { LucidePlane } from '@lucide/angular';
import { AuthService } from '../core/auth.service';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [
    FormsModule,
    RouterLink,
    ButtonModule,
    InputTextModule,
    PasswordModule,
    MessageModule,
    LucidePlane,
  ],
  template: `
    <div class="auth-page">
      <div class="auth-card">
        <div class="auth-brand">
          <svg lucidePlane [size]="28"></svg>
          <h1>Create Intelligence account</h1>
          <p>Registers via AccountService-API signup.</p>
        </div>
        <form (ngSubmit)="submit()">
          <label>
            Display name
            <input pInputText [(ngModel)]="displayName" name="displayName" />
          </label>
          <label>
            Username
            <input pInputText [(ngModel)]="username" name="username" required />
          </label>
          <label>
            Password
            <p-password
              [(ngModel)]="password"
              name="password"
              [feedback]="false"
              [toggleMask]="true"
              styleClass="w-full"
              inputStyleClass="w-full"
            />
          </label>
          @if (error()) {
            <p-message severity="error" [text]="error()!" />
          }
          <p-button type="submit" label="Sign up" [loading]="busy()" styleClass="w-full" />
        </form>
        <p class="hint"><a routerLink="/signin">Back to sign in</a></p>
      </div>
    </div>
  `,
  styles: [
    `
      .auth-page {
        min-height: 100vh;
        display: grid;
        place-items: center;
        background: var(--arfd-ice);
        padding: 1.5rem;
      }
      .auth-card {
        width: min(420px, 100%);
        background: var(--arfd-white);
        border: 1px solid var(--arfd-border);
        border-radius: 1rem;
        padding: 2rem;
      }
      .auth-brand {
        text-align: center;
        margin-bottom: 1.5rem;
        color: var(--arfd-sky);
      }
      .auth-brand h1 {
        margin: 0.5rem 0 0.25rem;
        font-size: 1.35rem;
        color: var(--arfd-navy);
      }
      .auth-brand p,
      .hint {
        color: var(--arfd-muted);
        font-size: 0.9rem;
      }
      form {
        display: grid;
        gap: 1rem;
      }
      label {
        display: grid;
        gap: 0.35rem;
        font-weight: 600;
        font-size: 0.85rem;
      }
      :host ::ng-deep .p-password,
      :host ::ng-deep .p-password-input {
        width: 100%;
      }
    `,
  ],
})
export class SignupComponent {
  displayName = '';
  username = '';
  password = '';
  readonly busy = signal(false);
  readonly error = signal<string | null>(null);

  constructor(
    private readonly auth: AuthService,
    private readonly router: Router,
  ) {}

  submit(): void {
    this.busy.set(true);
    this.error.set(null);
    this.auth.signup(this.username, this.password, this.displayName || this.username).subscribe((ok) => {
      this.busy.set(false);
      if (ok) {
        void this.router.navigateByUrl('/app/home');
      } else {
        this.error.set('Signup failed. Username may already exist or API is down.');
      }
    });
  }
}
