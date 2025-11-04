# Módulo 2: Patrones de Workflows Multi-Agente

## Índice
1. [Introducción](#introducción)
2. [Pattern 1: Routing](#pattern-1-routing)
3. [Pattern 2: Paralelización](#pattern-2-paralelización)
4. [Pattern 3: Orchestrator-Workers](#pattern-3-orchestrator-workers)
5. [Comparación de Patrones](#comparación-de-patrones)
6. [Cuándo Usar Cada Patrón](#cuándo-usar-cada-patrón)
7. [Referencias](#referencias)

---

## Introducción

Los **workflows multi-agente** son sistemas donde múltiples agentes o nodos especializados trabajan juntos de manera coordinada para resolver problemas complejos. A diferencia de un solo agente autónomo, estos sistemas siguen patrones arquitectónicos predefinidos que determinan cómo fluye la información y cómo se coordinan los agentes.

### ¿Por qué Workflows Multi-Agente?

Los workflows multi-agente resuelven limitaciones fundamentales de los agentes únicos:

**Problemas del agente único:**
- Intenta ser experto en todo (generalista, no especialista)
- Prompts largos y complejos
- Difícil de mantener y actualizar
- No escala bien con la complejidad

**Ventajas multi-agente:**
- ✅ **Especialización**: Cada agente es experto en su dominio
- ✅ **Modularidad**: Fácil agregar/modificar agentes individuales
- ✅ **Escalabilidad**: Crece con la complejidad del problema
- ✅ **Mantenibilidad**: Prompts focalizados y claros
- ✅ **Rendimiento**: Potencial para paralelización

### Los Tres Patrones Fundamentales

Este módulo cubre tres patrones esenciales para sistemas multi-agente:

1. **Routing (Enrutamiento)**: Dirigir consultas a agentes especializados
2. **Paralelización (Map-Reduce)**: Múltiples perspectivas simultáneas
3. **Orchestrator-Workers**: División de problemas complejos

---

## Pattern 1: Routing

### Concepto

El **routing** es el patrón más simple y común en sistemas multi-agente. Funciona como un sistema de triaje:

1. Un **clasificador** analiza la entrada
2. La entrada se **dirige** a un agente especializado
3. El agente especializado **procesa** y responde

```
┌─────────────────────────────────────────────┐
│              Input del Usuario              │
└───────────────────┬─────────────────────────┘
                    │
                    ▼
          ┌──────────────────┐
          │   Clasificador   │
          │   (Router Node)  │
          └────────┬─────────┘
                   │
      ┌────────────┼────────────┐
      ▼            ▼            ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Agente A │ │ Agente B │ │ Agente C │
│ Técnico  │ │  Ventas  │ │ Soporte  │
└──────────┘ └──────────┘ └──────────┘
      │            │            │
      └────────────┼────────────┘
                   ▼
             Respuesta Final
```

### Implementación en LangGraph

**Paso 1: Clasificador con LLM**
```python
def classifier_node(state: State) -> dict:
    """Clasifica la consulta en una categoría."""
    query = state["query"]

    prompt = f"""Clasifica esta consulta en UNA categoría:
    - technical: Problemas técnicos, errores
    - sales: Precios, productos, compras
    - support: Devoluciones, garantías

    Consulta: {query}

    Responde SOLO con: technical, sales, o support"""

    category = llm.invoke(prompt).content.strip().lower()
    return {"category": category}
```

**Paso 2: Función de Routing**
```python
def route_query(state: State) -> str:
    """Decide el siguiente nodo basándose en la categoría."""
    routing_map = {
        "technical": "technical_agent",
        "sales": "sales_agent",
        "support": "support_agent"
    }
    return routing_map[state["category"]]
```

**Paso 3: Grafo con Conditional Edges**
```python
workflow = StateGraph(State)

workflow.add_node("classifier", classifier_node)
workflow.add_node("technical_agent", technical_agent)
workflow.add_node("sales_agent", sales_agent)
workflow.add_node("support_agent", support_agent)

workflow.set_entry_point("classifier")

# Conditional edge: routing dinámico
workflow.add_conditional_edges(
    "classifier",
    route_query,
    {
        "technical_agent": "technical_agent",
        "sales_agent": "sales_agent",
        "support_agent": "support_agent"
    }
)

# Todos terminan
workflow.add_edge("technical_agent", END)
workflow.add_edge("sales_agent", END)
workflow.add_edge("support_agent", END)
```

### Variantes de Routing

#### 1. LLM-Based Routing (Flexible)
El clasificador usa un LLM para categorizar.

**Ventajas**:
- Maneja lenguaje natural
- Flexible a nuevas formulaciones
- No requiere mantenimiento de reglas

**Desventajas**:
- Más lento (llamada extra al LLM)
- Más costoso
- Puede ser impredecible

#### 2. Rule-Based Routing (Rápido)
Usa keywords o regex para clasificar.

```python
def rule_based_classifier(query: str) -> str:
    query_lower = query.lower()

    if any(word in query_lower for word in ["error", "bug", "falla"]):
        return "technical"
    elif any(word in query_lower for word in ["precio", "costo", "comprar"]):
        return "sales"
    elif any(word in query_lower for word in ["devolver", "garantía"]):
        return "support"

    return "general"  # Default
```

**Ventajas**:
- Muy rápido
- Determinista
- Gratuito (sin llamadas LLM)

**Desventajas**:
- Rígido
- Requiere mantenimiento manual
- No maneja sinónimos

#### 3. Embedding-Based Routing (Robusto)
Usa similaridad semántica con ejemplos.

```python
from langchain.embeddings import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

# Pre-definir ejemplos de cada categoría
category_examples = {
    "technical": ["mi app crashea", "error 500", "no puedo login"],
    "sales": ["cuánto cuesta", "quiero comprar", "opciones de pago"],
    "support": ["devolver producto", "garantía", "reembolso"]
}

def embedding_based_classifier(query: str) -> str:
    query_embedding = embeddings.embed_query(query)

    best_category = None
    best_similarity = -1

    for category, examples in category_examples.items():
        for example in examples:
            example_embedding = embeddings.embed_query(example)
            similarity = cosine_similarity(query_embedding, example_embedding)

            if similarity > best_similarity:
                best_similarity = similarity
                best_category = category

    return best_category
```

**Ventajas**:
- Robusto a variaciones
- Maneja sinónimos
- No necesita reglas manuales

**Desventajas**:
- Requiere setup de embeddings
- Más lento que reglas
- Necesita buenos ejemplos

### Casos de Uso del Routing

✅ **Ideal para**:
- Sistemas de atención al cliente
- Triaje de tickets de soporte
- Routing de consultas en chatbots
- Clasificación de documentos

❌ **No usar para**:
- Consultas que requieren múltiples perspectivas
- Problemas que no tienen categorías claras
- Cuando necesitas consenso de múltiples expertos

---

## Pattern 2: Paralelización

### Concepto

La **paralelización** ejecuta múltiples agentes simultáneamente sobre el **mismo input** para obtener perspectivas diversas, luego **agrega** los resultados.

```
                ┌────────────────┐
   Input   ────►│   Broadcast    │
                └────┬─────┬─────┘
                     │     │
          ┌──────────┴─────┴──────────┐
          │      EJECUCIÓN PARALELA   │
     ┌────▼────┐  ┌────▼────┐  ┌────▼────┐
     │ Agente  │  │ Agente  │  │ Agente  │
     │    A    │  │    B    │  │    C    │
     └────┬────┘  └────┬────┘  └────┬────┘
          │            │            │
          └────────────┼────────────┘
                       ▼
              ┌────────────────┐
              │   Aggregator   │
              │    (Síntesis)  │
              └────────┬───────┘
                       ▼
                Final Result
```

### Implementación en LangGraph

**Paso 1: Agentes con Perspectivas**
```python
def optimistic_agent(state: State) -> dict:
    """Analiza enfocándose en aspectos positivos."""
    review = state["review"]

    prompt = f"""Analiza esta reseña enfocándote en ASPECTOS POSITIVOS:
    {review}

    Resalta fortalezas y beneficios."""

    analysis = llm.invoke(prompt)
    return {"optimistic_analysis": analysis.content}


def pessimistic_agent(state: State) -> dict:
    """Analiza enfocándose en aspectos negativos."""
    review = state["review"]

    prompt = f"""Analiza esta reseña enfocándote en PROBLEMAS:
    {review}

    Identifica debilidades y riesgos."""

    analysis = llm.invoke(prompt)
    return {"pessimistic_analysis": analysis.content}


def neutral_agent(state: State) -> dict:
    """Analiza de manera balanceada."""
    review = state["review"]

    prompt = f"""Analiza esta reseña de manera OBJETIVA Y BALANCEADA:
    {review}

    Proporciona perspectiva equilibrada."""

    analysis = llm.invoke(prompt)
    return {"neutral_analysis": analysis.content}
```

**Paso 2: Aggregator**
```python
def aggregator_node(state: State) -> dict:
    """Sintetiza las múltiples perspectivas."""
    analyses = [
        state["optimistic_analysis"],
        state["pessimistic_analysis"],
        state["neutral_analysis"]
    ]

    prompt = f"""Sintetiza estos análisis en uno balanceado:

    Optimista: {analyses[0]}
    Pesimista: {analyses[1]}
    Neutral: {analyses[2]}

    Integra las perspectivas y proporciona conclusión."""

    final = llm.invoke(prompt)
    return {"final_analysis": final.content}
```

**Paso 3: Grafo Paralelo**
```python
workflow = StateGraph(State)

# Nodo broadcast (opcional, para claridad)
workflow.add_node("broadcast", lambda s: {})

# Agentes que se ejecutan en paralelo
workflow.add_node("optimistic", optimistic_agent)
workflow.add_node("pessimistic", pessimistic_agent)
workflow.add_node("neutral", neutral_agent)

# Aggregator
workflow.add_node("aggregator", aggregator_node)

# Configurar paralelismo
workflow.set_entry_point("broadcast")

# Múltiples edges = paralelismo
workflow.add_edge("broadcast", "optimistic")
workflow.add_edge("broadcast", "pessimistic")
workflow.add_edge("broadcast", "neutral")

# Todos convergen en aggregator
workflow.add_edge("optimistic", "aggregator")
workflow.add_edge("pessimistic", "aggregator")
workflow.add_edge("neutral", "aggregator")

workflow.add_edge("aggregator", END)
```

### Variantes de Paralelización

#### 1. Voting/Consensus
Múltiples agentes "votan" y se toma la mayoría.

```python
def voting_aggregator(state: State) -> dict:
    votes = [
        state["agent1_vote"],
        state["agent2_vote"],
        state["agent3_vote"]
    ]

    # Tomar mayoría
    from collections import Counter
    majority_vote = Counter(votes).most_common(1)[0][0]

    return {"final_decision": majority_vote}
```

**Casos de uso**:
- Moderación de contenido
- Clasificación de documentos
- Detección de spam

#### 2. Weighted Aggregation
Dar más peso a ciertos agentes.

```python
def weighted_aggregator(state: State) -> dict:
    scores = [
        ("expert1", state["expert1_score"], 0.5),  # 50% peso
        ("expert2", state["expert2_score"], 0.3),  # 30% peso
        ("expert3", state["expert3_score"], 0.2)   # 20% peso
    ]

    weighted_score = sum(score * weight for _, score, weight in scores)
    return {"final_score": weighted_score}
```

#### 3. Ensemble (Promedio)
Combinar predicciones de múltiples modelos.

```python
def ensemble_aggregator(state: State) -> dict:
    predictions = [
        state["model1_prediction"],
        state["model2_prediction"],
        state["model3_prediction"]
    ]

    avg_prediction = sum(predictions) / len(predictions)
    return {"final_prediction": avg_prediction}
```

### Casos de Uso de Paralelización

✅ **Ideal para**:
- Análisis multi-perspectiva (sentiment, opiniones)
- Reducción de sesgo (múltiples opiniones)
- Moderación de contenido (consenso)
- Evaluación de calidad (múltiples criterios)

❌ **No usar para**:
- Problemas con una sola respuesta correcta
- Cuando el costo es crítico (múltiples llamadas LLM)
- Tareas donde las perspectivas son redundantes

---

## Pattern 3: Orchestrator-Workers

### Concepto

El **orchestrator-workers** divide un problema complejo en sub-tareas, asigna cada sub-tarea a un worker especializado, y ensambla los resultados.

```
                ┌────────────────────────┐
   Input   ────►│  Orchestrator (Plan)   │
                │  Divide en sub-tareas  │
                └───────────┬────────────┘
                            │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
    Sub-tarea 1        Sub-tarea 2        Sub-tarea 3
         │                  │                  │
         ▼                  ▼                  ▼
    ┌─────────┐        ┌─────────┐        ┌─────────┐
    │Worker 1 │        │Worker 2 │        │Worker 3 │
    │Executive│        │Technical│        │Financial│
    └────┬────┘        └────┬────┘        └────┬────┘
         │                  │                  │
         └──────────────────┼──────────────────┘
                            ▼
                ┌────────────────────────┐
                │ Orchestrator (Synth)   │
                │ Ensambla resultados    │
                └────────────┬───────────┘
                             ▼
                       Final Report
```

### Implementación en LangGraph

**Paso 1: Orchestrator de Planificación**
```python
def orchestrator_plan(state: State) -> dict:
    """Analiza el problema y divide en sub-tareas."""
    document = state["document"]

    # Dividir documento en secciones
    sections = {
        "executive": extract_executive_section(document),
        "technical": extract_technical_section(document),
        "financial": extract_financial_section(document)
    }

    return sections
```

**Paso 2: Workers Especializados**
```python
def executive_worker(state: State) -> dict:
    """Worker experto en análisis ejecutivo."""
    section = state["executive"]

    prompt = f"""Como consultor ejecutivo, analiza:
    {section}

    Proporciona análisis estratégico de alto nivel."""

    analysis = llm.invoke(prompt)
    return {"executive_analysis": analysis.content}


def technical_worker(state: State) -> dict:
    """Worker experto en análisis técnico."""
    section = state["technical"]

    prompt = f"""Como arquitecto técnico, analiza:
    {section}

    Proporciona análisis técnico detallado."""

    analysis = llm.invoke(prompt)
    return {"technical_analysis": analysis.content}
```

**Paso 3: Orchestrator de Síntesis**
```python
def orchestrator_synthesize(state: State) -> dict:
    """Ensambla los análisis parciales."""
    analyses = {
        "executive": state["executive_analysis"],
        "technical": state["technical_analysis"],
        "financial": state["financial_analysis"]
    }

    prompt = f"""Integra estos análisis especializados:

    Ejecutivo: {analyses['executive']}
    Técnico: {analyses['technical']}
    Financiero: {analyses['financial']}

    Crea un reporte ejecutivo coherente."""

    report = llm.invoke(prompt)
    return {"final_report": report.content}
```

**Paso 4: Grafo "Diamante"**
```python
workflow = StateGraph(State)

# Orchestrator inicial
workflow.add_node("plan", orchestrator_plan)

# Workers especializados
workflow.add_node("exec_worker", executive_worker)
workflow.add_node("tech_worker", technical_worker)
workflow.add_node("fin_worker", financial_worker)

# Orchestrator final
workflow.add_node("synthesize", orchestrator_synthesize)

# Flujo
workflow.set_entry_point("plan")

# Paralelismo: plan → workers
workflow.add_edge("plan", "exec_worker")
workflow.add_edge("plan", "tech_worker")
workflow.add_edge("plan", "fin_worker")

# Convergencia: workers → synthesize
workflow.add_edge("exec_worker", "synthesize")
workflow.add_edge("tech_worker", "synthesize")
workflow.add_edge("fin_worker", "synthesize")

workflow.add_edge("synthesize", END)
```

### Variantes de Orchestrator-Workers

#### 1. Secuencial
Workers se ejecutan uno tras otro (no paralelo).

**Ventaja**: Cada worker puede usar resultados del anterior
**Desventaja**: Más lento

#### 2. Paralelo (Más común)
Workers se ejecutan simultáneamente.

**Ventaja**: Más rápido
**Desventaja**: Workers no comparten información

#### 3. Jerárquico
Orchestrators anidados para problemas muy complejos.

```
Master Orchestrator
  ├─ Sub-Orchestrator A
  │   ├─ Worker A1
  │   └─ Worker A2
  └─ Sub-Orchestrator B
      ├─ Worker B1
      └─ Worker B2
```

#### 4. Adaptativo
El orchestrator ajusta el plan basándose en resultados intermedios.

### Casos de Uso de Orchestrator-Workers

✅ **Ideal para**:
- Análisis de documentos largos (contratos, reportes)
- Procesamiento de datos multi-facético
- Proyectos complejos con múltiples aspectos
- Revisión de código (diferentes archivos)

❌ **No usar para**:
- Problemas simples (overhead innecesario)
- Cuando la división no es clara
- Tareas que requieren contexto global constante

---

## Comparación de Patrones

| Aspecto | Routing | Paralelización | Orchestrator-Workers |
|---------|---------|----------------|---------------------|
| **Agentes activos** | 1 por consulta | N simultáneos | N secuencial/paralelo |
| **Input** | Diferentes por agente | Mismo para todos | Diferentes sub-tareas |
| **Coordinación** | Clasificador | Aggregator | Orchestrator (2 etapas) |
| **Costo** | Bajo (1-2 LLMs) | Alto (N+1 LLMs) | Medio-Alto (N+2 LLMs) |
| **Latencia** | Baja | Media (paralelo) | Media-Alta |
| **Complejidad** | Baja | Media | Alta |
| **Escalabilidad** | +++| + | +++ |
| **Flexibilidad** | + | + | +++ |

---

## Cuándo Usar Cada Patrón

### Usar Routing cuando:
- ✅ Necesitas dirigir consultas a expertos específicos
- ✅ Las categorías son claras y mutuamente excluyentes
- ✅ Cada consulta requiere solo un tipo de expertise
- ✅ Costo y latencia son críticos

**Ejemplo**: Sistema de atención al cliente con departamentos

### Usar Paralelización cuando:
- ✅ Necesitas múltiples perspectivas del mismo input
- ✅ Quieres reducir sesgo o mejorar robustez
- ✅ El consenso es importante
- ✅ El costo adicional justifica la calidad mejorada

**Ejemplo**: Análisis de sentimiento, moderación de contenido

### Usar Orchestrator-Workers cuando:
- ✅ El problema es naturalmente divisible en sub-problemas
- ✅ Cada sub-problema requiere expertise específico
- ✅ Necesitas análisis profundo de múltiples aspectos
- ✅ El resultado final debe integrar todas las perspectivas

**Ejemplo**: Análisis de documentos complejos, revisión de código

---

## Referencias

### Documentación Oficial
- [LangGraph Multi-Agent Systems](https://docs.langchain.com/oss/python/langchain/multi-agent.md)
- [Conditional Edges](https://docs.langchain.com/oss/python/langgraph/graph-api.md)
- [Map-Reduce](https://docs.langchain.com/oss/python/langchain/retrieval.md)

### Papers y Artículos
- **Multi-Agent Systems in AI**: Russell & Norvig, "Artificial Intelligence: A Modern Approach"
- **Ensemble Methods**: Dietterich, "Ensemble Methods in Machine Learning"
- **Orchestration Patterns**: Hohpe & Woolf, "Enterprise Integration Patterns"

---

## Siguiente Módulo

¡Felicidades! Has completado el **Módulo 2: Patrones de Workflows Multi-Agente**.

En el **Módulo 3: Redes de Agentes Autónomos**, aprenderás patrones avanzados donde:
- Los agentes toman decisiones dinámicas
- Hay memoria compartida y comunicación entre agentes
- Los sistemas se adaptan durante la ejecución
- Se implementan estrategias de handoff y delegación

¡Continúa al Módulo 3 para llevar tus sistemas multi-agente al siguiente nivel! 🚀
