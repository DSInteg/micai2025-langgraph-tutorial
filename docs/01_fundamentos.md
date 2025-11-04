# Módulo 1: Fundamentos de LangGraph y Sistemas Agénticos

## Índice
1. [Introducción](#introducción)
2. [Workflows vs Agentes](#workflows-vs-agentes)
3. [Componentes de LangGraph](#componentes-de-langgraph)
4. [Anatomía de un Sistema Agéntico](#anatomía-de-un-sistema-agéntico)
5. [El Pattern ReAct](#el-pattern-react)
6. [Cuándo Usar Cada Enfoque](#cuándo-usar-cada-enfoque)
7. [Referencias](#referencias)

---

## Introducción

Los **sistemas basados en LLMs** (Large Language Models) han evolucionado significativamente desde simples prompts hasta arquitecturas complejas que combinan razonamiento, herramientas y memoria. Este módulo establece los fundamentos para entender y construir estos sistemas usando **LangGraph**, un framework diseñado específicamente para orquestar aplicaciones con LLMs.

### ¿Por qué LangGraph?

LangGraph resuelve problemas fundamentales al construir sistemas con LLMs:

1. **Orquestación Explícita**: Define flujos de control como grafos (DAGs o cíclicos)
2. **Estado Compartido**: Gestiona el estado a través de múltiples pasos
3. **Flexibilidad**: Soporta desde workflows simples hasta agentes autónomos complejos
4. **Observabilidad**: Integración nativa con LangSmith para debugging
5. **Producción-Ready**: Checkpointing, persistencia y manejo de errores

---

## Workflows vs Agentes

La distinción fundamental en sistemas con LLMs es entre **workflows determinísticos** y **agentes autónomos**.

### Workflows Determinísticos

Un workflow es una secuencia predefinida de operaciones que se ejecutan en un orden específico.

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Input   │ -> │  Step 1  │ -> │  Step 2  │ -> │  Output  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

**Características:**
- ✅ **Predecible**: Siempre sigue el mismo camino
- ✅ **Fácil de debuggear**: El flujo es explícito
- ✅ **Menor costo**: Menos llamadas al LLM
- ✅ **Rápido**: No hay decisiones que tomar
- ❌ **Inflexible**: No se adapta a cambios en el input

**Ejemplo de uso:**
- Pipelines de ETL (Extract, Transform, Load)
- Procesamiento de documentos multi-etapa
- Validación de datos secuencial
- Generación de reportes estructurados

**Código conceptual:**
```python
def workflow(input):
    result1 = step1(input)
    result2 = step2(result1)
    result3 = step3(result2)
    return result3
```

### Agentes Autónomos

Un agente es un sistema que **decide dinámicamente** qué hacer en cada paso basándose en el contexto.

```
┌──────────┐    ┌──────────────┐
│  Input   │ -> │  LLM Decide  │
└──────────┘    └──────┬───────┘
                       │
            ┌──────────┴──────────┐
            ▼                     ▼
     ┌──────────┐          ┌──────────┐
     │  Tool A  │          │  Tool B  │
     └──────┬───┘          └──────┬───┘
            │                     │
            └──────────┬──────────┘
                       ▼
               ┌──────────────┐
               │  LLM Decide  │ ─────> ¿Continuar?
               └──────────────┘
```

**Características:**
- ✅ **Flexible**: Se adapta a diferentes inputs
- ✅ **Autónomo**: Toma decisiones sin programación explícita
- ✅ **Robusto**: Puede manejar casos no previstos
- ❌ **Impredecible**: El camino varía según el contexto
- ❌ **Más costoso**: Múltiples llamadas al LLM
- ❌ **Más lento**: Cada decisión toma tiempo

**Ejemplo de uso:**
- Asistentes conversacionales
- Sistemas de investigación autónomos
- Resolución de problemas complejos
- Interfaces de lenguaje natural para APIs

**Código conceptual:**
```python
def agent(input):
    state = {"input": input, "done": False}
    while not state["done"]:
        action = llm_decide(state)
        result = execute_action(action)
        state = update_state(state, result)
    return state["output"]
```

### Comparación Directa

| Aspecto | Workflow | Agente |
|---------|----------|--------|
| **Flujo** | Predefinido y fijo | Dinámico y adaptativo |
| **Decisiones** | No toma decisiones | Decide en cada paso |
| **Complejidad** | Baja | Media a Alta |
| **Costo** | Bajo (menos llamadas LLM) | Alto (múltiples llamadas) |
| **Latencia** | Baja (sin decisiones) | Alta (razonamiento) |
| **Debugging** | Fácil (flujo explícito) | Difícil (emergente) |
| **Casos de uso** | Procesos conocidos | Problemas abiertos |
| **Herramientas** | Opcionales | Esenciales |

---

## Componentes de LangGraph

LangGraph se basa en tres primitivas fundamentales:

### 1. State (Estado)

El estado es un **diccionario tipado** que fluye a través del grafo.

```python
from typing import TypedDict

class MyState(TypedDict):
    input: str
    intermediate_result: str
    output: str
```

**Características importantes:**
- Se define usando `TypedDict` para type hints
- Cada nodo puede leer cualquier campo
- Los nodos retornan solo los campos que actualizan
- LangGraph fusiona automáticamente los updates

**Reducers especiales:**

```python
from typing import Annotated
from langgraph.graph.message import add_messages

class StateWithMessages(TypedDict):
    # add_messages es un reducer que agrega mensajes en lugar de reemplazarlos
    messages: Annotated[list[BaseMessage], add_messages]
```

### 2. Nodes (Nodos)

Los nodos son **funciones** que transforman el estado.

```python
def my_node(state: MyState) -> dict:
    """
    Un nodo recibe el estado y retorna un diccionario
    con los campos a actualizar.
    """
    # Leer del estado
    input_data = state["input"]

    # Procesar (llamar LLM, usar herramienta, etc.)
    result = process(input_data)

    # Retornar solo campos actualizados
    return {"intermediate_result": result}
```

**Tipos de nodos comunes:**

1. **Nodos de procesamiento**: Transforman datos
2. **Nodos de LLM**: Invocan modelos de lenguaje
3. **Nodos de herramientas**: Ejecutan tools
4. **Nodos de decisión**: Clasifican o rutean

### 3. Graph (Grafo)

El grafo conecta nodos en un flujo de ejecución.

```python
from langgraph.graph import StateGraph, END

# Crear grafo
workflow = StateGraph(MyState)

# Agregar nodos
workflow.add_node("node1", my_node_function)
workflow.add_node("node2", another_node_function)

# Definir flujo
workflow.set_entry_point("node1")
workflow.add_edge("node1", "node2")
workflow.add_edge("node2", END)

# Compilar
app = workflow.compile()
```

### 4. Edges (Conexiones)

Existen dos tipos de edges:

#### a) **Edges Incondicionales**
Siempre siguen el mismo camino.

```python
workflow.add_edge("node_a", "node_b")
```

#### b) **Conditional Edges**
Deciden dinámicamente el siguiente nodo.

```python
def router(state: MyState) -> str:
    """Función que decide el siguiente nodo"""
    if state["some_condition"]:
        return "path_a"
    else:
        return "path_b"

workflow.add_conditional_edges(
    "decision_node",
    router,
    {
        "path_a": "node_a",
        "path_b": "node_b"
    }
)
```

---

## Anatomía de un Sistema Agéntico

Un sistema agéntico con LLM se compone de:

### 1. LLM Aumentado

El LLM (modelo de lenguaje) es el "cerebro" del sistema.

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
)
```

**Parámetros importantes:**
- `model`: El modelo a usar (gpt-4, claude-3, etc.)
- `temperature`: Aleatoriedad (0 = determinista, 1 = creativo)
- `max_tokens`: Límite de tokens en la respuesta

### 2. Herramientas (Tools)

Las herramientas son **funciones que el LLM puede invocar**.

```python
from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """
    Calcula expresiones matemáticas.

    Args:
        expression: Expresión matemática (ej: "2 + 2")

    Returns:
        Resultado del cálculo
    """
    return str(eval(expression))
```

**Importante:**
- El docstring es crucial: el LLM lo usa para decidir cuándo usar la tool
- Los type hints definen el esquema de entrada
- El nombre de la función es cómo el LLM la invoca

**Vincular tools al LLM:**

```python
tools = [calculator, search, other_tool]
llm_with_tools = llm.bind_tools(tools)
```

### 3. Memoria (State Management)

La memoria permite al sistema recordar información entre pasos.

```python
from typing import Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # Los mensajes se acumulan (no se reemplazan)
    messages: Annotated[Sequence[BaseMessage], add_messages]
```

**Tipos de memoria:**

1. **Short-term (Working memory)**: El estado del grafo
2. **Long-term**: Persistencia entre sesiones (checkpoints)
3. **Semantic**: RAG (Retrieval-Augmented Generation)

### 4. Ciclo de Control

El ciclo que orquesta el sistema.

```python
def build_agent_graph():
    workflow = StateGraph(AgentState)

    # Nodo que razona y decide
    workflow.add_node("agent", agent_node)

    # Nodo que ejecuta herramientas
    workflow.add_node("tools", tool_node)

    # Ciclo: agent -> tools -> agent
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {"continue": "tools", "end": END}
    )
    workflow.add_edge("tools", "agent")

    return workflow.compile()
```

---

## El Pattern ReAct

**ReAct** (Reasoning + Acting) es el patrón fundamental para agentes con LLMs.

### Ciclo ReAct

```
1. REASON (Razonar)
   ↓
   "Necesito saber X para responder"
   ↓
2. ACT (Actuar)
   ↓
   Llamar herramienta con parámetros
   ↓
3. OBSERVE (Observar)
   ↓
   Ver resultado de la herramienta
   ↓
   ¿Tengo suficiente información?
   NO → Volver a REASON
   SÍ → RESPOND (Responder)
```

### Ejemplo de Trace ReAct

```
Usuario: "¿Cuál es el 15% de 250 más el precio del producto X?"

[1] REASON
Agente: "Necesito calcular 15% de 250 y buscar el precio del producto X"

[2] ACT
Agente: tool_calls=[
    {"name": "calculator", "args": {"expression": "15% of 250"}}
]

[3] OBSERVE
Tool: "37.5"

[4] REASON (continúa)
Agente: "Ahora necesito el precio del producto X"

[5] ACT
Agente: tool_calls=[
    {"name": "search_knowledge", "args": {"query": "precio producto X"}}
]

[6] OBSERVE
Tool: "El precio del producto X es $120"

[7] REASON (final)
Agente: "Tengo ambas piezas, puedo calcular el total"

[8] ACT
Agente: tool_calls=[
    {"name": "calculator", "args": {"expression": "37.5 + 120"}}
]

[9] OBSERVE
Tool: "157.5"

[10] RESPOND
Agente: "El resultado es $157.5 (15% de 250 = $37.5, más el precio del
         producto X = $120)"
```

### Implementación en LangGraph

```python
def agent_node(state: AgentState):
    """Nodo que implementa REASON y decide ACT"""
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def tool_node(state: AgentState):
    """Nodo que implementa ACT y OBSERVE"""
    last_message = state["messages"][-1]
    tool_calls = last_message.tool_calls

    tool_messages = []
    for call in tool_calls:
        result = execute_tool(call)
        tool_messages.append(ToolMessage(result, call["id"]))

    return {"messages": tool_messages}

def should_continue(state: AgentState):
    """Decide si continuar el ciclo o terminar"""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "continue"  # Hay herramientas por ejecutar
    return "end"  # El agente dio una respuesta final
```

---

## Cuándo Usar Cada Enfoque

### Usa Workflows Cuando:

✅ **Conoces los pasos exactos**
```
Ejemplo: Pipeline de procesamiento de CV
1. Extraer texto del PDF
2. Identificar secciones
3. Extraer información estructurada
4. Validar contra requisitos
5. Generar reporte
```

✅ **El proceso es repetitivo y predecible**
```
Ejemplo: Generación de reportes diarios
- Los pasos siempre son los mismos
- Solo varían los datos de entrada
```

✅ **La eficiencia es crítica**
```
Ejemplo: Procesamiento de alto volumen
- Costo por llamada LLM es significativo
- Latencia debe ser mínima
```

✅ **Necesitas debugging fácil**
```
Ejemplo: Sistemas en producción críticos
- Fácil identificar dónde falló
- Logs claros de cada paso
```

### Usa Agentes Cuando:

✅ **No conoces los pasos de antemano**
```
Ejemplo: Asistente de investigación
- La consulta puede requerir 1, 3 o 10 pasos
- Depende de qué encuentre en cada búsqueda
```

✅ **Necesitas adaptabilidad**
```
Ejemplo: Soporte técnico automatizado
- Diferentes problemas requieren diferentes soluciones
- El agente debe diagnosticar y resolver
```

✅ **El problema requiere razonamiento**
```
Ejemplo: Análisis de código complejo
- Necesita entender el contexto
- Decidir qué archivos revisar
- Adaptar el análisis según lo que encuentre
```

✅ **Tienes herramientas variadas**
```
Ejemplo: Asistente personal
- Múltiples APIs y servicios
- El agente decide cuáles usar y en qué orden
```

### Enfoque Híbrido

En la práctica, **combinar ambos** suele ser óptimo:

```python
# Workflow principal con pasos agénticos

def hybrid_system():
    # PASO 1: Workflow - Clasificación
    category = classify_query(user_input)

    # PASO 2: Agent - Resolver según categoría
    if category == "technical":
        result = technical_agent(user_input)
    elif category == "sales":
        result = sales_agent(user_input)

    # PASO 3: Workflow - Formatear respuesta
    formatted = format_response(result)

    return formatted
```

---

## Referencias

### Documentación Oficial
- [LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview.md)
- [LangGraph Quickstart](https://docs.langchain.com/oss/python/langgraph/quickstart.md)
- [Workflows and Agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents.md)
- [Thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph.md)

### Papers Importantes
- **ReAct: Synergizing Reasoning and Acting in Language Models** (Yao et al., 2022)
- **Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** (Wei et al., 2022)
- **Reflexion: Language Agents with Verbal Reinforcement Learning** (Shinn et al., 2023)

### Recursos Adicionales
- [LangChain Academy](https://docs.langchain.com/oss/python/langchain/academy.md)
- [LangGraph Agents Guide](https://docs.langchain.com/oss/python/langchain/agents.md)
- [Tool Calling Documentation](https://docs.langchain.com/oss/python/langchain/tools.md)

---

## Siguiente Módulo

En el **Módulo 2: Patrones de Workflows Multi-Agente**, exploraremos:
- Routing y clasificación
- Paralelización (sectioning y voting)
- Orchestrator-Workers pattern
- Evaluator-Optimizer pattern

¡Continúa al Módulo 2 para aprender a coordinar múltiples agentes! 🚀
