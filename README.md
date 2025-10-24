# ISOapp - Sistema de Gestión de Seguridad de la Información

## 📋 Descripción

ISOapp es una aplicación web desarrollada con Flask que permite gestionar y analizar la seguridad de la información en el proyecto de identificación de zonas geotérmicas utilizando redes neuronales convolucionales (CNN). 

La aplicación integra cuatro marcos de seguridad principales:

- **MAGERIT**: Análisis y gestión de riesgos
- **ISO 27001 (Anexo A)**: Controles de seguridad de la información
- **COBIT**: Procesos de gobernanza de TI
- **NIST CSF**: Marco de ciberseguridad

## ✨ Características

- 📊 **Visualización de datos** de los 4 marcos de seguridad
- ✏️ **Edición interactiva** de valores en MAGERIT
- 🧮 **Cálculo automático** de riesgos intrínsecos y residuales
- 📈 **Dashboard** con estadísticas en tiempo real
- 🔍 **Filtros y búsqueda** en todas las secciones
- 📄 **Generación de reportes** en PDF
- 💻 **Interfaz moderna y responsiva**

## 🚀 Instalación

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar el repositorio** (o ya estás en él):

```bash
cd /workspaces/ISOapp
```

2. **Crear un entorno virtual** (opcional pero recomendado):

```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate  # En Windows
```

3. **Instalar dependencias**:

```bash
pip install -r requirements.txt
```

## 🎯 Uso

### Iniciar la aplicación

```bash
python app.py
```

La aplicación se ejecutará en: `http://localhost:5000`

### Navegación

1. **Dashboard** (`/`): Vista general con estadísticas
2. **MAGERIT** (`/magerit`): Análisis de riesgos con calculadora y edición de activos
3. **ISO 27001** (`/anexo-a`): Controles de seguridad organizacionales, de personas y tecnológicos
4. **COBIT** (`/cobit`): Procesos de gobernanza de TI
5. **NIST CSF** (`/nist`): Marco de ciberseguridad con 5 funciones
6. **Reportes** (`/reports`): Generador de reportes en PDF

## 📊 Estructura del Proyecto

```
ISOapp/
├── app.py                      # Aplicación Flask principal
├── requirements.txt            # Dependencias Python
├── README.md                   # Documentación
├── Matiz(MAGERIT).csv         # Datos de análisis de riesgos
├── Matiz(Anexo A).csv         # Datos de controles ISO 27001
├── Matiz(COBIT).csv           # Datos de procesos COBIT
├── Matiz(NIST).csv            # Datos de marco NIST
├── utils/
│   └── csv_processor.py       # Módulo de procesamiento de CSV
├── templates/                  # Plantillas HTML
│   ├── base.html              # Plantilla base
│   ├── index.html             # Dashboard
│   ├── magerit.html           # Vista MAGERIT
│   ├── anexo_a.html           # Vista ISO 27001
│   ├── cobit.html             # Vista COBIT
│   ├── nist.html              # Vista NIST
│   └── reports.html           # Vista de reportes
└── static/                     # Archivos estáticos
    ├── css/
    │   └── style.css          # Estilos CSS
    └── js/
        └── main.js            # JavaScript principal
```

## 🧮 Funcionalidades Clave

### Calculadora de Riesgos MAGERIT

La aplicación calcula automáticamente:

- **Riesgo Intrínseco** = Frecuencia × Impacto
- **Riesgo Residual** = Riesgo Intrínseco - (Riesgo Intrínseco × % Salvaguarda)

### Edición de Activos

Permite modificar:
- Valor económico del activo
- Frecuencia de amenazas
- Nivel de impacto
- Salvaguardas implementadas
- Porcentaje de efectividad de salvaguardas

Los riesgos se recalculan automáticamente al guardar cambios.

### Generación de Reportes

Genera reportes PDF que incluyen:
- Todas las secciones seleccionadas
- Tablas con datos actualizados
- Información del proyecto
- Fecha y hora de generación

## 🔧 API Endpoints

- `GET /` - Dashboard principal
- `GET /magerit` - Vista MAGERIT
- `GET /anexo-a` - Vista ISO 27001
- `GET /cobit` - Vista COBIT
- `GET /nist` - Vista NIST
- `GET /reports` - Vista de reportes
- `GET /api/data/all` - Obtener todos los datos (JSON)
- `GET /api/data/<csv_type>` - Obtener datos de un CSV específico
- `POST /api/magerit/calculate` - Calcular riesgos
- `POST /api/magerit/update/<row_index>` - Actualizar activo
- `POST /api/report/generate` - Generar reporte PDF

## 📝 Notas de Desarrollo

### Modificar los CSV

Los archivos CSV pueden editarse directamente o a través de la interfaz web. El formato debe mantenerse consistente para evitar errores de lectura.

### Personalizar Estilos

Los estilos CSS se encuentran en `static/css/style.css`. Se utilizan variables CSS para facilitar la personalización de colores y temas.

### Agregar Nuevas Funcionalidades

1. Agregar rutas en `app.py`
2. Crear templates en `templates/`
3. Actualizar procesadores en `utils/csv_processor.py`
4. Añadir estilos en `static/css/style.css`

## 🐛 Solución de Problemas

### Error de encoding en CSV

Si hay problemas al leer los CSV, el procesador intenta automáticamente con diferentes encodings (utf-8-sig y latin-1).

### Puerto en uso

Si el puerto 5000 está ocupado, modifica en `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Cambiar puerto
```

### Problemas con reportes PDF

Asegúrate de que `reportlab` esté instalado correctamente:

```bash
pip install --upgrade reportlab
```

## 👥 Contribuir

Para contribuir al proyecto:

1. Fork del repositorio
2. Crear una rama para tu feature
3. Commit de cambios
4. Push a la rama
5. Crear Pull Request

## 📄 Licencia

Este proyecto es parte del proyecto de Geotermia con CNN.

## 📧 Contacto

Para preguntas o sugerencias sobre el proyecto, contacta al equipo de desarrollo.

---

**Desarrollado para el Proyecto de Identificación de Zonas Geotérmicas con CNN**