import { Component } from '@angular/core';
import { PlaceholderComponent } from './placeholder.component';

@Component({
  selector: 'app-pipeline-nav',
  standalone: true,
  imports: [PlaceholderComponent],
  template: `<app-placeholder title="Pipeline health" blurb="CDC / lake health summary lands in story #42." />`,
})
export class PipelineNavComponent {}
