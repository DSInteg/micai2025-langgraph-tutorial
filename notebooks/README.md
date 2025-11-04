# 📓 Notebooks para el Instructor

Esta carpeta contiene notebooks interactivos diseñados específicamente para que el instructor los use durante el tutorial MICAI 2025.

## 🎯 Propósito

Estos notebooks sirven como:
- **Herramienta de demostración en vivo** durante el tutorial
- **Guía paso a paso** con timing y scripts incluidos
- **Laboratorio de experimentación** para modificar parámetros en vivo
- **Material de respaldo** si algo falla durante la presentación
- **Referencia post-tutorial** que estudiantes pueden revisar

## 📁 Estructura

```
notebooks/
├── README.md (este archivo)
│
├── modulo_1/ - Fundamentos
│   ├── 00_primer_grafo_interactivo.ipynb ⭐ COMENZAR AQUÍ
│   ├── 01_instructor_workflow_vs_agente.ipynb
│   ├── 02_instructor_ejercicio_1_1.ipynb
│   └── 03_instructor_ejercicio_1_2.ipynb
│
├── modulo_2/ - Patrones Multi-Agente
│   ├── 01_instructor_patrones_overview.ipynb
│   ├── 02_instructor_ejercicio_2_1_routing.ipynb
│   ├── 03_instructor_ejercicio_2_2_parallel.ipynb
│   └── 04_instructor_ejercicio_2_3_orchestrator.ipynb
│
├── modulo_3/ - Agentes Autónomos
│   ├── 01_instructor_autonomia_overview.ipynb
│   ├── 02_instructor_ejercicio_3_1_plan_execute.ipynb
│   ├── 03_instructor_ejercicio_3_2_handoffs.ipynb
│   └── 04_instructor_ejercicio_3_3_memoria.ipynb
│
└── modulo_4/ - Aplicaciones de Negocio
    ├── 01_instructor_produccion_overview.ipynb
    ├── 02_instructor_ejercicio_4_1_customer_support.ipynb
    ├── 03_instructor_ejercicio_4_2_document_analysis.ipynb
    └── 04_instructor_ejercicio_4_3_research.ipynb
```

## ⭐ Notebook Especial: Primer Grafo Interactivo

El notebook `00_primer_grafo_interactivo.ipynb` es el **punto de entrada ideal** para el tutorial:

### 🎯 Por qué empezar aquí

- **Caso de uso real**: Sistema de clasificación de tickets de soporte
- **Conceptos fundamentales**: State, Nodes, Edges explicados desde cero
- **Hands-on inmediato**: Código ejecutable en cada paso
- **Progresión gradual**: De simple a complejo en 30 minutos
- **Motivador**: Los estudiantes ven resultados inmediatos

### 📚 Qué enseña

1. **State (Estados)**: Qué son, cómo se definen, cómo viajan por el grafo
2. **Nodes (Nodos)**: Funciones que procesan el estado
3. **Edges (Aristas)**: Conexiones normales vs condicionales
4. **Routing dinámico**: Cómo dirigir el flujo según lógica
5. **Construcción completa**: Del diseño a la ejecución

### 🎬 Flujo pedagógico

- **5 min**: Setup y contexto del caso de uso
- **8 min**: Definir State con explicación detallada
- **10 min**: Crear 3 nodos + conditional edge
- **5 min**: Construir y visualizar el grafo
- **7 min**: Ejecutar con diferentes inputs
- **5 min**: Experimentos hands-on

### 💡 Ventajas vs otros notebooks

Este notebook es **mejor como punto de entrada** porque:
- No requiere conocimiento previo de LangGraph
- Usa solo Python estándar (sin LLMs todavía)
- Cada concepto se explica con analogías
- Incluye experimentos interactivos
- Caso de uso familiar (todos han usado tickets de soporte)

## 🚀 Cómo Usar

### Antes del Tutorial

1. **Abre Jupyter Lab o VS Code**:
   ```bash
   jupyter lab notebooks/
   # O
   code notebooks/
   ```

2. **Ejecuta todas las celdas de setup** de cada notebook que vas a usar

3. **Verifica que no hay errores** en ningún notebook

4. **Practica el timing** ejecutando cada notebook completo

### Durante el Tutorial

1. **Proyecta el notebook** en pantalla grande

2. **Ejecuta celda por celda** siguiendo los scripts incluidos

3. **Lee los comentarios `💬 SCRIPT:`** - están diseñados para leerlos en voz alta

4. **Modifica inputs en las celdas `🎬 DEMO:`** para mostrar diferentes casos

5. **Usa las celdas `🧪 EXPERIMENTO:`** para invitar a la audiencia a participar

### Después del Tutorial

Los estudiantes pueden:
- Clonar el repo y ejecutar los notebooks
- Experimentar modificando el código
- Revisar las explicaciones paso a paso

## 📊 Características de los Notebooks

Cada notebook incluye:

### 🏷️ Secciones Marcadas

