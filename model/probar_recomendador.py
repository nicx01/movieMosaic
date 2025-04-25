from surprise import dump
import pandas as pd
import os

MODELO_PATH = 'modelo_entrenado_grande.pkl'

print("🔄 Cargando datos...")
ratings = pd.read_csv("ratings.csv")
movies = pd.read_csv("movies.csv")
print("✅ ratings.csv y movies.csv cargados.")

print(f"🔎 Buscando el modelo en {MODELO_PATH} ...")
if not os.path.exists(MODELO_PATH):
    print("❌ No se encontró el modelo entrenado. Ejecuta primero entrenar_modelo.py")
    exit(1)

try:
    model = dump.load(MODELO_PATH)[0][0]
    print("✅ Modelo cargado correctamente.")
except Exception as e:
    print(f"❌ Error al cargar el modelo: {e}")
    exit(1)

def mostrar_peliculas_valoradas(usuario_id):
    valoradas = ratings[ratings['userId'] == usuario_id]
    if valoradas.empty:
        print(f"El usuario {usuario_id} no ha valorado ninguna película.")
        return
    print(f"\nPelículas ya valoradas por el usuario {usuario_id}:")
    for _, row in valoradas.iterrows():
        movie_id = row['movieId']
        rating = row['rating']
        titulo = movies[movies['movieId'] == movie_id]['title'].values[0]
        print(f"- {titulo} (nota: {rating})")

def recomendar_peliculas(usuario_id, n=5):
    movie_ids = movies['movieId'].unique()
    ya_vistas = ratings[ratings['userId'] == usuario_id]['movieId'].tolist()
    no_vistas = [mid for mid in movie_ids if mid not in ya_vistas]

    predicciones = []
    for mid in no_vistas:
        prediccion = model.predict(usuario_id, mid)
        predicciones.append((mid, prediccion.est))
    
    predicciones.sort(key=lambda x: x[1], reverse=True)
    top_n = predicciones[:n]

    print(f"\n🎬 Recomendaciones para el usuario {usuario_id}:\n")
    for movie_id, score in top_n:
        titulo = movies[movies['movieId'] == movie_id]['title'].values[0]
        print(f"👉 {titulo} (predicción: {score:.2f})")

try:
    usuario_id = int(input("¿Para qué ID de usuario quieres recomendaciones? "))
    n = int(input("¿Cuántas películas quieres que te recomiende? "))
    mostrar_peliculas_valoradas(usuario_id)
    recomendar_peliculas(usuario_id=usuario_id, n=n)
except Exception as e:
    print(f"Ha ocurrido un error: {e}")
