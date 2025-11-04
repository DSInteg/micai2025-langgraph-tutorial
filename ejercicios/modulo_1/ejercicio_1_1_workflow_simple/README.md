# Ejercicio 1.1: Workflow Simple con Prompt Chaining

## Objetivo

Aprender a construir un **workflow determinístico** usando LangGraph para procesar texto a través de múltiples etapas secuenciales. Este ejercicio introduce los conceptos fundamentales de:
- Definición de estado (State)
- Creación de nodos (Nodes)
- Construcción de grafos (Graph)
- Edges (conexiones) entre nodos

## Contexto

Imagina que trabajas para una empresa que necesita procesar artículos de blog en español. El pipeline debe:
1. **Extraer** las ideas principales del artículo
2. **Resumir** el contenido en 3 párrafos
3. **Traducir** el resumen al inglés

Este es un **workflow determinístico**: siempre sigue el mismo camino (extracto → resumen → traducción), sin tomar decisiones basadas en el contenido.

## ¿Qué es un Workflow?

Un **workflow** es una secuencia predefinida de pasos que se ejecutan en orden. A diferencia de un **agente**, que toma decisiones autónomas sobre qué hacer a continuación, un workflow siempre sigue la misma ruta.

**Características de un Workflow:**
- ✅ Flujo predecible y determinístico
- ✅ Fácil de debuggear y entender
- ✅ Ideal cuando conoces exactamente los pasos necesarios
- ✅ Menor costo computacional que agentes autónomos

**Cuándo usar Workflows:**
- Procesamiento de datos en etapas conocidas
- Pipelines de transformación de contenido
- Validación y verificación multi-paso
- Tareas con pasos bien definidos

## Conceptos Clave de LangGraph

### 1. Estado (State)
El estado es un diccionario que se pasa entre nodos y contiene toda la información necesaria. En Python usamos `TypedDict` para definir la estructura:

```python
from typing import TypedDict

class WorkflowState(TypedDict):
    """
    Estado que fluye a través del workflow.
    Cada nodo puede leer y actualizar estos campos.
    """
    article: str          # Artículo original
    key_points: str       # Puntos clave extraídos
    summary: str          # Resumen del artículo
    translation: str      # Traducción al inglés
```

### 2. Nodos (Nodes)
Los nodos son funciones que reciben el estado, realizan alguna operación, y retornan un estado actualizado:

```python
def my_node(state: WorkflowState) -> WorkflowState:
    """
    Un nodo es simplemente una función que:
    1. Recibe el estado actual
    2. Realiza alguna operación (llamar LLM, procesar datos, etc.)
    3. Retorna el estado actualizado
    """
    # Tu lógica aquí
    return {"field_to_update": new_value}
```

**Importante:** Solo necesitas retornar los campos que quieres actualizar, no todo el estado.

### 3. Grafo (Graph)
El grafo conecta nodos en un flujo de ejecución. En LangGraph usamos `StateGraph`:

```python
from langgraph.graph import StateGraph, END

# Crear el grafo con el tipo de estado
workflow = StateGraph(WorkflowState)

# Agregar nodos
workflow.add_node("extract", extract_key_points)
workflow.add_node("summarize", summarize_content)
workflow.add_node("translate", translate_summary)

# Definir el flujo con edges
workflow.set_entry_point("extract")       # Primer nodo
workflow.add_edge("extract", "summarize") # extract → summarize
workflow.add_edge("summarize", "translate") # summarize → translate
workflow.add_edge("translate", END)        # translate → fin

# Compilar el grafo
app = workflow.compile()
```

### 4. Edges (Conexiones)
Los edges definen cómo fluye la ejecución entre nodos:
- **`set_entry_point(node)`**: Define el primer nodo a ejecutar
- **`add_edge(from, to)`**: Conecta dos nodos
- **`END`**: Marca el final del workflow

## Instrucciones

### Paso 1: Revisar el código inicial
Abre el archivo `starter.py` y familiarízate con:
- La definición del estado `WorkflowState`
- Las tres funciones (nodos) con TODOs
- La estructura del grafo

### Paso 2: Implementar los nodos
Completa las tres funciones:

1. **`extract_key_points`**: Usa el LLM para extraer 3-5 ideas principales
2. **`summarize_content`**: Crea un resumen de 3 párrafos basado en los puntos clave
3. **`translate_summary`**: Traduce el resumen al inglés

**Pistas:**
- Usa prompts claros y específicos
- El objeto `llm` ya está configurado (GPT-4o-mini)
- Cada nodo solo necesita retornar los campos que actualiza

### Paso 3: Construir el grafo
En la función `build_graph()`:
1. Agrega los tres nodos al workflow
2. Define el punto de entrada
3. Conecta los nodos en el orden correcto
4. Termina el flujo con `END`

### Paso 4: Probar el workflow
Ejecuta el archivo:
```bash
python starter.py
```

Deberías ver la ejecución paso a paso del workflow.

## Criterios de Éxito

✅ El workflow ejecuta sin errores
✅ Se extraen puntos clave coherentes del artículo
✅ El resumen contiene aproximadamente 3 párrafos
✅ La traducción al inglés es correcta
✅ El flujo sigue el orden: extract → summarize → translate
✅ El estado se actualiza correctamente en cada paso

## Tiempo Estimado

20 minutos

## Conceptos Aprendidos

Al completar este ejercicio, habrás aprendido:
- ✅ Cómo definir un estado en LangGraph usando `TypedDict`
- ✅ Cómo crear nodos (funciones) que procesan el estado
- ✅ Cómo construir un grafo con `StateGraph`
- ✅ Cómo conectar nodos con edges
- ✅ La diferencia entre workflows determinísticos y agentes autónomos

## Pistas Adicionales

<details>
<summary>💡 Pista 1: Estructura de un prompt efectivo</summary>

Para extraer puntos clave:
```python
prompt = f"""Analiza el siguiente artículo y extrae las 3-5 ideas principales.

Artículo:
{state["article"]}

Responde con una lista clara de puntos clave."""
```
</details>

<details>
<summary>💡 Pista 2: Cómo invocar el LLM</summary>

```python
from langchain_core.messages import HumanMessage

# Crear el mensaje
message = HumanMessage(content=prompt)

# Invocar el LLM
response = llm.invoke([message])

# Obtener el contenido
result = response.content
```
</details>

<details>
<summary>💡 Pista 3: Estructura del grafo</summary>

```python
workflow = StateGraph(WorkflowState)

# Agregar nodos
workflow.add_node("nombre_nodo_1", funcion_nodo_1)
workflow.add_node("nombre_nodo_2", funcion_nodo_2)

# Definir flujo
workflow.set_entry_point("nombre_nodo_1")
workflow.add_edge("nombre_nodo_1", "nombre_nodo_2")
workflow.add_edge("nombre_nodo_2", END)

# Compilar
return workflow.compile()
```
</details>

## Referencias

- [LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview.md)
- [LangGraph Quickstart](https://docs.langchain.com/oss/python/langgraph/quickstart.md)
- [Workflows and Agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents.md)

## Siguiente Paso

Una vez completado este ejercicio, continúa con el **Ejercicio 1.2: Agente Básico Autónomo**, donde aprenderás cómo agregar capacidad de decisión a tu sistema.
