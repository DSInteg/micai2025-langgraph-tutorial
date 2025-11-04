# Ejemplos de Referencia - LangGraph Multi-Agent

Esta carpeta contiene **ejemplos concisos y ejecutables** que demuestran los conceptos clave de cada módulo del tutorial.

## 📁 Estructura

```
ejemplos/
├── README.md (este archivo)
│
├── Módulo 1: Fundamentos
│   ├── modulo_1_workflow_simple.py     → Workflow determinístico básico
│   └── modulo_1_agente_basico.py       → Agente con ReAct pattern
│
├── Módulo 2: Patrones Multi-Agente
│   ├── modulo_2_routing.py             → Routing a agentes especializados
│   ├── modulo_2_parallelization.py     → Análisis paralelos con agregación
│   └── modulo_2_orchestrator.py        → Orchestrator-Workers pattern
│
├── Módulo 3: Agentes Autónomos
│   ├── modulo_3_plan_execute.py        → Plan-Execute-Evaluate
│   ├── modulo_3_handoffs.py            → Handoffs dinámicos
│   └── modulo_3_memoria.py             → Memoria compartida persistente
│
└── Módulo 4: Aplicaciones de Negocio
    ├── modulo_4_customer_support.py    → Sistema de atención al cliente
    └── modulo_4_document_pipeline.py   → Pipeline de análisis de documentos
```

## 🎯 Propósito de los Ejemplos

Los ejemplos en esta carpeta son **versiones simplificadas** de los ejercicios completos. Su propósito es:

1. **Demostrar el concepto core** de cada pattern
2. **Ser ejecutables de inmediato** sin configuración compleja
3. **Servir como referencia rápida** durante el desarrollo
4. **Facilitar la experimentación** y modificación

## 🔄 Diferencia con Ejercicios

| Aspecto | Ejemplos (`/ejemplos`) | Ejercicios (`/ejercicios`) |
|---------|------------------------|----------------------------|
| **Propósito** | Demostración rápida | Práctica completa |
| **Complejidad** | Simplificado | Completo y detallado |
| **Líneas de código** | ~100-200 | ~400-800 |
| **Documentación** | Comentarios básicos | Extensa con READMEs |
| **Tests** | No incluidos | Suite completa |
| **Tiempo** | 5-10 min lectura | 30-60 min implementación |

## 🚀 Cómo Usar los Ejemplos

### 1. Setup

Todos los ejemplos requieren:

```bash
# Instalar dependencias
pip install -r ../requirements.txt

# Configurar API key
export OPENAI_API_KEY="tu-api-key"
# O crear .env en la raíz del proyecto
```

### 2. Ejecutar un Ejemplo

```bash
# Desde la carpeta ejemplos/
python modulo_1_workflow_simple.py

# O con ruta completa
python ejemplos/modulo_1_workflow_simple.py
```

### 3. Experimentar

Los ejemplos están diseñados para ser modificados fácilmente:

```python
# Ejemplo: Cambiar el modelo LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)  # Era gpt-4o-mini

# Ejemplo: Agregar nueva herramienta
@tool
def mi_herramienta(input: str) -> str:
    """Mi herramienta personalizada."""
    return "resultado"

tools = [calculator, get_weather, mi_herramienta]  # Agregar aquí
```

## 📖 Guía por Módulo

### Módulo 1: Fundamentos

#### `modulo_1_workflow_simple.py`
**Concepto**: Workflow determinístico con prompt chaining

```python
# Flujo: Extract → Summarize → Translate
workflow.add_edge("extract", "summarize")
workflow.add_edge("summarize", "translate")
```

**Cuándo usar**: Procesos predecibles con pasos fijos

---

#### `modulo_1_agente_basico.py`
**Concepto**: Agente autónomo con ReAct pattern

```python
# El agente decide cuándo usar herramientas
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {"continue": "tools", "end": END}
)
```

**Cuándo usar**: Tareas que requieren razonamiento y uso de herramientas

---

### Módulo 2: Patrones Multi-Agente

#### `modulo_2_routing.py`
**Concepto**: Clasificador rutea a agentes especializados

