import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-usuario',
  standalone: true,
  imports: [CommonModule, FormsModule], 
  template: `
    <div class="card">
      <h2>¡Bienvenido a Movie Mosaic!</h2>
      <form (ngSubmit)="guardarUsuario()" #f="ngForm">
        <input
          type="text"
          placeholder="Introduce tu nombre de usuario"
          [(ngModel)]="usuario"
          name="usuario"
          required
          style="margin-bottom:10px; padding:8px; width:90%;"
        />
        <br/>
        <button type="submit" [disabled]="!usuario">Entrar</button>
      </form>
    </div>
  `
})
export class UsuarioComponent {
  usuario = '';

  constructor(private router: Router) {}

  guardarUsuario() {
    localStorage.setItem('usuario', this.usuario);
    this.router.navigate(['/tinder-rating']);
  }
}
