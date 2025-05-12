import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { forkJoin, of } from 'rxjs';
import { catchError } from 'rxjs/operators';
interface Recomendacion {
  movieId: number;
  title: string;
  score: number;
  tmdbId?: number;
  posterUrl?: string;
}

@Component({
  selector: 'app-recomendador',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './recomendador.component.html',
  styleUrls: ['./recomendador.component.css']
})
export class RecomendadorComponent {
  private tmdbApiKey = 'a';
  userId: number = 1;
  nRecomendaciones: number = 5;
  recomendaciones: Recomendacion[] = [];
  error: string = '';

  constructor(private http: HttpClient) {}

  obtenerRecomendaciones() {
    this.http.post<{recomendaciones: Recomendacion[]}>('http://localhost:8000/recomendar', {
      user_id: this.userId,
      n_recomendaciones: this.nRecomendaciones
    }).subscribe({
      next: res => {
        const recomendaciones: Recomendacion[] = res.recomendaciones;

        const observables = recomendaciones.map((rec: Recomendacion) =>
          rec.tmdbId
            ? this.buscarPosterPorId(rec.tmdbId).pipe(
                catchError(err => {
                  console.log(`Error al buscar imagen para tmdbId ${rec.tmdbId}:`, err);
                  return of(null); // Devuelve null si falla
                })
              )
            : of(null)
        );

        forkJoin(observables).subscribe((results: any[]) => {
          this.recomendaciones = recomendaciones.map((rec: Recomendacion, i: number) => {
            const result = results[i];
            //console.log(`Sin imagen: movieId=${rec.movieId}, title="${rec.title}", tmdbId=${rec.tmdbId}`);
            if (result && result.poster_path) {
              rec.posterUrl = `https://image.tmdb.org/t/p/w300${result.poster_path}`;
              console.log("nico");
            } else {
              rec.posterUrl = undefined;
            }
            return rec;
          });
          this.error = '';
        }, err => {
          this.error = 'Error al buscar imágenes en TMDb';
          this.recomendaciones = recomendaciones; 
        });
      },
      error: err => {
        this.error = err.error?.detail || 'Error desconocido';
        this.recomendaciones = [];
      }
    });
  }

  buscarPosterPorId(tmdbId: number) {
    const url = `https://api.themoviedb.org/3/movie/${tmdbId}?api_key=${this.tmdbApiKey}`;
    return this.http.get<any>(url);
  }
}
