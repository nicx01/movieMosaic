import pandas as pd
from surprise import dump, Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy
import os

MODELO_PATH = 'modelo_entrenado_grande.pkl'
MODELO_PERSONALIZADO_PATH = 'modelo_personalizado_999999.pkl'
MOVIES_PATH = 'movies.csv'
RATINGS_PATH = 'ratings.csv'

# Cargar datos
movies = pd.read_csv(MOVIES_PATH)
print("🎬 movies.csv cargado.")
ratings = pd.read_csv(RATINGS_PATH)
print("📊 ratings.csv cargado.")

# Comprobar modelo entrenado general
if not os.path.exists(MODELO_PATH):
    print("❌ No se encontró el modelo entrenado. Ejecuta primero entrenar_modelo.py")
    exit(1)

model_general = dump.load(MODELO_PATH)[0][0]
print("✅ Modelo general cargado correctamente.")

""" # 1. Pedir 10 películas y sus notas
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

    valoraciones.append({'userId': 999999, 'movieId': movie_id, 'rating': nota}) """

#valoraciones = [
#    {'userId': 999999, 'movieId': 1, 'rating': 4.0},       # Toy Story (1995)
#    {'userId': 999999, 'movieId': 3114, 'rating': 5.0},    # Toy Story 2 (1999)
#    {'userId': 999999, 'movieId': 78499, 'rating': 5.0},   # Toy Story 3 (2010)
#    {'userId': 999999, 'movieId': 106782, 'rating': 5.0},  # Toy Story of Terror (2013)
#    {'userId': 999999, 'movieId': 5952, 'rating': 5.0},    # Tarzan (1999)
#    {'userId': 999999, 'movieId': 1124, 'rating': 1.0},    # Untouchables, The (1987)
#    {'userId': 999999, 'movieId': 260, 'rating': 3.6},     # Star Wars: Episode IV
#    {'userId': 999999, 'movieId': 1196, 'rating': 3.2},    # Lord of the Rings (1978)
#    {'userId': 999999, 'movieId': 1221, 'rating': 4.3},    # Incredibles, The (2004)
#    {'userId': 999999, 'movieId': 32587, 'rating': 2.2},   # Charlie: The Life and Art of Charles Chaplin
#]
valoraciones = [
    # ---- Favoritas: Star Wars, Superhéroes, Acción, Fantasía, Sci-Fi, Animación épica ----
    {'userId': 999999, 'movieId': 260, 'rating': 5.0},        # Star Wars: Episode IV - A New Hope (1977)
    {'userId': 999999, 'movieId': 1196, 'rating': 4.9},       # Star Wars: Episode V - The Empire Strikes Back (1980)
    {'userId': 999999, 'movieId': 1214, 'rating': 4.8},       # Star Wars: Episode VI - Return of the Jedi (1983)
    {'userId': 999999, 'movieId': 7153, 'rating': 4.7},       # Spider-Man (2002)
    {'userId': 999999, 'movieId': 95510, 'rating': 5.0},      # The Amazing Spider-Man (2012)
    {'userId': 999999, 'movieId': 95932, 'rating': 4.8},      # Fantastic Four, The (1994)
    {'userId': 999999, 'movieId': 2571, 'rating': 4.7},       # Matrix, The (1999)
    {'userId': 999999, 'movieId': 96079, 'rating': 4.9},      # Skyfall (2012)
    {'userId': 999999, 'movieId': 96302, 'rating': 4.7},      # War of the Arrows (2011)
    {'userId': 999999, 'movieId': 96131, 'rating': 4.6},      # K-20: The Fiend with Twenty Faces (2008)
    {'userId': 999999, 'movieId': 95473, 'rating': 4.8},      # Dragon Ball Z: The Return of Cooler (1992)
    {'userId': 999999, 'movieId': 95475, 'rating': 4.7},      # Dragon Ball Z: Cooler's Revenge (1991)
    {'userId': 999999, 'movieId': 95497, 'rating': 4.9},      # Dragon Ball Z: Super Android 13! (1992)
    {'userId': 999999, 'movieId': 95499, 'rating': 4.8},      # Dragon Ball Z: Broly - The Legendary Super Saiyan (1993)
    {'userId': 999999, 'movieId': 95519, 'rating': 4.7},      # Dragon Ball Z: Bojack Unbound (1993)
    {'userId': 999999, 'movieId': 95771, 'rating': 4.7},      # Dragon Ball Z: Broly Second Coming (1994)
    {'userId': 999999, 'movieId': 95780, 'rating': 4.8},      # Dragon Ball Z: Bio-Broly (1994)
    {'userId': 999999, 'movieId': 95782, 'rating': 4.9},      # Dragon Ball Z: Fusion Reborn (1995)
    {'userId': 999999, 'movieId': 95963, 'rating': 4.8},      # Dragon Ball Z: Wrath of the Dragon (1995)
    {'userId': 999999, 'movieId': 95965, 'rating': 4.7},      # Dragon Ball Z: Bardock - The Father of Goku (1990)
    {'userId': 999999, 'movieId': 96004, 'rating': 4.8},      # Dragon Ball Z: The History of Trunks (1993)
    {'userId': 999999, 'movieId': 96007, 'rating': 4.6},      # Dragon Ball GT: A Hero's Legacy (1997)
    {'userId': 999999, 'movieId': 96300, 'rating': 4.6},      # Operación Cannabis (2009) - Acción/Comedia
    {'userId': 999999, 'movieId': 96146, 'rating': 4.5},      # Logan's War: Bound by Honor (1998)
    {'userId': 999999, 'movieId': 96148, 'rating': 4.4},      # President's Man: A Line in the Sand (2002)
    {'userId': 999999, 'movieId': 96246, 'rating': 4.5},      # In Eagle Shadow Fist (1973)
    {'userId': 999999, 'movieId': 96250, 'rating': 4.7},      # K.G. (Karate Girl) (2011)
    {'userId': 999999, 'movieId': 95705, 'rating': 4.4},      # Sasori (2008)
    {'userId': 999999, 'movieId': 95506, 'rating': 4.3},      # Extraterrestrial (2011)
    {'userId': 999999, 'movieId': 95207, 'rating': 4.2},      # Abraham Lincoln: Vampire Hunter (2012)
    {'userId': 999999, 'movieId': 95298, 'rating': 4.2},      # Woochi: The Demon Slayer (2009)
    {'userId': 999999, 'movieId': 95484, 'rating': 4.1},      # Pulgasari (1985)
    {'userId': 999999, 'movieId': 95545, 'rating': 4.0},      # Dangerous Man, A (2009)
    {'userId': 999999, 'movieId': 96017, 'rating': 4.1},      # Dragon Eyes (2012)
    {'userId': 999999, 'movieId': 96367, 'rating': 4.0},      # Hit and Run (2012)
    {'userId': 999999, 'movieId': 95717, 'rating': 4.0},      # Treasure Island (2012)
    {'userId': 999999, 'movieId': 96022, 'rating': 4.0},      # Dick Tracy vs. Cueball (1946)
    {'userId': 999999, 'movieId': 96170, 'rating': 4.0},      # Cutter, The (2005)
    {'userId': 999999, 'movieId': 96105, 'rating': 4.0},      # Forest Warrior (1996)
    {'userId': 999999, 'movieId': 96193, 'rating': 4.0},      # Captain Video: Master of the Stratosphere (1951)

    # ---- Odia: Documentales y Romances ----
    {'userId': 999999, 'movieId': 95425, 'rating': 0.5},      # Map For Saturday, A (2007) - Documentary
    {'userId': 999999, 'movieId': 95197, 'rating': 0.7},      # Bel Ami (2012) - Romance
    {'userId': 999999, 'movieId': 95449, 'rating': 0.8},      # Magic Mike (2012) - Romance
    {'userId': 999999, 'movieId': 96009, 'rating': 0.5},      # Kiss, The (1896) - Romance
    {'userId': 999999, 'movieId': 95461, 'rating': 0.5},      # Revenge of the Electric Car (2011) - Documentary
    {'userId': 999999, 'movieId': 96018, 'rating': 0.5},      # Decoding the Past: Secrets of the Koran (2006) - Documentary
    {'userId': 999999, 'movieId': 95199, 'rating': 0.8},      # What to Expect When You're Expecting (2012) - Romance
    {'userId': 999999, 'movieId': 95443, 'rating': 0.7},      # Giant Mechanical Man, The (2012) - Romance
    {'userId': 999999, 'movieId': 95494, 'rating': 0.5},      # Joffrey: Mavericks of American Dance (2012) - Documentary
    {'userId': 999999, 'movieId': 96066, 'rating': 0.5},      # Love, Wedding, Marriage (2011) - Romance
]

