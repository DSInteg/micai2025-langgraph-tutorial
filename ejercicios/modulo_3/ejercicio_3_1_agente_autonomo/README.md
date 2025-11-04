# Ejercicio 3.1: Agente Autónomo con Planificación Dinámica

## Objetivo

Aprender a construir un **agente autónomo con planificación** que:
- Crea un plan de acción basándose en el objetivo
- Ejecuta el plan paso a paso
- Evalúa si necesita replantear o continuar
- Se adapta dinámicamente según los resultados

Este ejercicio introduce el patrón **Plan-Execute-Evaluate**, fundamental en agentes autónomos avanzados.

## Contexto

En el Módulo 1 creamos un agente ReAct simple que usa herramientas. Ahora vamos más allá:

**Agente ReAct Simple (Módulo 1)**:
```
Usuario: "Calcula X + busca Y"
→ Agente decide: Usar calculadora
→ Agente decide: Usar búsqueda
→ Agente responde
```

**Agente con Planificación (Este ejercicio)**:
```
Usuario: "Investiga sobre IA y crea un reporte"

→ Agente PLANIFICA:
   Plan:
   1. Buscar información sobre IA
   2. Buscar aplicaciones actuales
   3. Sintetizar hallazgos
   4. Crear reporte estructurado

→ Agente EJECUTA paso 1
→ Agente EVALÚA: ¿Completado? → Continuar
→ Agente EJECUTA paso 2
→ Agente EVALÚA: ¿Suficiente info? → Continuar
→ Agente EJECUTA paso 3
→ Agente EVALÚA: ¿Listo para reporte? → Sí
→ Agente EJECUTA paso 4
→ Agente EVALÚA: ¿Completado? → Terminar
```

## ¿Qué es el Pattern Plan-Execute-Evaluate?

El pattern **Plan-Execute-Evaluate** (también llamado Plan-and-Solve) es un ciclo donde:

1. **PLAN**: El agente crea un plan de acción
2. **EXECUTE**: Ejecuta un paso del plan
3. **EVALUATE**: Evalúa si debe continuar, replantear, o terminar

```
     ┌─────────────┐
     │    START    │
     └──────┬──────┘
            │
            ▼
     ┌─────────────┐
     │    PLAN     │◄────────┐
     │ Crear plan  │         │
     └──────┬──────┘         │
            │                │
            ▼                │
     ┌─────────────┐         │
     │   EXECUTE   │         │
     │ Ejecutar 1  │         │
     │    paso     │         │
     └──────┬──────┘         │
            │                │
            ▼                │
     ┌─────────────┐         │
     │  EVALUATE   │         │
     │ ¿Qué hacer? │         │
     └──────┬──────┘         │
            │                │
     ┌──────┼──────┐         │
     ▼      ▼      ▼         │
   [OK]  [Re-    [Más]       │
          plan]              │
     │      │      │         │
     │      └──────┘─────────┘
     │             (ciclo)
     ▼
   [END]
```

### Ventajas sobre ReAct Simple

| Aspecto | ReAct Simple | Plan-Execute-Evaluate |
|---------|--------------|---------------------|
| **Planificación** | Implícita | Explícita |
| **Visibilidad** | Baja | Alta |
| **Adaptabilidad** | Reactiva | Proactiva |
| **Debugging** | Difícil | Fácil (ver plan) |
| **Eficiencia** | Variable | Optimizada |
| **Complejidad** | Baja | Media-Alta |

### ¿Cuándo usar cada uno?

**ReAct Simple**: Tareas simples, 1-3 pasos
**Plan-Execute-Evaluate**: Tareas complejas, multi-paso, requiere coordinación

## Componentes del Sistema

### 1. Nodo de Planificación

Crea un plan estructurado:

```python
def planner_node(state: State) -> dict:
    """
    Crea un plan de acción para alcanzar el objetivo.
    """
    objective = state["objective"]

    prompt = f"""Eres un agente planificador experto.

Objetivo: {objective}

Crea un plan detallado paso a paso para alcanzar este objetivo.

El plan debe:
- Tener pasos específicos y accionables
- Estar en orden lógico
- Indicar qué herramientas usar en cada paso

Plan (formato numerado):"""

    plan = llm.invoke(prompt)

    return {
        "plan": plan.content,
        "current_step": 0
    }
```

### 2. Nodo de Ejecución

Ejecuta un paso del plan:

```python
def executor_node(state: State) -> dict:
    """
    Ejecuta el paso actual del plan.
    """
    plan = state["plan"]
    current_step = state["current_step"]
    observations = state.get("observations", [])

    # Extraer el paso actual del plan
    steps = extract_steps(plan)
    step_to_execute = steps[current_step]

    prompt = f"""Ejecuta este paso del plan:

Paso: {step_to_execute}

Contexto previo:
{observations}

Herramientas disponibles: search, calculate

Ejecuta el paso y proporciona el resultado."""

    # Aquí el agente usaría herramientas (similar a ReAct)
    result = execute_with_tools(prompt, tools)

    observations.append({
        "step": current_step,
        "action": step_to_execute,
        "result": result
    })

    return {
        "observations": observations,
        "current_step": current_step + 1
    }
```

