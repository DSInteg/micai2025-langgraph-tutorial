# Ejercicio 2.2: Paralelización con Agregación (Map-Reduce)

## Objetivo

Aprender a construir un **sistema paralelo** que:
- Ejecuta múltiples agentes **simultáneamente** sobre el mismo input
- Obtiene **perspectivas diversas** del mismo problema
- **Agrega y sintetiza** los resultados en una respuesta final coherente

Este ejercicio introduce los patrones de **paralelización** y **agregación** en sistemas multi-agente.

## Contexto

Imagina que necesitas analizar el sentimiento de reseñas de productos. En lugar de tener un solo agente que lo haga, puedes:

1. Tener **3 agentes analíticos** que analicen desde diferentes perspectivas:
   - **Agente Optimista**: Se enfoca en aspectos positivos
   - **Agente Pesimista**: Se enfoca en aspectos negativos
   - **Agente Neutral**: Análisis balanceado y objetivo

2. Cada agente analiza la **misma reseña** simultáneamente (en paralelo)

3. Un **agente agregador** sintetiza las tres perspectivas en un análisis final

```
                    ┌────────────────┐
      Input  ──────►│   Broadcast    │
      (review)      └────┬─────┬─────┘
                         │     │
                    ┌────┴─────┴────┐
                    │  PARALELISMO  │
         ┌──────────┼────────┼──────────┐
         ▼          ▼        ▼          ▼
    ┌─────────┐┌─────────┐┌─────────┐
    │Optimist ││Pessimist││ Neutral │
    │ Agent   ││ Agent   ││  Agent  │
    └────┬────┘└────┬────┘└────┬────┘
         │          │          │
         └──────────┼──────────┘
                    ▼
            ┌───────────────┐
            │   Aggregator  │
            │     Agent     │
            └───────┬───────┘
                    ▼
              Final Analysis
```

## ¿Qué es el Pattern de Paralelización?

**Paralelización** (o Map-Reduce en sistemas distribuidos) es un patrón donde:
- Múltiples agentes procesan el **mismo input** simultáneamente
- Cada agente aporta una **perspectiva diferente**
- Los resultados se **agregan** en una respuesta final

### Ventajas de la Paralelización

✅ **Diversidad de perspectivas**: Múltiples ángulos del mismo problema
✅ **Robustez**: Si un agente falla, los demás compensan
✅ **Reducción de sesgo**: Balancea diferentes enfoques
✅ **Paralelismo real**: Puede ejecutar en paralelo (menor latencia)
✅ **Calidad mejorada**: Consenso típicamente es mejor que una sola opinión

### Desventajas de la Paralelización

❌ **Costo**: N agentes = N llamadas al LLM (más caro)
❌ **Complejidad**: Requiere agregación inteligente
❌ **Latencia**: Aunque paralelo, espera al más lento
❌ **Conflictos**: Los agentes pueden contradecirse
❌ **Overhead**: El agregador es una llamada adicional

## Variantes del Pattern

### 1. Sectioning (División por Secciones)

Divide el input en secciones, cada agente procesa una:

```python
# Input: Documento largo
sections = split_document(document)

# Procesar cada sección en paralelo
results = parallel_map(analyze_section, sections)

# Agregar resultados
final_result = aggregate(results)
```

**Ejemplo**: Analizar un contrato legal largo
- Agente 1: Sección de términos generales
- Agente 2: Sección de pagos
- Agente 3: Sección de responsabilidades

### 2. Perspective-Based (Este Ejercicio)

Múltiples agentes analizan el **mismo input** con diferentes perspectivas:

```python
# Input: Reseña de producto
perspectives = ["optimistic", "pessimistic", "neutral"]

# Cada agente analiza con su perspectiva
analyses = parallel_map(analyze_with_perspective, perspectives)

# Sintetizar perspectivas
final_analysis = synthesize(analyses)
```

### 3. Voting/Consensus

Múltiples agentes "votan" y se toma la decisión mayoritaria:

```python
# Input: Clasificar un documento
agents = [classifier_1, classifier_2, classifier_3]

# Cada uno vota
votes = parallel_map(classify, agents)

# Tomar mayoría
final_classification = majority_vote(votes)
```

