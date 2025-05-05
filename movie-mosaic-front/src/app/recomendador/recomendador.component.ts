import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-recomendador',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './recomendador.component.html',
  styleUrls: ['./recomendador.component.css']
})
export class RecomendadorComponent {
  userId: number = 1;
  nRecomendaciones: number = 5;
  recomendaciones: any[] = [];
  error: string = '';

  constructor(private http: HttpClient) {}

  obtenerRecomendaciones() {
    this.http.post<any>('http://localhost:8000/recomendar', {
      user_id: this.userId,
      n_recomendaciones: this.nRecomendaciones
    }).subscribe({
      next: res => {
        this.recomendaciones = res.recomendaciones;
        this.error = '';
      },
      error: err => {
        this.error = err.error.detail || 'Error desconocido';
        this.recomendaciones = [];
      }
    });
  }
}
