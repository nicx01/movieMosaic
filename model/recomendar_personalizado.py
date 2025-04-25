import pandas as pd
from surprise import dump, Dataset, Reader, SVD
import os

MODELO_PATH = 'modelo_entrenado_grande.pkl'
MOVIES_PATH = 'movies.csv'
RATINGS_PATH = 'ratings.csv'

# Cargar datos
movies = pd.read_csv(MOVIES_PATH)
print("🎬 movies.csv cargado.")

# Comprobar modelo entrenado
if not os.path.exists(MODELO_PATH):
    print("❌ No se encontró el modelo entrenado. Ejecuta primero entrenar_modelo.py")
    exit(1)

model = dump.load(MODELO_PATH)[0][0]
print("✅ Modelo cargado correctamente.")

# 1. Pedir 10 películas y sus notas
valoraciones = []
for i in range(10):
    while True:
        titulo = input(f"\n[{i+1}/10] Escribe parte del título de una película que hayas visto: ").strip().lower()
        coincidencias = movies[movies['title'].str.lower().str.contains(titulo)]
        if coincidencias.empty:
            print("❌ No se encontraron películas con ese texto. Intenta de nuevo.")
            continue
        print("\nCoincidencias encontradas:")
        for idx, row in coincidencias.head(5).iterrows():
            print(f"{idx}: {row['title']}")
        try:
            seleccion = int(input("Selecciona el número de la película (índice de la lista mostrada): "))
            if seleccion not in coincidencias.index:
                print("❌ Índice no válido. Intenta de nuevo.")
                continue
            movie_id = coincidencias.loc[seleccion, 'movieId']
            break
        except Exception:
            print("❌ Entrada no válida. Intenta de nuevo.")

    while True:
        try:
            nota = float(input("¿Qué nota le das a esa película? (0.5 a 5.0): "))
            if 0.5 <= nota <= 5.0:
                break
            else:
                print("❌ La nota debe estar entre 0.5 y 5.0.")
        except Exception:
            print("❌ Entrada no válida. Intenta de nuevo.")

    valoraciones.append({'userId': 999999, 'movieId': movie_id, 'rating': nota})

# 2. Crear DataFrame con las valoraciones del usuario ficticio
usuario_df = pd.DataFrame(valoraciones)
print("\n✅ Tus valoraciones han sido registradas.")

# 3. Recomendar películas para el usuario ficticio
# Cargar ratings originales para excluir películas ya vistas
ratings = pd.read_csv(RATINGS_PATH)
ya_vistas = usuario_df['movieId'].tolist()
no_vistas = movies[~movies['movieId'].isin(ya_vistas)]['movieId'].tolist()

print("\n🔮 Calculando recomendaciones personalizadas para ti...")

predicciones = []
for mid in no_vistas:
    prediccion = model.predict(999999, mid)
    predicciones.append((mid, prediccion.est))

predicciones.sort(key=lambda x: x[1], reverse=True)
top_n = predicciones[:5]

print("\n🎬 ¡Tus 5 recomendaciones personalizadas!\n")
for movie_id, score in top_n:
    titulo = movies[movies['movieId'] == movie_id]['title'].values[0]
    print(f"👉 {titulo} (predicción: {score:.2f})")

print("\n¡Gracias por probar el recomendador personalizado! 🚀")
