# Ejercicio 2.3: Orchestrator-Workers Pattern

## Objetivo

Aprender a construir un **sistema orchestrator-workers** que:
- Divide un problema complejo en sub-tareas específicas
- Asigna cada sub-tarea a un worker especializado
- Coordina la ejecución mediante un orchestrator central
- Ensambla los resultados parciales en una solución completa

Este ejercicio introduce el patrón **orchestrator-workers**, uno de los más poderosos en sistemas multi-agente.

## Contexto

Imagina que necesitas analizar un documento largo (como un contrato legal o un reporte técnico). En lugar de procesarlo todo de una vez, puedes:

1. **Orchestrator**: Divide el documento en secciones lógicas
2. **Workers especializados**: Cada uno analiza su sección asignada
   - Worker 1: Analiza resumen ejecutivo
   - Worker 2: Analiza detalles técnicos
   - Worker 3: Analiza implicaciones financieras
3. **Orchestrator**: Ensambla los análisis parciales en un reporte completo

```
                    ┌─────────────────┐
    Documento  ──>  │  Orchestrator   │
                    │   (Divide)      │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
    Sub-tarea 1         Sub-tarea 2         Sub-tarea 3
         │                   │                   │
         ▼                   ▼                   ▼
    ┌─────────┐         ┌─────────┐         ┌─────────┐
    │Worker 1 │         │Worker 2 │         │Worker 3 │
    │Executive│         │Technical│         │Financial│
    └────┬────┘         └────┬────┘         └────┬────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             ▼
                    ┌─────────────────┐
                    │  Orchestrator   │
                    │   (Ensambla)    │
                    └────────┬────────┘
                             ▼
                      Reporte Final
```

## ¿Qué es el Pattern Orchestrator-Workers?

**Orchestrator-Workers** es un patrón arquitectónico donde:
- Un **orchestrator** central coordina todo el proceso
- **Workers** especializados ejecutan sub-tareas específicas
- El orchestrator **divide** el problema y **ensambla** los resultados

### Diferencia con otros patrones

| Pattern | División de trabajo | Coordinación | Uso típico |
|---------|-------------------|--------------|------------|
| **Routing** | Una ruta por consulta | Clasificador | Atención al cliente |
| **Paralelización** | Mismo input a todos | Ninguna → Aggregator | Análisis multi-perspectiva |
| **Orchestrator-Workers** | Sub-tareas diferentes | Orchestrator central | Problemas complejos divisibles |

### Ventajas del Pattern

✅ **Divide y conquista**: Problemas grandes → sub-problemas manejables
✅ **Especialización**: Cada worker es experto en su sub-tarea
✅ **Escalabilidad**: Fácil agregar más workers
✅ **Claridad**: El orchestrator hace el proceso explícito
✅ **Flexibilidad**: Fácil modificar la estrategia de división

### Desventajas

❌ **Complejidad**: Requiere lógica de división y ensamblaje
❌ **Dependencias**: Si un worker falla, puede afectar todo
❌ **Overhead**: El orchestrator agrega latencia
❌ **Coordinación**: Requiere buena estrategia de división

## Componentes del Sistema

### 1. Orchestrator (Coordinador)

El orchestrator tiene dos responsabilidades principales:

**A. División (Planning)**
```python
def orchestrator_plan(state: State) -> dict:
    """
    Analiza el documento y decide cómo dividirlo.

    Retorna:
    - plan: Lista de sub-tareas
    - assignments: Qué worker maneja cada sub-tarea
    """
    document = state["document"]

    # El orchestrator analiza el documento
    prompt = f"""Analiza este documento y divídelo en secciones lógicas.

    Documento:
    {document}

    Identifica las secciones principales (ejecutivo, técnico, financiero, etc.)
    y describe qué debe analizarse en cada una."""

    # El LLM genera un plan de división
    plan = llm.invoke(prompt)

    return {
        "plan": plan.content,
        "sections": extract_sections(document)
    }
```

**B. Ensamblaje (Synthesis)**
```python
def orchestrator_synthesize(state: State) -> dict:
    """
    Ensambla los análisis parciales en un reporte final.
    """
    analyses = [
        state["executive_analysis"],
        state["technical_analysis"],
        state["financial_analysis"]
    ]

    prompt = f"""Ensambla estos análisis parciales en un reporte coherente:

    {analyses}

    Crea un reporte ejecutivo completo."""

    final_report = llm.invoke(prompt)
    return {"final_report": final_report.content}
```

