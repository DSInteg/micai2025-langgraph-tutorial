# 🎯 Grafos Módulo 2 - Patrones Multi-Agente

Este directorio contiene **3 grafos educativos** que demuestran los patrones fundamentales de sistemas multi-agente, listos para ser abiertos en **LangGraph Studio**.

## 📁 Grafos Disponibles

### 1. `routing_support.py` - Sistema de Routing con Clasificador ⭐
**Complejidad**: ⭐⭐ Intermedio
**Requiere API**: ✅ OPENAI_API_KEY
**Patrón**: Routing (Classifier → Agentes Especializados)

**Sistema de Customer Support con routing inteligente:**
- **Classifier con LLM**: Categoriza consultas automáticamente
- **3 Agentes especializados**: Technical, Billing, General
- **Conditional edges**: Routing dinámico según categoría
- **Caso de uso**: Sistema de soporte técnico empresarial

```python
# Input:
{
  "query": "Mi API está devolviendo error 500",
  "intent": "",
  "response": ""
}

# Output:
{
  "query": "Mi API está devolviendo error 500",
  "intent": "technical",
  "response": "El error 500 es un Internal Server Error..."
}
```

**Arquitectura:**
```
START → classifier → [technical/billing/general] → END
```

---

### 2. `parallel_analysis.py` - Análisis Paralelo ⭐⭐
**Complejidad**: ⭐⭐⭐ Intermedio-Avanzado
**Requiere API**: ✅ OPENAI_API_KEY
**Patrón**: Paralelización (Fan-out → Fan-in)

**Sistema de análisis de documentos con ejecución paralela:**
- **3 Analistas en paralelo**: Sentiment, Entities, Summary
- **Send() API**: Fan-out para ejecución concurrente
- **Aggregator**: Fan-in para consolidar resultados
- **Performance**: ~3x más rápido que ejecución secuencial

```python
# Input:
{
  "document": "LangGraph es excelente para construir agentes...",
  "sentiment": "",
  "entities": [],
  "summary": "",
  "final_report": ""
}

# Output:
{
  "document": "LangGraph es excelente...",
  "sentiment": "Positivo",
  "entities": ["LangGraph", "LangChain"],
  "summary": "LangGraph es una herramienta para agentes.",
  "final_report": "[Reporte consolidado]"
}
```

**Arquitectura:**
```
START → fan_out
         ↓
    ┌────┼────┐
    ↓    ↓    ↓
 sentiment entities summary (EN PARALELO)
    └────┼────┘
         ↓
     aggregate → END
```

---

### 3. `orchestrator_workers.py` - Orchestrator-Workers ⭐⭐⭐
**Complejidad**: ⭐⭐⭐⭐ Avanzado
**Requiere API**: ✅ OPENAI_API_KEY
**Patrón**: Orchestrator-Workers (con Loops y Re-planificación)

**Sistema de coordinación inteligente con re-planificación:**
- **Orchestrator**: "Cerebro" que planifica y decide
- **3 Workers especializados**: Search, Analyze, Calculate
- **Loops**: Re-planificación hasta completar la tarea
- **Routing dinámico**: Basado en decisiones del orchestrator

```python
# Input:
{
  "query": "Investiga tendencias de LangGraph y proyecta adopción",
  "plan": "",
  "worker_results": [],
  "final_answer": ""
}

# Output:
{
  "query": "Investiga tendencias...",
  "plan": "synthesize",
  "worker_results": ["[SEARCH] ...", "[ANALYZE] ...", "[CALCULATE] ..."],
  "final_answer": "[Respuesta consolidada de múltiples workers]"
}
```

**Arquitectura:**
```
START → orchestrator ←──────┐
          ↓                  │
    [search/analyze/calc]    │
          ↓                  │
      workers ───────────────┘ (loop)
          ↓
      synthesize → END
```

---

## 🚀 Abrir en LangGraph Studio

### Opción 1: Línea de comandos

```bash
cd /home/jcordova/lang/micai2025/notebooks/modulo_2/studio
langgraph dev
```

### Opción 2: LangGraph Studio UI

1. Abre LangGraph Studio
2. "Open Folder" → Selecciona `/home/jcordova/lang/micai2025/notebooks/modulo_2/studio`
3. Selecciona el grafo del dropdown

---

## 📊 Comparación de Grafos

| Grafo | Patrón | Nodos | Loops | Paralelización | Mejor para aprender |
|-------|--------|-------|-------|----------------|---------------------|
| **routing_support** | Routing | 4 | ❌ | ❌ | Clasificación y routing básico |
| **parallel_analysis** | Fan-out/Fan-in | 4 | ❌ | ✅ | Ejecución concurrente, performance |
| **orchestrator_workers** | Orchestrator | 5 | ✅ | ❌ | Coordinación, re-planificación |

---

## 🎓 Ruta de Aprendizaje Recomendada

### Para este Módulo 2

