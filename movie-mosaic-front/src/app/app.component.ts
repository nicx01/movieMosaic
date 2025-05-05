import { Component } from '@angular/core';
import { RecomendadorComponent } from './recomendador/recomendador.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RecomendadorComponent],
  template: `<app-recomendador></app-recomendador>`
})
export class AppComponent {
  title = 'movie-mosaic-front';
}