# 2. Crear DataFrame con las valoraciones del usuario ficticio
usuario_df = pd.DataFrame(valoraciones)
print("\n✅ Tus valoraciones han sido registradas.")

# 3. Entrenar modelo personalizado para el usuario
print("\n⚙️ Entrenando modelo personalizado con tus valoraciones...")
ratings_personalizados = pd.concat([ratings, usuario_df], ignore_index=True)

reader = Reader(rating_scale=(0.5, 5.0))
data = Dataset.load_from_df(ratings_personalizados[['userId', 'movieId', 'rating']], reader) 
trainset = data.build_full_trainset()

model_personalizado = SVD()
model_personalizado.fit(trainset)

# Guardar modelo personalizado
dump.dump(MODELO_PERSONALIZADO_PATH, (model_personalizado, None))
print(f"✅ Modelo personalizado guardado como '{MODELO_PERSONALIZADO_PATH}'.")

# 4. Recomendar películas para el usuario ficticio
ya_vistas = usuario_df['movieId'].tolist()
no_vistas = movies[~movies['movieId'].isin(ya_vistas)]['movieId'].tolist()

print("\n🔮 Calculando recomendaciones personalizadas para ti...")

predicciones = []
for mid in no_vistas:
    prediccion = model_personalizado.predict(999999, mid)
    predicciones.append((mid, prediccion.est))

predicciones.sort(key=lambda x: x[1], reverse=True)
top_n = predicciones[:30]

print("\n🎬 ¡Tus 30 recomendaciones personalizadas!\n")
for movie_id, score in top_n:
    titulo = movies[movies['movieId'] == movie_id]['title'].values[0]
    print(f"👉 {titulo} (predicción: {score:.2f})")

print("\n¡Gracias por probar el recomendador personalizado! 🚀")