1. **`routing_support.py`** (15 min) ⭐ EMPEZAR AQUÍ
   - Patrón más simple del módulo
   - Concepto de classifier + agentes especializados
   - Base para entender routing

2. **`parallel_analysis.py`** (12 min)
   - Introduce paralelización
   - Send() API para fan-out
   - Medir beneficios de performance

3. **`orchestrator_workers.py`** (15 min)
   - Patrón más complejo
   - Loops y re-planificación
   - Coordinación inteligente

### Prerequisitos

Se recomienda haber completado **Módulo 1** primero:
- Entender State, Nodes, Edges
- Conocer conditional edges
- Familiaridad con LangGraph básico

---

## 🔧 Configuración

### Dependencias

```bash
pip install -r requirements.txt
```

### Variables de Entorno (REQUERIDO)

Todos los grafos requieren OpenAI API key:

```bash
# Copiar template
cp .env.example .env

# Editar y agregar tu API key
# OPENAI_API_KEY=sk-...
```

---

## 🎬 Ejemplos de Input

### Para `routing_support.py`

**Technical Query:**
```json
{
  "query": "Mi API está devolviendo error 500 en todas las llamadas",
  "intent": "",
  "response": ""
}
```

**Billing Query:**
```json
{
  "query": "Quiero cancelar mi suscripción actual",
  "intent": "",
  "response": ""
}
```

**General Query:**
```json
{
  "query": "¿Qué es LangGraph y para qué sirve?",
  "intent": "",
  "response": ""
}
```

### Para `parallel_analysis.py`

```json
{
  "document": "LangGraph de LangChain es excelente para construir sistemas multi-agente. Permite workflows complejos con múltiples LLMs trabajando juntos. La comunidad está muy emocionada.",
  "sentiment": "",
  "entities": [],
  "summary": "",
  "final_report": ""
}
```

### Para `orchestrator_workers.py`

```json
{
  "query": "Investiga las tendencias de LangGraph en 2024 y proyecta su adopción en 2025",
  "plan": "",
  "worker_results": [],
  "final_answer": ""
}
```

---

## 🧪 Ejecutar Localmente (Sin Studio)

Todos los grafos pueden ejecutarse directamente:

```bash
# Activar entorno virtual
source ../../../venv/bin/activate

# Ejecutar cada grafo
python routing_support.py
python parallel_analysis.py
python orchestrator_workers.py
```

Cada script incluye tests predefinidos que demuestran el funcionamiento.

---

## 📚 Patrones Demostrados

### 1. Routing Pattern (`routing_support.py`)

**Concepto**: Un classifier centralizado dirige a agentes especializados

**Cuándo usar:**
- ✅ Diferentes tipos de consultas requieren expertise diferente
- ✅ Necesitas categorizar antes de procesar
- ✅ Agentes especializados por dominio

**Ejemplo real**: Sistemas de soporte, triage de tickets, enrutamiento de llamadas

**Código clave:**
```python
builder.add_conditional_edges(
    "classifier",
    lambda s: s['intent'],  # Decide basado en intent
    {
        'technical': 'technical',
        'billing': 'billing',
        'general': 'general'
    }
)
```

---

### 2. Parallelization Pattern (`parallel_analysis.py`)

**Concepto**: Ejecutar múltiples tareas independientes simultáneamente

**Cuándo usar:**
- ✅ Tareas independientes que no dependen entre sí
- ✅ Performance crítico (reducir latencia)
- ✅ Múltiples análisis del mismo input

**Ejemplo real**: Análisis de documentos, procesamiento de media, data pipelines

**Código clave:**
```python
def fan_out(state):
    return [
        Send('sentiment', state),    # Ejecuta
        Send('entities', state),      # EN
        Send('summary', state)        # PARALELO
    ]

builder.add_conditional_edges(START, fan_out)
```

**Beneficio**: ~3x más rápido que ejecución secuencial

---

### 3. Orchestrator-Workers Pattern (`orchestrator_workers.py`)

**Concepto**: Un coordinador central decide qué workers ejecutar y cuándo

**Cuándo usar:**
- ✅ Tareas complejas que requieren múltiples pasos
- ✅ Necesitas re-planificación dinámica
- ✅ Workers especializados en diferentes sub-tareas

**Ejemplo real**: Research agents, data analysis pipelines, automated workflows

**Código clave:**
```python
# Workers vuelven al orchestrator (loop)
builder.add_edge("search", "orchestrator")
builder.add_edge("analyze", "orchestrator")
builder.add_edge("calculate", "orchestrator")

# Orchestrator decide siguiente paso
builder.add_conditional_edges(
    "orchestrator",
    route_decision,  # Basado en plan
    {...}
)
```

**Característica clave**: Re-planificación con loops

---

## 🎓 Para el Instructor

### Demostración en Clase - Orden Sugerido

**Timing total: 40-45 min**

