from surprise import Dataset, Reader, SVD, dump
from surprise.model_selection import train_test_split
from surprise import accuracy
import pandas as pd

MODELO_PATH = 'modelo_entrenado_grande.pkl'

print("🔄 Cargando datos...")
ratings = pd.read_csv("ratings.csv")
print("✅ ratings.csv cargado")
reader = Reader(rating_scale=(0.5, 5.0))
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

print("🧠 Iniciando entrenamiento del modelo SVD...")
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)
model = SVD()
model.fit(trainset)
print("✅ Entrenamiento completado.")

print("📈 Evaluando el modelo...")
predictions = model.test(testset)
rmse = accuracy.rmse(predictions)
print(f"📊 Precisión RMSE: {rmse:.4f}")

print(f"💾 Guardando el modelo entrenado en {MODELO_PATH} ...")
try:
    dump.dump(MODELO_PATH, (model, None))
    print(f"✅ Modelo guardado con éxito en {MODELO_PATH}")
except Exception as e:
    print(f"❌ Error al guardar el modelo: {e}")