**Ejemplo**: Moderación de contenido
- 3 agentes revisan si un comentario es apropiado
- Solo se rechaza si 2 o más agentes dicen que no es apropiado

### 4. Ensemble

Combinar múltiples modelos/estrategias y promediar:

```python
# Usar diferentes modelos o estrategias
models = [gpt4, claude, gemini]

# Obtener respuesta de cada uno
responses = parallel_map(ask, models)

# Combinar respuestas
final_response = ensemble_combine(responses)
```

## Componentes del Sistema Paralelo

### 1. Broadcast Node (Opcional)

Prepara el estado para paralelización:

```python
def broadcast_node(state: State) -> dict:
    """
    Prepara el input para los agentes paralelos.
    En este caso solo pasa el input sin cambios.
    """
    return {"ready_for_parallel": True}
```

### 2. Agentes Paralelos

Múltiples nodos que se ejecutan simultáneamente:

```python
def optimistic_agent(state: State) -> dict:
    """Analiza enfocándose en lo positivo."""
    prompt = f"""Analiza esta reseña enfocándote en aspectos POSITIVOS:
    {state['review']}

    Resalta lo bueno, menciona fortalezas."""

    response = llm.invoke(prompt)
    return {"optimistic_analysis": response.content}

def pessimistic_agent(state: State) -> dict:
    """Analiza enfocándose en lo negativo."""
    # Similar pero enfocado en problemas
    ...
```

### 3. Aggregator Node

Sintetiza los resultados paralelos:

```python
def aggregator_node(state: State) -> dict:
    """
    Sintetiza las múltiples perspectivas en un análisis final.
    """
    prompt = f"""Sintetiza estos tres análisis en uno balanceado:

    Perspectiva Optimista: {state['optimistic_analysis']}
    Perspectiva Pesimista: {state['pessimistic_analysis']}
    Perspectiva Neutral: {state['neutral_analysis']}

    Proporciona un análisis equilibrado que considere todos los puntos."""

    response = llm.invoke(prompt)
    return {"final_analysis": response.content}
```

## Arquitectura del Grafo Paralelo

La clave es usar **múltiples edges** desde un nodo:

```python
workflow = StateGraph(State)

# Agregar nodos
workflow.add_node("broadcast", broadcast_node)
workflow.add_node("optimistic", optimistic_agent)
workflow.add_node("pessimistic", pessimistic_agent)
workflow.add_node("neutral", neutral_agent)
workflow.add_node("aggregator", aggregator_node)

# Entry point
workflow.set_entry_point("broadcast")

# PARALELISMO: Múltiples edges desde broadcast
workflow.add_edge("broadcast", "optimistic")
workflow.add_edge("broadcast", "pessimistic")
workflow.add_edge("broadcast", "neutral")

# AGREGACIÓN: Todos convergen en aggregator
workflow.add_edge("optimistic", "aggregator")
workflow.add_edge("pessimistic", "aggregator")
workflow.add_edge("neutral", "aggregator")

# Fin
workflow.add_edge("aggregator", END)
```

**Importante**: LangGraph automáticamente espera a que todos los nodos paralelos terminen antes de ejecutar el aggregator.

## Instrucciones

### Paso 1: Entender el Estado

El estado contiene:
- `review`: Reseña original a analizar
- `optimistic_analysis`: Análisis del agente optimista
- `pessimistic_analysis`: Análisis del agente pesimista
- `neutral_analysis`: Análisis del agente neutral
- `final_analysis`: Síntesis final

### Paso 2: Implementar Agentes con Perspectivas

Completa tres funciones:
- `optimistic_agent()`: Enfoque en lo positivo
- `pessimistic_agent()`: Enfoque en lo negativo
- `neutral_agent()`: Análisis balanceado

Cada uno debe analizar la misma reseña con su perspectiva única.

### Paso 3: Implementar el Aggregator

Completa `aggregator_node()`:
- Debe recibir los tres análisis
- Sintetizarlos en un análisis final balanceado
- Identificar consenso y discrepancias