1. **Routing (15 min)**
   - Mostrar diferentes consultas → diferentes rutas
   - Modificar las categorías en vivo
   - Discutir: ¿Cuándo usar routing vs otros patrones?

2. **Paralelización (12 min)**
   - Ejecutar y mostrar timing
   - Comparar: ¿Qué pasa si fuera secuencial?
   - Experimento: Agregar un 4to analista

3. **Orchestrator (15 min)**
   - Mostrar el loop de re-planificación
   - Observar cómo decide qué worker usar
   - Discutir: Cuándo necesitas un orchestrator

### Puntos Clave para Enfatizar

**Routing:**
- ✅ Classifier es la clave
- ✅ Agentes especializados = mejor calidad
- ✅ Escalable: fácil agregar nuevas categorías

**Paralelización:**
- ✅ Send() API para fan-out
- ✅ Performance: ~3x speedup
- ✅ Ideal para tareas independientes

**Orchestrator:**
- ✅ Loops permiten re-planificación
- ✅ Coordinación inteligente
- ✅ Flexibilidad: puede ejecutar N workers

### Preguntas para la Audiencia

1. "¿En qué se diferencia routing de orchestrator?"
2. "¿Cuándo usarían paralelización vs secuencial?"
3. "¿Pueden pensar en casos de uso reales para cada patrón?"
4. "¿Qué pasa si combinamos los 3 patrones?"

### Experimentos Interactivos

**Routing:**
- Cambiar categorías (agregar "emergency")
- Modificar la lógica del classifier
- Agregar un 4to agente especializado

**Paralelización:**
- Agregar 4to analista (keywords)
- Medir tiempo con 1, 2, 3, 4 analistas
- Comparar speedup

**Orchestrator:**
- Cambiar límite de workers (de 3 a 2)
- Agregar un nuevo worker type
- Modificar lógica de decisión

---

## 🔍 Debugging en Studio

### Qué observar

**En routing_support:**
- Ver qué intent clasifica el LLM
- Seguir la ruta tomada por cada consulta
- Inspeccionar la respuesta de cada agente

**En parallel_analysis:**
- Ver los 3 analistas ejecutándose en paralelo
- Comparar tiempos de ejecución
- Inspeccionar el reporte final agregado

**En orchestrator_workers:**
- Contar cuántas veces pasa por orchestrator
- Ver qué workers se ejecutan y en qué orden
- Observar cuándo decide hacer synthesize

---

## 🆘 Troubleshooting

### "OPENAI_API_KEY not found"
```bash
cp .env.example .env
# Editar .env y agregar tu key
```

### "Module not found"
```bash
pip install -r requirements.txt
```

### El grafo no aparece en Studio
- Verifica que langgraph.json está correcto
- Recarga Studio (Cmd+R / Ctrl+R)
- Verifica que no hay errores de sintaxis en los .py

### Los prints no aparecen
- En Studio, ve a la consola/terminal
- O ejecuta directamente: `python routing_support.py`

---

## 📖 Recursos Adicionales

- [LangGraph Patterns Documentation](https://langchain-ai.github.io/langgraph/how-tos/)
- [Send() API Reference](https://langchain-ai.github.io/langgraph/reference/types/#send)
- [Conditional Edges Guide](https://langchain-ai.github.io/langgraph/how-tos/branching/)
- [Notebooks Tutorial](../) - Versión interactiva de estos grafos

---

## 🔗 Integración con Notebooks

Cada grafo corresponde a un notebook del tutorial:

| Grafo | Notebook | Ejercicio |
|-------|----------|-----------|
| routing_support.py | 02_instructor_ejercicio_2_1_routing.ipynb | Ejercicio 2.1 |
| parallel_analysis.py | 03_instructor_ejercicio_2_2_parallel.ipynb | Ejercicio 2.2 |
| orchestrator_workers.py | 04_instructor_ejercicio_2_3_orchestrator.ipynb | Ejercicio 2.3 |

**Flujo de aprendizaje:**
1. Aprender con el notebook (conceptos paso a paso)
2. Practicar en Studio (visualización e interacción)
3. Modificar el código (extensiones y experimentos)

---

## ✨ Extensiones Sugeridas

### Routing Support
- [ ] Agregar categoría "emergency" con prioridad
- [ ] Implementar fallback para categorías desconocidas
- [ ] Agregar confidence scoring

### Parallel Analysis
- [ ] Agregar 4to analista (keywords extraction)
- [ ] Implementar timeout para analistas lentos
- [ ] Agregar métricas de performance

### Orchestrator Workers
- [ ] Agregar 4to worker type (validate)
- [ ] Implementar límite de iteraciones
- [ ] Agregar historial de decisiones

---

**🎉 ¡Explora los 3 patrones multi-agente y construye sistemas más sofisticados!**

**Recomendación**: Empieza con `routing_support.py` si es tu primer contacto con patrones multi-agente.