```python
# Classifier → [Tech, Sales, General]
workflow.add_conditional_edges(
    "classifier",
    route_query,
    {"tech": "tech", "sales": "sales", "general": "general"}
)
```

**Cuándo usar**: Diferentes consultas requieren diferentes expertos

---

#### `modulo_2_parallelization.py`
**Concepto**: Múltiples agentes analizan en paralelo

```python
# Broadcast → [Optimistic, Pessimistic, Neutral] → Aggregator
workflow.add_edge("broadcast", "optimistic")
workflow.add_edge("broadcast", "pessimistic")
workflow.add_edge("broadcast", "neutral")
```

**Cuándo usar**: Necesitas múltiples perspectivas sobre lo mismo

---

#### `modulo_2_orchestrator.py`
**Concepto**: Orquestador divide y luego sintetiza

```python
# Orchestrator → [Workers] → Orchestrator
# Diamond pattern: divide y conquista
```

**Cuándo usar**: Trabajo grande dividible en sub-tareas independientes

---

### Módulo 3: Agentes Autónomos

#### `modulo_3_plan_execute.py`
**Concepto**: Planificación explícita antes de ejecutar

```python
# Planner → Executor → Evaluator → [Continue/Finish]
# Ciclos permiten replanificación
workflow.add_conditional_edges(
    "evaluator",
    route_decision,
    {"executor": "executor", "finish": "finish"}
)
```

**Cuándo usar**: Tareas complejas que se benefician de plan explícito

---

#### `modulo_3_handoffs.py`
**Concepto**: Agentes se pasan el control dinámicamente

```python
# Code Agent decide si necesita Security Agent
# Flujo NO predefinido, emerge en runtime
```

**Cuándo usar**: Problemas multi-dimensionales donde secuencia no es clara

---

#### `modulo_3_memoria.py`
**Concepto**: Memoria compartida que persiste entre sesiones

```python
# shared_memory se reutiliza entre invocaciones
# El sistema aprende con cada interacción
```

**Cuándo usar**: Valor acumulativo, aprendizaje continuo

---

### Módulo 4: Aplicaciones de Negocio

#### `modulo_4_customer_support.py`
**Concepto**: Sistema completo integrando múltiples patterns

```python
# Combina: Routing + Especialización + Confidence + Escalamiento
```

**Caso de uso**: Atención al cliente automatizada

---

#### `modulo_4_document_pipeline.py`
**Concepto**: Pipeline multi-etapa con validación

```python
# Preprocess → [Analysts paralelos] → Aggregate → Validate
```

**Caso de uso**: Análisis de documentos legales/financieros

---

## 💡 Tips para Aprender

1. **Empieza por el Módulo 1**: Asegúrate de entender workflows vs agentes
2. **Ejecuta cada ejemplo**: No solo leas, corre el código
3. **Modifica y experimenta**: Cambia prompts, agrega nodos, prueba variaciones
4. **Compara con ejercicios**: Después de entender el ejemplo, ve al ejercicio completo
5. **Combina patterns**: Los patterns se pueden mezclar (ej: routing + memoria)

## 🔧 Troubleshooting

### Error: "No module named 'langchain'"
```bash
pip install -r ../requirements.txt
```

### Error: "AuthenticationError"
```bash
# Configura tu API key
export OPENAI_API_KEY="sk-..."
```

### Ejemplo se ejecuta pero sin output
```bash
# Algunos ejemplos son verbosos, verifica la salida completa
python modulo_1_workflow_simple.py | less
```

## 📚 Recursos Adicionales

- **Ejercicios completos**: Ver `/ejercicios/modulo_X/`
- **Documentación teórica**: Ver `/docs/`
- **Documentación oficial**: [LangGraph Docs](https://langchain-ai.github.io/langgraph/)

## 🤝 Contribuir

Para agregar un nuevo ejemplo:

1. Mantén el código < 200 líneas
2. Enfócate en UN concepto clave
3. Incluye comentarios explicativos
4. Asegúrate que sea ejecutable standalone
5. Sigue la convención de nombres: `modulo_X_concepto.py`

---

**¡Happy coding!** 🚀

Para preguntas o feedback sobre los ejemplos, revisa la documentación completa en `/docs/` o los ejercicios detallados en `/ejercicios/`.
