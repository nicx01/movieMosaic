from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List
from surprise import dump
import pandas as pd
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API Recomendador MovieMosaic")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # O ["*"] para desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


MODELO_PATH = 'modelo_entrenado_grande.pkl'
MOVIES_PATH = 'movies.csv'
RATINGS_PATH = 'ratings.csv'
LINKS_PATH = 'links.csv'

# Carga datos y modelo al iniciar la API
print("Cargando datos y modelo...")
movies = pd.read_csv(MOVIES_PATH)
ratings = pd.read_csv(RATINGS_PATH)
links = pd.read_csv(LINKS_PATH)
links = links.set_index('movieId')

if not os.path.exists(MODELO_PATH):
    raise RuntimeError(f"Modelo no encontrado en {MODELO_PATH}. Entrena el modelo primero.")

model = dump.load(MODELO_PATH)[0][0]
print("Modelo cargado correctamente.")

# Modelos Pydantic
class RecomendacionRequest(BaseModel):
    user_id: int
    n_recomendaciones: int = 5

class Valoracion(BaseModel):
    movieId: int
    rating: float

class RecomendarPersonalizadoRequest(BaseModel):
    valoraciones: List[Valoracion]
    n_recomendaciones: int = 5

@app.get("/")
def root():
    return {"mensaje": "API Recomendador MovieMosaic funcionando"}

@app.post("/recomendar")
def recomendar(request: RecomendacionRequest):
    user_id = request.user_id
    n = request.n_recomendaciones

    # Verificar si el usuario existe en ratings
    if user_id not in ratings['userId'].unique():
        raise HTTPException(status_code=404, detail=f"Usuario {user_id} no encontrado")

    movie_ids = movies['movieId'].unique()
    ya_vistas = ratings[ratings['userId'] == user_id]['movieId'].tolist()
    no_vistas = [mid for mid in movie_ids if mid not in ya_vistas]

    predicciones = []
    for mid in no_vistas:
        prediccion = model.predict(user_id, mid)
        predicciones.append((mid, prediccion.est))

    predicciones.sort(key=lambda x: x[1], reverse=True)
    top_n = predicciones[:n]

    recomendaciones = []
    for movie_id, score in top_n:
        titulo = movies[movies['movieId'] == movie_id]['title'].values[0]
        tmdb_id = get_tmdb_id(movie_id)
        recomendaciones.append({
            "movieId": int(movie_id),
            "title": titulo,
            "score": round(score, 2),
            "tmdbId": tmdb_id
        })

    return {"user_id": user_id, "recomendaciones": recomendaciones}

@app.get("/buscar_pelicula")
def buscar_pelicula(nombre: str = Query(..., min_length=2, description="Parte del título de la película")):
    resultados = movies[movies['title'].str.lower().str.contains(nombre.lower())]
    if resultados.empty:
        return {"resultados": []}
    pelis = [
        {"movieId": int(row["movieId"]), "title": row["title"]}
        for _, row in resultados.iterrows()
    ]
    return {"resultados": pelis}

@app.post("/recomendar_personalizado")
def recomendar_personalizado(request: RecomendarPersonalizadoRequest):
    user_id = 999999  # ID ficticio para el usuario temporal
    user_ratings = pd.DataFrame(
        [{"userId": user_id, "movieId": v.movieId, "rating": v.rating} for v in request.valoraciones]
    )

    movie_ids = movies['movieId'].unique()
    ya_vistas = user_ratings['movieId'].tolist()
    no_vistas = [mid for mid in movie_ids if mid not in ya_vistas]

    predicciones = []
    for mid in no_vistas:
        prediccion = model.predict(user_id, mid)
        predicciones.append((mid, prediccion.est))

    predicciones.sort(key=lambda x: x[1], reverse=True)
    top_n = predicciones[:request.n_recomendaciones]

    recomendaciones = []
    for movie_id, score in top_n:
        titulo = movies[movies['movieId'] == movie_id]['title'].values[0]
        recomendaciones.append({"movieId": int(movie_id), "title": titulo, "score": round(score, 2)})

    return {"recomendaciones": recomendaciones}
def get_tmdb_id(movie_id):
    try:
        tmdb_id = int(links.loc[movie_id]['tmdbId'])
        return tmdb_id if tmdb_id > 0 else None
    except Exception:
        return None
