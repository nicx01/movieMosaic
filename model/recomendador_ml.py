from surprise import Dataset, Reader, SVD, dump
from surprise.model_selection import train_test_split
from surprise import accuracy
import os
import pandas as pd 

# Cargar datos
ratings = pd.read_csv("ratings.csv")
movies = pd.read_csv("movies.csv")
print("Datos cargados: ratings.csv y movies.csv")

# Inicialización de Reader y Dataset
reader = Reader(rating_scale=(0.5, 5.0))
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

# Nombre del archivo donde se guarda el modelo
modelo_guardado = 'modelo_entrenado_grande.pkl'

# Función para entrenar y guardar el modelo
def entrenar_y_guardar_modelo():
    print("Entrenando un nuevo modelo...")
    trainset, testset = train_test_split(data, test_size=0.2, random_state=42)
    model = SVD()
    model.fit(trainset)
    predictions = model.test(testset)
    print(f"📊 Precisión RMSE: {accuracy.rmse(predictions)}")
    
    try:
        dump.dump(modelo_guardado, (model, None))
        print(f"Modelo guardado con éxito en {modelo_guardado}")
    except Exception as e:
        print(f"Error al guardar el modelo: {e}")
    return model

# Verificar si el modelo existe
model = None
if os.path.exists(modelo_guardado):
    print("Cargando el modelo entrenado...")
    try:
        model = dump.load(modelo_guardado)[0][0]  # Solo agarramos el modelo
        print("Modelo cargado con éxito.")
    except Exception as e:
        print(f"Error al cargar el modelo: {e}")
        model = entrenar_y_guardar_modelo()
else:
    print("No se encontró el modelo entrenado. Entrenando un nuevo modelo...")
    model = entrenar_y_guardar_modelo()

# Verificar el tipo de objeto model
print(f"Tipo de modelo cargado o entrenado: {type(model)}")

# Mostrar películas ya valoradas
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

# Función para recomendar películas
def recomendar_peliculas(usuario_id, n=5):
    if not model:
        print("El modelo no se ha cargado correctamente.")
        return
    
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

# Preguntar por usuario y número de recomendaciones
try:
    usuario_id = int(input("¿Para qué ID de usuario quieres recomendaciones? "))
    n = int(input("¿Cuántas películas quieres que te recomiende? "))
    mostrar_peliculas_valoradas(usuario_id)
    recomendar_peliculas(usuario_id=usuario_id, n=n)
except Exception as e:
    print(f"Ha ocurrido un error: {e}")
