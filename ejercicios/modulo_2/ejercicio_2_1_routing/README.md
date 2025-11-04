# Ejercicio 2.1: Sistema de Routing con Agentes Especializados

## Objetivo

Aprender a construir un **sistema de routing** que:
- Clasifica consultas de usuarios en categorías
- Dirige cada consulta al agente especializado apropiado
- Coordina múltiples agentes especializados en un solo sistema

Este ejercicio introduce el patrón fundamental de **routing** en sistemas multi-agente.

## Contexto

Imagina que trabajas para una empresa que recibe diferentes tipos de consultas de clientes:
- **Consultas técnicas**: Problemas con productos, errores, configuración
- **Consultas de ventas**: Precios, disponibilidad, comparaciones de productos
- **Consultas de soporte**: Devoluciones, garantías, políticas

En lugar de tener un solo agente general que intente manejar todo (y que probablemente no sea bueno en nada), construiremos un **sistema de routing** que:

1. **Clasifica** la consulta del usuario
2. **Dirige** la consulta al agente especializado correcto
3. El **agente especializado** procesa la consulta con su conocimiento específico

```
                        ┌─────────────────┐
    Usuario Query  ──>  │  Clasificador   │
                        └────────┬────────┘
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
            ┌─────────────┐ ┌─────────┐ ┌──────────┐
            │   Agente    │ │ Agente  │ │  Agente  │
            │   Técnico   │ │ Ventas  │ │ Soporte  │
            └─────────────┘ └─────────┘ └──────────┘
                    │            │            │
                    └────────────┼────────────┘
                                 ▼
                           Respuesta Final
```

## ¿Qué es el Pattern Routing?

**Routing** (o enrutamiento) es un patrón arquitectónico donde:
- Un **clasificador** determina la categoría/tipo de la entrada
- La entrada se **dirige** a un handler específico basado en la categoría
- Cada handler es **especializado** en su dominio

### Ventajas del Routing

✅ **Especialización**: Cada agente es experto en su dominio
✅ **Mantenibilidad**: Fácil agregar/modificar agentes especializados
✅ **Prompts focalizados**: Cada agente tiene instrucciones específicas
✅ **Escalabilidad**: Puedes tener docenas de agentes especializados
✅ **Rendimiento**: Cada agente solo procesa lo relevante

### Desventajas del Routing

❌ **Dependencia del clasificador**: Si clasifica mal, falla todo
❌ **No maneja ambigüedad**: Una consulta solo va a un agente
❌ **Overhead**: Requiere una llamada extra al LLM para clasificar
❌ **Casos edge**: ¿Qué pasa si la consulta es multi-dominio?

## Componentes del Sistema de Routing

### 1. Clasificador (Router Node)

El nodo clasificador analiza la consulta y decide la ruta:

```python
def classifier_node(state: State) -> dict:
    """
    Clasifica la consulta del usuario.

    Retorna una categoría: "technical", "sales", o "support"
    """
    query = state["query"]

    # Prompt para clasificación
    prompt = f"""Clasifica la siguiente consulta del cliente en UNA categoría:

    Categorías:
    - technical: Problemas técnicos, errores, configuración
    - sales: Precios, productos, compras
    - support: Devoluciones, garantías, políticas

    Consulta: {query}

    Responde SOLO con la categoría (technical, sales, o support)."""

    category = llm.invoke(prompt).content.strip().lower()
    return {"category": category}
```

### 2. Función de Routing

Decide qué nodo ejecutar basándose en la categoría:

```python
def route_query(state: State) -> str:
    """
    Función de routing que decide el próximo nodo.

    Retorna el nombre del nodo a ejecutar.
    """
    category = state["category"]

    # Mapeo de categoría a nodo
    routing_map = {
        "technical": "technical_agent",
        "sales": "sales_agent",
        "support": "support_agent"
    }

    return routing_map.get(category, "general_agent")
```

### 3. Agentes Especializados

Cada agente tiene un prompt y comportamiento específico:

```python
def technical_agent(state: State) -> dict:
    """Agente especializado en consultas técnicas."""

    system_prompt = """Eres un experto técnico de soporte.
    Tu especialidad es resolver problemas técnicos, errores y configuración.
    Proporciona soluciones paso a paso y técnicas."""

    # Procesar con contexto técnico...
    return {"response": response}

def sales_agent(state: State) -> dict:
    """Agente especializado en consultas de ventas."""

    system_prompt = """Eres un experto en ventas.
    Conoces todos los productos, precios y promociones.
    Ayuda a los clientes a encontrar el producto perfecto."""

    # Procesar con contexto de ventas...
    return {"response": response}
```

## Arquitectura del Grafo

El grafo de routing tiene una estructura especial:

```python
workflow = StateGraph(State)

# Agregar nodos
workflow.add_node("classifier", classifier_node)
workflow.add_node("technical_agent", technical_agent)
workflow.add_node("sales_agent", sales_agent)
workflow.add_node("support_agent", support_agent)

# Punto de entrada: clasificador
workflow.set_entry_point("classifier")

# Conditional edge desde clasificador
workflow.add_conditional_edges(
    "classifier",
    route_query,  # Función que decide la ruta
    {
        "technical_agent": "technical_agent",
        "sales_agent": "sales_agent",
        "support_agent": "support_agent"
    }
)

# Todos los agentes terminan
workflow.add_edge("technical_agent", END)
workflow.add_edge("sales_agent", END)
workflow.add_edge("support_agent", END)
```

## Variaciones del Pattern Routing

### 1. Routing Basado en LLM (Este ejercicio)
El clasificador usa un LLM para categorizar.

