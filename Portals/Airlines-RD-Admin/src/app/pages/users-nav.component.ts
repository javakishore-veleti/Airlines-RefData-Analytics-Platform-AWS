import { Component } from '@angular/core';
import { PlaceholderComponent } from './placeholder.component';

@Component({
  selector: 'app-users-nav',
  standalone: true,
  imports: [PlaceholderComponent],
  template: `<app-placeholder title="User Management" blurb="CRUD against AccountService-API lands in story #61." />`,
})
export class UsersNavComponent {}
