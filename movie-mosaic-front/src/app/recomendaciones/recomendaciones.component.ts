import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { of, forkJoin, Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Component({
  selector: 'app-recomendaciones',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './recomendaciones.component.html',
  styleUrls: ['./recomendaciones.component.css']
})
export class RecomendacionesComponent implements OnInit {
  usuario: string | null = null;
  recomendaciones: any[] = [];
  private tmdbApiKey = 'a';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.usuario = localStorage.getItem('usuario');
    this.loadRecomendaciones();
  }

  refresh() {
    this.loadRecomendaciones();
  }

  private loadRecomendaciones() {
    if (!this.usuario) return;
    const gustos = localStorage.getItem('valoraciones_' + this.usuario);
    console.log('Gustos:', gustos);
    if (!gustos) {
      this.recomendaciones = [];
      return;
    }
    this.recomendaciones = []; // Para mostrar el loading si quieres
    this.http.post<any>('http://localhost:8000/recomendar_personalizado', {
      valoraciones: JSON.parse(gustos),
      n_recomendaciones: 20
    }).subscribe(res => {
      const recs = res.recomendaciones;
      const obs = recs.map((rec: any) =>
        rec.tmdbId
          ? this.http.get<any>(`https://api.themoviedb.org/3/movie/${rec.tmdbId}?api_key=${this.tmdbApiKey}`)
              .pipe(catchError(() => of(null)))
          : of(null)
      );
      forkJoin(obs as Observable<any>[]).subscribe((results: any[]) => {
        this.recomendaciones = recs.map((rec: any, i: number) => {
          const result = results[i];
          rec.posterUrl = (result && result.poster_path)
            ? `https://image.tmdb.org/t/p/w300${result.poster_path}`
            : undefined;
          return rec;
        });
      });
    });
  }
}
