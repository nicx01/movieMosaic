#!/bin/bash

# Script para preparar entorno virtual y dependencias para el recomendador

echo "🚀 Creando entorno virtual Python..."
python3 -m venv venv

echo "✅ Entorno virtual creado. Activando..."
source venv/bin/activate

echo "🔄 Actualizando pip..."
pip install --upgrade pip

echo "⬇️ Instalando numpy < 2.0 (por compatibilidad con scikit-surprise)..."
pip install "numpy<2.0"

echo "⬇️ Instalando pandas y scikit-surprise..."
pip install pandas scikit-surprise

echo "⬇️ Instalando requests (útil para APIs externas, como TMDb)..."
pip install requests

echo "🧹 Instalación completa."
echo
echo "Para activar el entorno virtual en el futuro, ejecuta:"
echo "source venv/bin/activate"
echo
echo "¡Ya puedes ejecutar tu recomendador!"
