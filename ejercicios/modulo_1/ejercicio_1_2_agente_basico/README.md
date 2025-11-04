# Ejercicio 1.2: Agente Básico Autónomo con Herramientas

## Objetivo

Aprender a construir un **agente autónomo** que puede:
- Decidir qué herramientas usar
- Ejecutar herramientas dinámicamente
- Razonar sobre cuándo ha completado su tarea

Este ejercicio introduce conceptos clave de agentes:
- ReAct pattern (Reasoning + Acting)
- Tool calling (invocación de herramientas)
- Conditional edges (decisiones dinámicas)
- Ciclos de razonamiento

## Contexto

Ahora vamos a construir un **asistente matemático** que puede:
1. **Realizar cálculos** usando una calculadora
2. **Buscar información** en una base de conocimiento simulada
3. **Decidir autónomamente** qué herramientas necesita
4. **Razonar** sobre si necesita más información o puede dar una respuesta final

**Ejemplo de interacción:**
```
Usuario: "¿Cuál es el 15% de 250 más el precio del producto X?"

Agente:
1. [Piensa] "Necesito calcular 15% de 250 y buscar el precio del producto X"
2. [Usa calculadora] "15% de 250 = 37.5"
3. [Busca información] "Precio producto X = 120"
4. [Usa calculadora] "37.5 + 120 = 157.5"
5. [Responde] "El resultado es 157.5"
```

## ¿Qué es un Agente?

Un **agente autónomo** es un sistema que:
- **Razona** sobre qué hacer a continuación
- **Actúa** usando herramientas disponibles
- **Observa** los resultados de sus acciones
- **Decide** si necesita más acciones o puede terminar

**Diferencias clave con Workflows:**

| Característica | Workflow | Agente |
|----------------|----------|--------|
| Flujo | Predefinido | Dinámico |
| Decisiones | No toma decisiones | Decide qué hacer |
| Herramientas | Opcionales | Esenciales |
| Complejidad | Baja | Media-Alta |
| Costo | Menor | Mayor (más llamadas al LLM) |

**Cuándo usar Agentes:**
- No conoces de antemano los pasos exactos
- El sistema debe adaptarse a diferentes inputs
- Necesitas razonamiento sobre qué hacer
- Las herramientas disponibles varían

## El Pattern ReAct

**ReAct** (Reasoning + Acting) es el patrón fundamental para agentes:

```
┌─────────────────────────────────────┐
│  1. REASON (Razonar)                │
│  "¿Qué necesito hacer?"             │
│  "¿Qué herramientas necesito?"      │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  2. ACT (Actuar)                    │
│  Llamar a una herramienta           │
│  Ejecutar la acción                 │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  3. OBSERVE (Observar)              │
│  Ver el resultado de la herramienta │
│  Agregar al contexto                │
└────────────┬────────────────────────┘
             │
             ▼
         ¿Terminé? ──NO──┐
             │           │
            SÍ           │
             │           │
             ▼           │
          RESPONDER      │
                         │
                         └──► Volver a REASON
```

## Conceptos Clave de Agentes en LangGraph

### 1. Tool Binding (Vincular Herramientas)

Las herramientas son funciones que el agente puede llamar:

```python
from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """
    Calcula una expresión matemática.

    Args:
        expression: Expresión matemática (ej: "2 + 2", "15% of 250")
    """
    # Implementación
    return result

# Vincular herramientas al LLM
llm_with_tools = llm.bind_tools([calculator, search_knowledge])
```

### 2. Conditional Edges (Decisiones Dinámicas)

A diferencia de los workflows, los agentes usan **conditional edges** para decidir qué hacer:

```python
# En lugar de: workflow.add_edge("nodo_a", "nodo_b")
# Usamos:
workflow.add_conditional_edges(
    "agent",
    should_continue,  # Función que decide el próximo paso
    {
        "continue": "action",  # Si debe usar herramienta
        "end": END             # Si debe terminar
    }
)
```

### 3. Tool Execution (Ejecución de Herramientas)

El agente decide qué herramienta llamar, y un nodo especial las ejecuta:

```python
def call_tools(state: AgentState) -> dict:
    """
    Ejecuta las herramientas que el agente solicitó.
    """
    # Obtener tool_calls del último mensaje
    tool_calls = state["messages"][-1].tool_calls

    # Ejecutar cada herramienta
    responses = []
    for tool_call in tool_calls:
        tool = tool_map[tool_call["name"]]
        result = tool.invoke(tool_call["args"])
        responses.append(ToolMessage(result, tool_call_id=tool_call["id"]))

    return {"messages": responses}
```

### 4. Estado con Mensajes

Los agentes usan una secuencia de mensajes como estado:

```python
from typing import Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """
    Estado de un agente con historial de mensajes.

    add_messages es un reducer especial que:
    - Agrega nuevos mensajes al historial
    - Mantiene el orden
    - Permite al LLM ver todo el contexto
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]
```

