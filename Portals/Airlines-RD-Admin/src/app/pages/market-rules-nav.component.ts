import { Component } from '@angular/core';
import { PlaceholderComponent } from './placeholder.component';

@Component({
  selector: 'app-market-rules-nav',
  standalone: true,
  imports: [PlaceholderComponent],
  template: `<app-placeholder title="Market rules" blurb="Admin market-rule management lands in story #41." />`,
})
export class MarketRulesNavComponent {}
