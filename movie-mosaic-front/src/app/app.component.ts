import { Component } from '@angular/core';
import { RecomendadorComponent } from './recomendador/recomendador.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RecomendadorComponent],
  template: `
    <div style="text-align:center; margin: 20px;">
      <img src="assets/logo.png" alt="Logo Movie Mosaic" style="width: 200px;">
    </div>
    <app-recomendador></app-recomendador>
  `
})
export class AppComponent {}