## Instrucciones

### Paso 1: Entender las Herramientas
Revisa las dos herramientas implementadas en `starter.py`:
- `calculator`: Realiza cálculos matemáticos
- `search_knowledge`: Busca información en una base de conocimiento simulada

### Paso 2: Implementar el Nodo del Agente
Completa la función `agent_node()`:
- Debe invocar el LLM con herramientas vinculadas
- El LLM decidirá si necesita usar herramientas o responder

### Paso 3: Implementar el Nodo de Herramientas
Completa la función `tool_node()`:
- Debe ejecutar las herramientas que el agente solicitó
- Debe retornar los resultados como `ToolMessage`

### Paso 4: Implementar la Función de Routing
Completa la función `should_continue()`:
- Debe verificar si el último mensaje tiene `tool_calls`
- Si tiene tool_calls → retornar "continue"
- Si no → retornar "end"

### Paso 5: Construir el Grafo
En `build_graph()`:
- Agregar nodo "agent"
- Agregar nodo "tools"
- Configurar conditional edges
- Conectar "tools" de vuelta a "agent" (¡ciclo!)

### Paso 6: Probar el Agente
Ejecuta con diferentes consultas:
```bash
python starter.py
```

## Criterios de Éxito

✅ El agente puede realizar cálculos usando la calculadora
✅ El agente puede buscar información en la base de conocimiento
✅ El agente usa múltiples herramientas cuando es necesario
✅ El agente responde correctamente después de obtener información
✅ El ciclo agent → tools → agent funciona correctamente
✅ El agente termina apropiadamente (no loop infinito)

## Tiempo Estimado

20 minutos

## Conceptos Aprendidos

Al completar este ejercicio, habrás aprendido:
- ✅ Cómo crear y vincular herramientas a un LLM
- ✅ Cómo implementar el pattern ReAct
- ✅ Cómo usar conditional edges para decisiones dinámicas
- ✅ Cómo crear ciclos en grafos de LangGraph
- ✅ Cómo manejar tool_calls y ToolMessages
- ✅ La diferencia fundamental entre workflows y agentes

## Pistas Adicionales

<details>
<summary>💡 Pista 1: Cómo vincular herramientas al LLM</summary>

```python
# Crear lista de herramientas
tools = [calculator, search_knowledge]

# Vincular al LLM
llm_with_tools = llm.bind_tools(tools)

# El LLM ahora puede decidir llamar estas herramientas
response = llm_with_tools.invoke(messages)
```
</details>

<details>
<summary>💡 Pista 2: Cómo verificar si hay tool_calls</summary>

```python
last_message = state["messages"][-1]

# Los modelos que soportan tool calling agregan este atributo
if hasattr(last_message, "tool_calls") and last_message.tool_calls:
    return "continue"  # Hay herramientas por ejecutar
else:
    return "end"  # No hay herramientas, el agente terminó
```
</details>

<details>
<summary>💡 Pista 3: Cómo ejecutar herramientas</summary>

```python
from langgraph.prebuilt import ToolNode

# LangGraph proporciona ToolNode que automáticamente:
# 1. Extrae tool_calls del último mensaje
# 2. Ejecuta las herramientas correspondientes
# 3. Retorna ToolMessages con los resultados

tool_node = ToolNode(tools=[calculator, search_knowledge])
```
</details>

<details>
<summary>💡 Pista 4: Estructura del grafo con ciclo</summary>

```python
workflow = StateGraph(AgentState)

# Agregar nodos
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

# Configurar flujo con ciclo
workflow.set_entry_point("agent")

# Conditional edge: decide si continuar o terminar
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "tools",  # Ejecutar herramientas
        "end": END            # Terminar
    }
)

# ¡CICLO! Después de usar herramientas, volver al agente
workflow.add_edge("tools", "agent")
```
</details>

## Desafíos Extra (Opcional)

Una vez completado el ejercicio básico, intenta:

1. **Agregar una tercera herramienta** (ej: convertir divisas)
2. **Limitar el número de iteraciones** para evitar loops infinitos
3. **Agregar logging** para ver cada paso del razonamiento
4. **Mejorar el prompt del sistema** para guiar mejor al agente

## Referencias

- [LangGraph Agents](https://docs.langchain.com/oss/python/langchain/agents.md)
- [Tools in LangChain](https://docs.langchain.com/oss/python/langchain/tools.md)
- [ReAct Pattern](https://docs.langchain.com/oss/python/langgraph/workflows-agents.md)
- [Thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph.md)

## Siguiente Paso

Con estos fundamentos de workflows y agentes, estás listo para el **Módulo 2: Patrones de Workflows Multi-Agente**, donde aprenderás a coordinar múltiples agentes especializados.