### 2. Workers Especializados

Cada worker es experto en un tipo de análisis:

```python
def executive_summary_worker(state: State) -> dict:
    """
    Worker especializado en resúmenes ejecutivos.
    """
    section = state["executive_section"]

    prompt = f"""Como experto en análisis ejecutivo, analiza esta sección:

    {section}

    Proporciona:
    - Puntos clave
    - Decisiones importantes
    - Recomendaciones de alto nivel"""

    analysis = llm.invoke(prompt)
    return {"executive_analysis": analysis.content}


def technical_details_worker(state: State) -> dict:
    """
    Worker especializado en detalles técnicos.
    """
    section = state["technical_section"]

    prompt = f"""Como experto técnico, analiza esta sección:

    {section}

    Proporciona:
    - Especificaciones técnicas
    - Requisitos y dependencias
    - Consideraciones de implementación"""

    analysis = llm.invoke(prompt)
    return {"technical_analysis": analysis.content}
```

### 3. Función de Routing del Orchestrator

Decide qué workers ejecutar:

```python
def route_to_workers(state: State) -> list[str]:
    """
    Determina qué workers deben ejecutarse basándose en el plan.

    Retorna lista de nombres de workers a ejecutar.
    """
    plan = state["plan"]

    # El orchestrator decide qué workers necesita
    # Basándose en las secciones identificadas
    workers_needed = []

    if "executive" in plan.lower():
        workers_needed.append("executive_worker")
    if "technical" in plan.lower():
        workers_needed.append("technical_worker")
    if "financial" in plan.lower():
        workers_needed.append("financial_worker")

    return workers_needed
```

## Arquitectura del Grafo

El grafo tiene una estructura de "diamante":

```python
workflow = StateGraph(State)

# Orchestrator (inicio)
workflow.add_node("orchestrator_plan", orchestrator_plan)

# Workers especializados
workflow.add_node("executive_worker", executive_summary_worker)
workflow.add_node("technical_worker", technical_details_worker)
workflow.add_node("financial_worker", financial_analysis_worker)

# Orchestrator (final)
workflow.add_node("orchestrator_synthesize", orchestrator_synthesize)

# Flujo
workflow.set_entry_point("orchestrator_plan")

# Del orchestrator a los workers (puede ser paralelo)
workflow.add_edge("orchestrator_plan", "executive_worker")
workflow.add_edge("orchestrator_plan", "technical_worker")
workflow.add_edge("orchestrator_plan", "financial_worker")

# De los workers al orchestrator final
workflow.add_edge("executive_worker", "orchestrator_synthesize")
workflow.add_edge("technical_worker", "orchestrator_synthesize")
workflow.add_edge("financial_worker", "orchestrator_synthesize")

workflow.add_edge("orchestrator_synthesize", END)
```

## Variantes del Pattern

### 1. Orchestrator Secuencial
Workers se ejecutan uno después del otro (no paralelo).

**Ventaja**: Cada worker puede usar resultados del anterior
**Desventaja**: Más lento

### 2. Orchestrator Paralelo (Este Ejercicio)
Workers se ejecutan simultáneamente.

**Ventaja**: Más rápido
**Desventaja**: Workers no pueden compartir información

### 3. Orchestrator Jerárquico
Múltiples niveles de orchestrators y workers.

```
Master Orchestrator
    ├── Sub-Orchestrator 1
    │   ├── Worker 1.1
    │   └── Worker 1.2
    └── Sub-Orchestrator 2
        ├── Worker 2.1
        └── Worker 2.2
```

### 4. Orchestrator Adaptativo
El orchestrator ajusta el plan basándose en resultados intermedios.

## Instrucciones

### Paso 1: Implementar Orchestrator de Planificación

Completa `orchestrator_plan()`:
- Analiza el documento de entrada
- Identifica las secciones principales
- Extrae cada sección para los workers

### Paso 2: Implementar Workers Especializados

Completa tres workers:
- `executive_summary_worker()`: Análisis ejecutivo
- `technical_details_worker()`: Análisis técnico
- `financial_analysis_worker()`: Análisis financiero

### Paso 3: Implementar Orchestrator de Síntesis

Completa `orchestrator_synthesize()`:
- Recibe los tres análisis parciales
- Ensambla en un reporte coherente
- Asegura que nada importante se pierda

### Paso 4: Construir el Grafo

