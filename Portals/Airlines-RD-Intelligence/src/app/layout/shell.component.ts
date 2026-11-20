import { Component, signal } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { ButtonModule } from 'primeng/button';
import {
  LucidePlane,
  LucideLayoutDashboard,
  LucideSearch,
  LucideBookmark,
  LucideMenu,
} from '@lucide/angular';
import { AuthService } from '../core/auth.service';

@Component({
  selector: 'app-shell',
  standalone: true,
  imports: [
    RouterOutlet,
    RouterLink,
    RouterLinkActive,
    ButtonModule,
    LucidePlane,
    LucideLayoutDashboard,
    LucideSearch,
    LucideBookmark,
    LucideMenu,
  ],
  templateUrl: './shell.component.html',
  styleUrl: './shell.component.scss',
})
export class ShellComponent {
  readonly navOpen = signal(true);

  constructor(readonly auth: AuthService) {}

  toggleNav(): void {
    this.navOpen.update((v) => !v);
  }

  signout(): void {
    this.auth.signout();
  }
}