### 3. Nodo de Evaluación

Decide el siguiente paso:

```python
def evaluator_node(state: State) -> dict:
    """
    Evalúa el progreso y decide qué hacer.
    """
    objective = state["objective"]
    plan = state["plan"]
    observations = state["observations"]
    current_step = state["current_step"]

    prompt = f"""Evalúa el progreso del agente:

Objetivo original: {objective}

Plan: {plan}

Observaciones hasta ahora:
{observations}

Paso actual: {current_step}

Evalúa:
1. ¿Se ha completado el objetivo? (sí/no)
2. ¿El plan sigue siendo válido? (sí/no/necesita_ajuste)
3. ¿Qué acción tomar?

Opciones:
- CONTINUE: Continuar con el plan
- REPLAN: Crear nuevo plan
- FINISH: Objetivo completado

Decisión (CONTINUE/REPLAN/FINISH):"""

    decision = llm.invoke(prompt).content.strip().upper()

    return {"decision": decision}
```

### 4. Función de Routing

Decide el flujo basándose en la evaluación:

```python
def route_decision(state: State) -> str:
    """Routing basado en la decisión del evaluator."""
    decision = state["decision"]

    routing_map = {
        "CONTINUE": "executor",
        "REPLAN": "planner",
        "FINISH": "finish"
    }

    return routing_map.get(decision, "finish")
```

## Arquitectura del Grafo

```python
workflow = StateGraph(State)

# Nodos
workflow.add_node("planner", planner_node)
workflow.add_node("executor", executor_node)
workflow.add_node("evaluator", evaluator_node)
workflow.add_node("finish", finish_node)

# Entry point
workflow.set_entry_point("planner")

# Flujo con ciclos
workflow.add_edge("planner", "executor")
workflow.add_edge("executor", "evaluator")

# Routing condicional desde evaluator
workflow.add_conditional_edges(
    "evaluator",
    route_decision,
    {
        "executor": "executor",    # Continuar
        "planner": "planner",      # Replantear
        "finish": "finish"         # Terminar
    }
)

workflow.add_edge("finish", END)
```

## Variantes del Pattern

### 1. Plan-Execute Simple
Plan fijo, solo ejecuta.

**Ventaja**: Más simple
**Desventaja**: No se adapta

### 2. Plan-Execute-Evaluate (Este ejercicio)
Plan adaptable, evalúa en cada paso.

**Ventaja**: Adaptable
**Desventaja**: Más llamadas LLM

### 3. Hierarchical Planning
Plan con sub-planes anidados.

```
Plan Principal
  ├─ Sub-plan 1
  │   ├─ Paso 1.1
  │   └─ Paso 1.2
  └─ Sub-plan 2
      ├─ Paso 2.1
      └─ Paso 2.2
```

### 4. Continuous Planning
Replanifica constantemente (muy adaptativo pero costoso).

## Instrucciones

### Paso 1: Implementar el Planner

Completa `planner_node()`:
- Analizar el objetivo
- Crear un plan detallado
- Retornar plan y estado inicial

### Paso 2: Implementar el Executor

Completa `executor_node()`:
- Leer el paso actual del plan
- Ejecutar usando herramientas disponibles
- Registrar observaciones

### Paso 3: Implementar el Evaluator

Completa `evaluator_node()`:
- Evaluar progreso
- Decidir: CONTINUE, REPLAN, o FINISH

### Paso 4: Implementar Routing

Completa `route_decision()`:
- Mapear decisión a siguiente nodo

### Paso 5: Construir el Grafo

En `build_graph()`:
- Agregar todos los nodos
- Configurar ciclos correctamente
- Establecer conditional edges

### Paso 6: Probar con Objetivos Complejos

```bash
python starter.py
```

## Criterios de Éxito

✅ El agente crea un plan coherente
✅ Ejecuta pasos del plan usando herramientas
✅ Evalúa progreso después de cada paso
✅ Se adapta (replanifica) cuando es necesario
✅ Termina cuando completa el objetivo
✅ No entra en loops infinitos

## Tiempo Estimado

30-35 minutos

## Conceptos Aprendidos

Al completar este ejercicio, habrás aprendido:
- ✅ Pattern Plan-Execute-Evaluate
- ✅ Planificación explícita vs implícita
- ✅ Evaluación de progreso
- ✅ Adaptación dinámica de planes
- ✅ Ciclos complejos en LangGraph
- ✅ Control de flujo avanzado

## Desafíos Extra (Opcional)

1. **Límite de iteraciones**: Prevenir loops infinitos
2. **Plan jerárquico**: Sub-planes anidados
3. **Confidence scores**: El agente indica confianza
4. **Human-in-the-loop**: Aprobar plan antes de ejecutar
5. **Logging detallado**: Registrar todo el proceso

## Referencias

- [Plan-and-Solve Pattern](https://docs.langchain.com/oss/python/langchain/agents.md)
- [Hierarchical Planning](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph.md)
- [Agent Loops](https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT.md)

## Siguiente Paso

Una vez completado, continúa con el **Ejercicio 3.2: Red Colaborativa con Handoffs**, donde múltiples agentes especializados se pasan el control dinámicamente.
