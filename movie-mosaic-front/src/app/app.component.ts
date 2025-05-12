import { Component } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';
@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet,RouterLink, RouterLinkActive],
  template: `
  <nav style="text-align:center; margin-bottom:20px;">
  <a routerLink="/tinder-rating">Valorar películas</a> |
  <a routerLink="/recomendaciones">Ver recomendaciones</a>
</nav>

    <div style="text-align:center; margin: 20px;">
      <img src="assets/logo.png" alt="Logo Movie Mosaic" style="width: 200px;">
    </div>
    <router-outlet></router-outlet>
  `
})
export class AppComponent {}