En `build_graph()`:
- Agregar orchestrator de planificación
- Agregar los tres workers
- Agregar orchestrator de síntesis
- Configurar el flujo de trabajo

### Paso 5: Probar con Documentos

Ejecuta con diferentes tipos de documentos.

```bash
python starter.py
```

## Criterios de Éxito

✅ El orchestrator identifica correctamente las secciones del documento
✅ Cada worker analiza su sección con expertise apropiado
✅ El orchestrator ensambla un reporte coherente
✅ El reporte final es completo (no pierde información)
✅ El sistema maneja documentos de diferentes estructuras

## Tiempo Estimado

25-30 minutos

## Conceptos Aprendidos

Al completar este ejercicio, habrás aprendido:
- ✅ Cómo implementar el pattern orchestrator-workers
- ✅ Cómo dividir problemas complejos en sub-tareas
- ✅ Cómo coordinar múltiples workers especializados
- ✅ Cómo ensamblar resultados parciales coherentemente
- ✅ Trade-offs entre diferentes estrategias de coordinación

## Pistas Adicionales

<details>
<summary>💡 Pista 1: Orchestrator de Planificación</summary>

```python
def orchestrator_plan(state: State) -> dict:
    document = state["document"]

    # Analizar estructura del documento
    prompt = f"""Analiza este documento de negocio e identifica sus secciones principales.

    Documento:
    {document}

    Identifica si hay:
    - Resumen ejecutivo / Overview
    - Detalles técnicos / Especificaciones
    - Información financiera / Costos

    Para cada sección encontrada, extrae el texto relevante."""

    # Extraer secciones (simplificado)
    sections = {
        "executive": extract_executive_section(document),
        "technical": extract_technical_section(document),
        "financial": extract_financial_section(document)
    }

    return sections
```
</details>

<details>
<summary>💡 Pista 2: Worker Especializado</summary>

```python
def technical_details_worker(state: State) -> dict:
    section = state.get("technical", "")

    if not section:
        return {"technical_analysis": "No technical section found."}

    prompt = f"""Como experto técnico, analiza esta sección:

    {section}

    Proporciona:
    1. Especificaciones técnicas clave
    2. Requisitos y dependencias
    3. Consideraciones de implementación
    4. Riesgos técnicos potenciales"""

    response = llm.invoke(prompt)
    return {"technical_analysis": response.content}
```
</details>

<details>
<summary>💡 Pista 3: Orchestrator de Síntesis</summary>

```python
def orchestrator_synthesize(state: State) -> dict:
    exec_analysis = state.get("executive_analysis", "")
    tech_analysis = state.get("technical_analysis", "")
    fin_analysis = state.get("financial_analysis", "")

    prompt = f"""Ensambla estos análisis especializados en un reporte ejecutivo coherente.

    ANÁLISIS EJECUTIVO:
    {exec_analysis}

    ANÁLISIS TÉCNICO:
    {tech_analysis}

    ANÁLISIS FINANCIERO:
    {fin_analysis}

    Crea un reporte final que:
    1. Integre todas las perspectivas
    2. Sea coherente y fluido
    3. Destaque puntos clave de cada área
    4. Proporcione recomendaciones integradas"""

    response = llm.invoke(prompt)
    return {"final_report": response.content}
```
</details>

## Desafíos Extra (Opcional)

1. **Orchestrator adaptativo**: Que decida dinámicamente qué workers ejecutar
2. **Workers condicionales**: Solo ejecutar si la sección existe
3. **Priorización**: Dar más peso a ciertos análisis
4. **Validación**: Orchestrator valida calidad de análisis de workers
5. **Iteración**: Si un análisis es incompleto, re-ejecutar el worker

## Referencias

- [Orchestrator Pattern](https://docs.langchain.com/oss/python/langchain/multi-agent.md)
- [Divide and Conquer](https://en.wikipedia.org/wiki/Divide-and-conquer_algorithm)
- [Microservices Orchestration](https://microservices.io/patterns/data/saga.html)

## Siguiente Paso

¡Felicidades! Has completado el **Módulo 2: Patrones de Workflows Multi-Agente**.

Has aprendido tres patrones fundamentales:
1. **Routing**: Dirigir consultas a agentes especializados
2. **Paralelización**: Obtener múltiples perspectivas simultáneas
3. **Orchestrator-Workers**: Dividir problemas complejos en sub-tareas

Continúa con el **Módulo 3: Redes de Agentes Autónomos** para aprender patrones avanzados con agentes que toman decisiones dinámicas.
