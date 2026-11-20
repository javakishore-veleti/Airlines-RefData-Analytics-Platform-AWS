import { Routes } from '@angular/router';
import { authGuard } from './core/auth.guard';
import { ShellComponent } from './layout/shell.component';
import { SigninComponent } from './pages/signin.component';
import { SignupComponent } from './pages/signup.component';
import { HomeComponent } from './pages/home.component';
import { PlaceholderComponent } from './pages/placeholder.component';

export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'signin' },
  { path: 'signin', component: SigninComponent },
  { path: 'signup', component: SignupComponent },
  {
    path: 'app',
    component: ShellComponent,
    canActivate: [authGuard],
    children: [
      { path: '', pathMatch: 'full', redirectTo: 'home' },
      { path: 'home', component: HomeComponent },
      {
        path: 'browse',
        component: PlaceholderComponent,
        data: { title: 'Browse / filter', blurb: 'Lake browse lands in story #47.' },
      },
      {
        path: 'saved-views',
        component: PlaceholderComponent,
        data: { title: 'Saved views', blurb: 'Query / saved views land in story #48.' },
      },
    ],
  },
  { path: '**', redirectTo: 'signin' },
];
