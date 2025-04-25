from surprise import dump
import os

MODELO_PATH = 'modelo_entrenado_grande.pkl'

print(f"🔎 Buscando el modelo en {MODELO_PATH} ...")
if os.path.exists(MODELO_PATH):
    try:
        model = dump.load(MODELO_PATH)[0][0]
        print("✅ Modelo cargado correctamente.")
        print(f"Tipo de modelo: {type(model)}")
    except Exception as e:
        print(f"❌ Error al cargar el modelo: {e}")
else:
    print("❌ No se encontró el modelo entrenado. Ejecuta primero entrenar_modelo.py")
