import { Routes } from '@angular/router';
import { authGuard } from './core/auth.guard';
import { ShellComponent } from './layout/shell.component';
import { SigninComponent } from './pages/signin.component';
import { SignupComponent } from './pages/signup.component';
import { HomeComponent } from './pages/home.component';
import { UsersNavComponent } from './pages/users-nav.component';
import { MarketRulesNavComponent } from './pages/market-rules-nav.component';
import { PipelineNavComponent } from './pages/pipeline-nav.component';

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
      { path: 'users', component: UsersNavComponent },
      { path: 'market-rules', component: MarketRulesNavComponent },
      { path: 'pipeline', component: PipelineNavComponent },
    ],
  },
  { path: '**', redirectTo: 'signin' },
];
