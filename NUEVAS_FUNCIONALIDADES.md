# 🎉 Nuevas Funcionalidades MAGERIT - ISOapp

## ✨ Funcionalidades Agregadas

### 1. **Calculadora de Riesgos Mejorada**
La calculadora ahora muestra los datos de manera más clara y permite hacer cálculos rápidos.

### 2. **Formulario para Agregar Nuevos Activos** 🆕

Ahora puedes agregar nuevos activos directamente desde la interfaz web. El formulario incluye todos los campos necesarios:

#### Campos del Formulario:

1. **Tipo de Activo** *
   - Ejemplo: "Datos Geoespaciales", "Modelo de IA (CNN)", "Infraestructura de TI"

2. **Nombre del Activo** *
   - Ejemplo: "Datos de Zonas Geotérmicas"

3. **Amenaza** *
   - Ejemplo: "Acceso no autorizado a datos"

4. **Valor Económico** *
   - Ejemplo: "Normal: 1.350.000 COP"

5. **Frecuencia (Texto)**
   - Ejemplo: "1 vez cada 3 meses"

6. **Frecuencia (Número)** *
   - Valor numérico: 0-5
   - Ejemplo: 1.5

7. **Impacto** *
   - Valor numérico: 0-5
   - Ejemplo: 3.5

8. **% Salvaguarda** *
   - Porcentaje: 0-100
   - Ejemplo: 85

9. **Salvaguardas Implementadas** *
   - Ejemplo: "Backup de datos, Cifrado de datos, Protección de acceso"

### 3. **Cálculo Automático**

Cuando agregas un nuevo activo, el sistema calcula automáticamente:

- ✅ **Riesgo Intrínseco** = Frecuencia × Impacto
- ✅ **Riesgo Residual** = Riesgo Intrínseco - (Riesgo Intrínseco × % Salvaguarda)
- ✅ **Clasificación del Riesgo**:
  - Riesgo Bajo (< 2)
  - Riesgo Medio-Bajo (2-3)
  - Riesgo Medio-Alto (3-4)
  - Riesgo Alto (> 4)

### 4. **Numeración Automática**

El sistema asigna automáticamente el siguiente número disponible al nuevo activo.

## 📋 Cómo Usar

### Paso 1: Ir a MAGERIT
Navega a la sección **MAGERIT** desde el menú principal.

### Paso 2: Mostrar Formulario
Click en el botón **"Mostrar Formulario"** en la sección "Agregar Nuevo Activo".

### Paso 3: Llenar el Formulario
Completa todos los campos marcados con asterisco (*) que son obligatorios.

**Ejemplo de valores:**
```
Tipo de Activo: Base de Datos
Nombre del Activo: Base de datos de usuarios
Amenaza: SQL Injection
Valor Económico: Alto: 3.000.000 COP
Frecuencia (Texto): 1 vez cada mes
Frecuencia (Número): 2
Impacto: 4
% Salvaguarda: 75
Salvaguardas: WAF, Validación de entradas, Prepared statements
```

### Paso 4: Agregar Activo
Click en **"Agregar Activo"** y espera la confirmación.

### Paso 5: Verificar
La página se recargará automáticamente y verás el nuevo activo en la tabla.

## 🔧 APIs Disponibles

### POST `/api/magerit/add`

Agrega un nuevo activo a MAGERIT.

**Body (JSON):**
```json
{
  "tipo_activo": "Datos Geoespaciales",
  "activo": "Datos de Zonas Geotérmicas",
  "amenaza": "Acceso no autorizado a datos",
  "valor_economico": "Normal: 1.350.000 COP",
  "frecuencia_texto": "1 vez cada 3 meses",
  "frecuencia": 1.5,
  "impacto": 3.5,
  "salvaguarda": "Backup de datos, Cifrado de datos",
  "valor_salvaguarda_pct": 85
}
```

**Response:**
```json
{
  "success": true,
  "message": "Nuevo activo agregado correctamente",
  "data": [...]
}
```

### POST `/api/magerit/calculate`

Calcula riesgos sin guardar.

**Body (JSON):**
```json
{
  "frecuencia": 1.5,
  "impacto": 3.5,
  "salvaguarda_pct": 85
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "riesgo_intrinseco": 5.25,
    "riesgo_residual": 0.79
  }
}
```

## 📊 Datos Existentes

Actualmente tienes 5 activos en MAGERIT:

1. **Datos Geoespaciales** - Datos de Zonas Geotérmicas
2. **Modelo de IA (CNN)** - Modelo entrenado para predicción
3. **Infraestructura de TI** - Rack de servidores
4. **Firewall y Red** - Firewall de red externa e interna
5. **Dispositivos de comunicación** - Router, Dispositivos móviles

## 💡 Tips

- **Frecuencia**: Usa valores decimales para mejor precisión (ej: 1.5, 2.5)
- **Impacto**: Escala del 1 al 5, donde 5 es muy alto
- **Salvaguarda**: Porcentajes altos (80-100%) reducen significativamente el riesgo residual
- **Descripción clara**: Sé específico en las amenazas y salvaguardas para mejor documentación

## 🔄 Edición de Activos

Además de agregar, puedes **editar activos existentes**:
1. Click en el botón "Editar" (icono lápiz) en cualquier fila
2. Modifica los valores que necesites
3. Los riesgos se recalculan automáticamente
4. Guarda los cambios

## 📁 Almacenamiento

Los datos se guardan directamente en el archivo CSV: `Matiz(MAGERIT).csv`

## 🎯 Próximas Mejoras Sugeridas

- [ ] Exportar activos individuales
- [ ] Duplicar activo existente
- [ ] Eliminar activos
- [ ] Historial de cambios
- [ ] Gráficos de visualización de riesgos
- [ ] Comparación de riesgos entre activos
- [ ] Alertas para riesgos altos

---

**¡Listo para usar! 🚀**

Navega a http://127.0.0.1:5000/magerit y comienza a agregar tus activos.
