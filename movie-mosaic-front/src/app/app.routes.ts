import { Routes } from '@angular/router';
import { UsuarioComponent } from './usuario/usuario.component';
import { TinderRatingComponent } from './tinder-rating/tinder-rating.component';
import { RecomendadorComponent } from './recomendador/recomendador.component';
import { RecomendacionesComponent } from './recomendaciones/recomendaciones.component'
export const routes: Routes = [
    { path: '', redirectTo: 'usuario', pathMatch: 'full' },
    { path: 'usuario', component: UsuarioComponent },
    { path: 'tinder-rating', component: TinderRatingComponent },
    { path: 'recomendador', component: RecomendadorComponent },
    { path: 'recomendaciones', component: RecomendacionesComponent }
];