### Paso 4: Construir el Grafo Paralelo

En `build_graph()`:
- Agregar todos los nodos
- Crear paralelismo con múltiples edges
- Configurar agregación
- Conectar a END

### Paso 5: Probar con Reseñas Variadas

Ejecuta con reseñas:
- Muy positivas
- Muy negativas
- Mixtas (lo más interesante)

```bash
python starter.py
```

## Criterios de Éxito

✅ Los tres agentes se ejecutan en paralelo
✅ El agente optimista enfatiza aspectos positivos
✅ El agente pesimista enfatiza aspectos negativos
✅ El agente neutral es balanceado
✅ El aggregator sintetiza coherentemente las tres perspectivas
✅ El análisis final es más completo que cualquier perspectiva individual

## Tiempo Estimado

20-25 minutos

## Conceptos Aprendidos

Al completar este ejercicio, habrás aprendido:
- ✅ Cómo implementar paralelización en LangGraph
- ✅ Cómo crear agentes con perspectivas específicas
- ✅ Cómo agregar resultados de múltiples agentes
- ✅ Trade-offs entre costo y calidad
- ✅ Cuándo usar paralelización vs routing

## Pistas Adicionales

<details>
<summary>💡 Pista 1: Prompt para Agente con Perspectiva</summary>

```python
def optimistic_agent(state: State) -> dict:
    review = state["review"]

    prompt = f"""Analiza la siguiente reseña de producto enfocándote en aspectos POSITIVOS.

Tu perspectiva:
- Resalta lo que el cliente apreció
- Enfócate en fortalezas del producto
- Menciona aspectos positivos, incluso si son sutiles
- Sé realista pero optimista

Reseña: {review}

Análisis optimista:"""

    response = llm.invoke(prompt)
    return {"optimistic_analysis": response.content}
```
</details>

<details>
<summary>💡 Pista 2: Aggregator que Sintetiza</summary>

```python
def aggregator_node(state: State) -> dict:
    prompt = f"""Sintetiza estos tres análisis en uno balanceado y completo.

Análisis Optimista:
{state['optimistic_analysis']}

Análisis Pesimista:
{state['pessimistic_analysis']}

Análisis Neutral:
{state['neutral_analysis']}

Tarea:
1. Identifica puntos de consenso entre las tres perspectivas
2. Nota discrepancias importantes
3. Proporciona un análisis final equilibrado
4. Incluye una puntuación de satisfacción del 1-5

Análisis Final:"""
```
</details>

<details>
<summary>💡 Pista 3: Configurar Paralelismo</summary>

```python
# Para ejecutar nodos en paralelo, simplemente agregar
# múltiples edges desde el mismo nodo origen

workflow.add_edge("start_node", "parallel_node_1")
workflow.add_edge("start_node", "parallel_node_2")
workflow.add_edge("start_node", "parallel_node_3")

# LangGraph automáticamente:
# 1. Ejecuta parallel_node_1, 2, y 3 simultáneamente
# 2. Espera a que TODOS terminen
# 3. Actualiza el estado con todos los resultados
# 4. Continúa al siguiente nodo
```
</details>

## Desafíos Extra (Opcional)

1. **Agregar más perspectivas**: Cliente, Empresa, Experto técnico
2. **Implementar voting**: Los agentes votan rating (1-5) y calcular promedio
3. **Pesos en agregación**: Dar más peso a ciertas perspectivas
4. **Detección de conflictos**: Identificar cuándo las perspectivas difieren mucho
5. **Confidence scores**: Cada agente indica su confianza

## Referencias

- [LangGraph Parallelism](https://docs.langchain.com/oss/python/langgraph/graph-api.md)
- [Map-Reduce Pattern](https://docs.langchain.com/oss/python/langchain/retrieval.md)
- [Ensemble Methods in ML](https://en.wikipedia.org/wiki/Ensemble_learning)

## Siguiente Paso

Una vez completado este ejercicio, continúa con el **Ejercicio 2.3: Orchestrator-Workers**, donde aprenderás a coordinar agentes especializados que trabajan en diferentes sub-tareas de un problema complejo.