**Pros**: Flexible, maneja lenguaje natural
**Contras**: Más lento, más costoso

### 2. Routing Basado en Reglas
Usa keywords o regex para clasificar.

```python
def rule_based_router(query: str) -> str:
    query_lower = query.lower()
    if any(word in query_lower for word in ["error", "bug", "no funciona"]):
        return "technical"
    elif any(word in query_lower for word in ["precio", "comprar", "producto"]):
        return "sales"
    # ...
```

**Pros**: Rápido, determinista, barato
**Contras**: Rígido, difícil de mantener

### 3. Routing por Embeddings
Usa similaridad semántica para clasificar.

```python
# Pre-definir ejemplos de cada categoría
examples = {
    "technical": ["error en la app", "no puedo iniciar sesión"],
    "sales": ["cuánto cuesta", "quiero comprar"],
}

# Comparar query con ejemplos usando embeddings
category = find_most_similar_category(query, examples)
```

**Pros**: Robusto, maneja sinónimos
**Contras**: Requiere setup de embeddings

## Instrucciones

### Paso 1: Entender el Estado

El estado del sistema contiene:
- `query`: Consulta original del usuario
- `category`: Categoría asignada por el clasificador
- `response`: Respuesta del agente especializado

### Paso 2: Implementar el Clasificador

Completa `classifier_node()`:
- Debe analizar la consulta
- Retornar una de tres categorías: "technical", "sales", "support"
- Usa un prompt claro para guiar al LLM

### Paso 3: Implementar Agentes Especializados

Completa tres funciones:
- `technical_agent()`: Maneja consultas técnicas
- `sales_agent()`: Maneja consultas de ventas
- `support_agent()`: Maneja consultas de soporte

Cada uno debe tener un prompt específico a su dominio.

### Paso 4: Implementar Routing

Completa `route_query()`:
- Lee la categoría del estado
- Retorna el nombre del nodo apropiado

### Paso 5: Construir el Grafo

En `build_graph()`:
- Agrega todos los nodos
- Configura el clasificador como entry point
- Agrega conditional edge desde clasificador
- Conecta cada agente a END

### Paso 6: Probar el Sistema

Ejecuta con diferentes tipos de consultas:
```bash
python starter.py
```

## Criterios de Éxito

✅ El clasificador categoriza correctamente diferentes tipos de consultas
✅ Las consultas técnicas van al agente técnico
✅ Las consultas de ventas van al agente de ventas
✅ Las consultas de soporte van al agente de soporte
✅ Cada agente responde con expertise en su dominio
✅ El grafo ejecuta sin errores

## Tiempo Estimado

20-25 minutos

## Conceptos Aprendidos

Al completar este ejercicio, habrás aprendido:
- ✅ Cómo implementar el pattern routing
- ✅ Cómo usar conditional edges con múltiples destinos
- ✅ Cómo crear agentes especializados con prompts focalizados
- ✅ Cómo estructurar sistemas multi-agente escalables
- ✅ Trade-offs entre clasificación por LLM, reglas y embeddings

## Pistas Adicionales

<details>
<summary>💡 Pista 1: Prompt para el Clasificador</summary>

```python
prompt = f"""Analiza la siguiente consulta y clasifícala en UNA categoría.

Categorías:
- technical: Problemas técnicos, errores, bugs, configuración, instalación
- sales: Precios, productos disponibles, comparaciones, quiero comprar
- support: Devoluciones, garantías, políticas, reembolsos, cambios

Consulta del cliente: "{query}"

Responde SOLAMENTE con una palabra: technical, sales, o support."""
```
</details>

<details>
<summary>💡 Pista 2: Estructura del Agente Especializado</summary>

```python
def technical_agent(state: State) -> dict:
    query = state["query"]

    system_prompt = """Eres un experto técnico de soporte de primera línea.

    Tu rol:
    - Diagnosticar problemas técnicos
    - Proporcionar soluciones paso a paso
    - Ser claro y preciso

    Siempre empieza identificando el problema, luego ofrece la solución."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=query)
    ]

    response = llm.invoke(messages)
    return {"response": response.content}
```
</details>

<details>
<summary>💡 Pista 3: Configuración del Grafo con Routing</summary>

```python
workflow = StateGraph(State)

# Agregar todos los nodos
workflow.add_node("classifier", classifier_node)
workflow.add_node("technical_agent", technical_agent)
workflow.add_node("sales_agent", sales_agent)
workflow.add_node("support_agent", support_agent)

# Comenzar con clasificador
workflow.set_entry_point("classifier")

# Routing condicional
workflow.add_conditional_edges(
    "classifier",          # Desde este nodo
    route_query,          # Función que decide
    {                     # Mapeo de retorno → nodo
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
</details>

## Desafíos Extra (Opcional)

1. **Agregar más agentes**: Billing, Account Management, etc.
2. **Mejorar la clasificación**: Usar few-shot examples
3. **Agregar fallback**: ¿Qué pasa si la categoría no existe?
4. **Logging detallado**: Registrar qué agente manejó cada consulta
5. **Métricas**: Rastrear accuracy del clasificador

## Referencias

- [LangGraph Conditional Edges](https://docs.langchain.com/oss/python/langgraph/graph-api.md)
- [Multi-agent Systems](https://docs.langchain.com/oss/python/langchain/multi-agent.md)
- [System Messages](https://docs.langchain.com/oss/python/langchain/messages.md)

## Siguiente Paso

Una vez completado este ejercicio, continúa con el **Ejercicio 2.2: Paralelización con Agregación**, donde aprenderás a ejecutar múltiples agentes simultáneamente y combinar sus resultados.
