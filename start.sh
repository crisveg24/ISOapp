#!/bin/bash
# Script para iniciar la aplicación ISOapp

echo "🚀 Iniciando ISOapp - Sistema de Gestión de Seguridad"
echo "=================================================="
echo ""

# Verificar si el entorno virtual existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

# Iniciar aplicación
echo ""
echo "✅ Todo listo!"
echo "🌐 La aplicación se iniciará en: http://localhost:5000"
echo "📊 Presiona CTRL+C para detener la aplicación"
echo ""
python app.py