- `📋 CELL X: SETUP` - Configuración inicial
- `📖 CELL X: OBJETIVOS` - Qué se va a aprender
- `💡 CELL X: CONCEPTO` - Explicación teórica
- `📝 CELL X: PASO N` - Implementación paso a paso
- `🎬 CELL X: DEMO` - Demostración en vivo
- `🧪 CELL X: EXPERIMENTO` - Actividad interactiva
- `⚠️ CELL X: TROUBLESHOOTING` - Solución de problemas
- `✅ CELL X: CHECKPOINT` - Verificación de comprensión
- `🚀 CELL X: BONUS` - Contenido opcional avanzado

### 💬 Scripts para el Instructor

Cada celda tiene comentarios que indican:
- `💬 SCRIPT:` - Qué decir exactamente
- `❓ PREGUNTA:` - Preguntas para hacer a la audiencia
- `💡 TIP:` - Consejos de presentación
- `⏱️ Tiempo:` - Duración estimada de esa sección

### 🎨 Output Visual

- Prints formateados con bordes (`═══`, `───`)
- Emojis para facilitar lectura rápida
- Colores en markdown cells
- Visualizaciones del grafo cuando es posible

## ⏱️ Timing por Notebook

### Módulo 1 (60 min total)
- `00_primer_grafo_interactivo.ipynb` - 30 min ⭐ **COMENZAR AQUÍ**
- `01_workflow_vs_agente.ipynb` - 15 min
- `02_ejercicio_1_1.ipynb` - 8 min
- `03_ejercicio_1_2.ipynb` - 7 min

### Módulo 2 (60 min total)
- `01_patrones_overview.ipynb` - 15 min
- `02_ejercicio_2_1_routing.ipynb` - 15 min
- `03_ejercicio_2_2_parallel.ipynb` - 12 min
- `04_ejercicio_2_3_orchestrator.ipynb` - 10 min

### Módulo 3 (60 min total)
- `01_autonomia_overview.ipynb` - 15 min
- `02_ejercicio_3_1_plan_execute.ipynb` - 17 min
- `03_ejercicio_3_2_handoffs.ipynb` - 12 min
- `04_ejercicio_3_3_memoria.ipynb` - 10 min

### Módulo 4 (75 min total)
- `01_produccion_overview.ipynb` - 15 min
- `02_ejercicio_4_1_customer_support.ipynb` - 20 min
- `03_ejercicio_4_2_document_analysis.ipynb` - 20 min
- `04_ejercicio_4_3_research.ipynb` - 15 min (demo)

## 🔧 Configuración Requerida

Todos los notebooks asumen que tienes:

```bash
# 1. Ambiente virtual activado
source venv/bin/activate

# 2. Dependencias instaladas
pip install -r requirements.txt

# 3. Variables de entorno configuradas
cp .env.example .env
# Editar .env con tus API keys
```

## 💡 Tips para el Instructor

### Durante la Presentación

1. **Usa dos pantallas**:
   - Pantalla 1: Notebook ejecutándose
   - Pantalla 2: Documentación o GUIA_INSTRUCTOR.md

2. **Modo presentación**:
   - Jupyter: View → Presentation Mode
   - VS Code: Zoom al 150%

3. **Font size grande**:
   - Mínimo 18pt para que todos vean
   - Verifica desde el fondo del salón

4. **Celda por celda**:
   - No ejecutes todo de golpe
   - Deja que vean el proceso
   - Explica qué esperas antes de ejecutar

### Si Algo Falla

1. **El notebook tiene la solución**:
   - Scroll down - la celda de troubleshooting está ahí
   - O usa el código de `ejercicios/.../solution.py`

2. **Backup plan**:
   - Muestra el output pre-ejecutado (screenshots)
   - O cambia a mostrar `ejemplos/` que son más simples

3. **No entres en pánico**:
   - "Interesante, esto nos pasa en producción también"
   - Usa como oportunidad para mostrar debugging

## 📚 Relación con Otros Materiales

```
GUIA_INSTRUCTOR.md  ←→  Notebooks  ←→  Ejercicios
       ↓                    ↓              ↓
   Qué decir          Cómo mostrar    Qué hacer
```

- **GUIA_INSTRUCTOR.md**: Qué explicar, timing, estrategia
- **Notebooks** (aquí): Código para demostrar en vivo
- **Ejercicios**: Código para que estudiantes completen

## 🎓 Filosofía Pedagógica

Los notebooks siguen el principio **"I do, We do, You do"**:

1. **I do** (Celdas de demo): Instructor ejecuta y explica
2. **We do** (Celdas de experimento): Todos modifican juntos
3. **You do** (Referencia a ejercicios): Estudiantes lo hacen solos

## ⚠️ Notas Importantes

- **NO compartir estos notebooks antes del tutorial**
  - Contienen las soluciones
  - Estudiantes deben trabajar en `ejercicios/.../starter.py`

- **Sí compartir después del tutorial**
  - Como material de referencia
  - Para que puedan revisar

- **Los notebooks asumen OpenAI**
  - Si usas Anthropic, modifica las imports
  - El código es 95% compatible

## 📞 Soporte

Si encuentras errores en los notebooks:
1. Verifica que usas la versión correcta de dependencias
2. Revisa el archivo `.env`
3. Consulta `docs/GUIA_INSTRUCTOR.md` sección Troubleshooting

---

**Última actualización**: 2025-01-03
**Versión**: 1.0
**Total de notebooks**: 13
**Tiempo total de contenido**: ~4 horas
