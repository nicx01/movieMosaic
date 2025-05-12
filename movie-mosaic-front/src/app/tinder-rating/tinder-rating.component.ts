import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { of, forkJoin } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Observable} from 'rxjs';

interface Pelicula {
  movieId: number;
  tmdbId?: number;
  title: string;
  posterUrl?: string;
}

interface Valoracion {
  movieId: number;
  rating: number;
}

@Component({
  selector: 'app-tinder-rating',
  standalone: true,
  imports: [CommonModule], 
  templateUrl: './tinder-rating.component.html',
  styleUrls: ['./tinder-rating.component.css']
})
export class TinderRatingComponent {
  peliculas: Pelicula[] = [];
  valoraciones: Valoracion[] = [];
  indiceActual = 0;
  maxValoraciones = 30;
  recomendaciones: any[] = [];
  private tmdbApiKey = 'a';
  usuario: string | null = null;
  constructor(private http: HttpClient) {
    this.usuario = localStorage.getItem('usuario');
    if (this.usuario) {
      console.log('Usuario:', this.usuario);
      const prev = localStorage.getItem('valoraciones_' + this.usuario);
      if (prev) {
        this.valoraciones = JSON.parse(prev);
        this.indiceActual = this.valoraciones.length;
      }
    }
    this.cargarPeliculasAleatorias();
  }

  cargarPeliculasAleatorias() {
    // Si tienes un endpoint para pelis aleatorias, úsalo. Si no, pide todas y baraja:
    this.http.get<any>('http://localhost:8000/peliculas_aleatorias?cantidad=30')
      .subscribe(res => {
        this.peliculas = res.peliculas;
        this.cargarPosters();
      },
      err => {
        console.error('Error al cargar películas:', err);
      });
  }

  cargarPosters() {
    const observables = this.peliculas.map(peli =>
      peli.tmdbId
        ? this.http.get<any>(`https://api.themoviedb.org/3/movie/${peli.tmdbId}?api_key=${this.tmdbApiKey}`)
            .pipe(
              catchError(() => of(null))
            )
        : of(null)
    );
    forkJoin(observables).subscribe(results => {
      this.peliculas = this.peliculas.map((peli, i) => {
        const result = results[i];
        if (result && result.poster_path) {
          peli.posterUrl = `https://image.tmdb.org/t/p/w300${result.poster_path}`;
        } else {
          console.log(`Sin imagen: movieId=${peli.movieId}, title="${peli.title}", tmdbId=${peli.tmdbId}`);
          peli.posterUrl = undefined;
        }
        return peli;
      });
    });
  }

  valorar(rating: number) {
    const peli = this.peliculas[this.indiceActual];
    this.valoraciones.push({ movieId: peli.movieId, rating });
    this.indiceActual++;
    if (this.usuario) {
      localStorage.setItem('valoraciones_' + this.usuario, JSON.stringify(this.valoraciones));
    }
  }

  enviarValoraciones() {
    this.http.post<any>('http://localhost:8000/recomendar_personalizado', {
      valoraciones: this.valoraciones,
      n_recomendaciones: 10
    }).subscribe(res => {
      console.log(this.valoraciones.length);
      // Carga los posters de las recomendaciones
      const recs = res.recomendaciones;
      const obs = recs.map((rec: any) =>
        rec.tmdbId
          ? this.http.get<any>(`https://api.themoviedb.org/3/movie/${rec.tmdbId}?api_key=${this.tmdbApiKey}`)
              .pipe(
                catchError(() => of(null))
              )
          : of(null)
      );
      forkJoin(obs as Observable<any>[]).subscribe((results: any[]) => {
        this.recomendaciones = recs.map((rec: any, i: number) => {
          const result = results[i];
          if (result && result.poster_path) {
            rec.posterUrl = `https://image.tmdb.org/t/p/w300${result.poster_path}`;
          } else {
            console.log(`Sin imagen: movieId=${rec.movieId}, title="${rec.title}", tmdbId=${rec.tmdbId}`);
            rec.posterUrl = undefined;
          }
          return rec;
        });
      });
    });
  }
  cargarMasPeliculas() {
    this.indiceActual = 0;
    this.cargarPeliculasAleatorias();
  }  
}
