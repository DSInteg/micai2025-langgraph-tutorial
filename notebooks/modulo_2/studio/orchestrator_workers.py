"""
Sistema Orchestrator-Workers
=============================

Ejercicio 2.3: Demuestra el patrón Orchestrator-Workers con re-planificación.

Conceptos:
- Orchestrator: "Cerebro" que planifica y decide
- Workers: "Manos" que ejecutan tareas específicas
- Routing dinámico basado en decisiones del orchestrator
- Loops: Re-planificación hasta completar la tarea
- Arquitectura de coordinación inteligente

Este grafo se puede abrir en LangGraph Studio.
"""

from typing import TypedDict, List
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END


# =============================================================================
# State Definition
# =============================================================================

class OrchestratorState(TypedDict):
    """Estado del sistema orchestrator-workers."""
    query: str                  # Consulta original del usuario
    plan: str                   # Plan actual del orchestrator
    worker_results: List[str]   # Resultados de workers ejecutados
    final_answer: str           # Respuesta final consolidada


# =============================================================================
# LLM Configuration
# =============================================================================

llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.3)


# =============================================================================
# Orchestrator Node (The "Brain")
# =============================================================================

def orchestrator(state: OrchestratorState) -> dict:
    """
    Orchestrator: El "cerebro" del sistema.

    Responsabilidades:
    1. Analiza la consulta y resultados previos
    2. Decide qué worker necesita ejecutarse siguiente
    3. Determina cuándo hay suficiente información
    4. Planifica la estrategia de ejecución

    Decisiones posibles:
    - search_worker: Buscar información
    - analyze_worker: Analizar datos
    - calculate_worker: Hacer cálculos
    - synthesize: Consolidar resultados
    - done: Tarea completada
    """
    query = state['query']
    results = state.get('worker_results', [])

    print(f'\n🎼 ORCHESTRATOR evaluando...')
    print(f'   Query: "{query[:50]}..."')
    print(f'   Resultados hasta ahora: {len(results)} workers ejecutados')

    # ¿Ya tenemos suficiente información?
    if len(results) >= 3:
        print(f'   Decisión: SUFICIENTE INFO → Sintetizar')
        return {'plan': 'synthesize'}

    # Decidir qué worker necesitamos
    prompt = f'''Eres un orchestrator que coordina workers especializados.

CONSULTA ORIGINAL: {query}

RESULTADOS PREVIOS:
{chr(10).join(f"- {r}" for r in results) if results else "Ninguno aún"}

WORKERS DISPONIBLES:
1. search_worker - Busca información en bases de conocimiento
2. analyze_worker - Analiza y procesa datos
3. calculate_worker - Realiza cálculos y operaciones
4. done - Ya tenemos suficiente información

INSTRUCCIONES:
- Analiza qué información falta
- Decide qué worker ejecutar SIGUIENTE
- Si ya hay suficiente info, responde "done"
- Responde SOLO con: search_worker, analyze_worker, calculate_worker, o done
- NO incluyas explicaciones'''

    decision = llm.invoke(prompt).content.strip().lower()

    # Normalizar respuesta
    if 'search' in decision:
        decision = 'search_worker'
    elif 'analyze' in decision:
        decision = 'analyze_worker'
    elif 'calculate' in decision:
        decision = 'calculate_worker'
    elif 'done' in decision or 'synthesize' in decision:
        decision = 'synthesize'

    print(f'   Decisión: {decision.upper()}')

    return {'plan': decision}


# =============================================================================
# Worker Nodes (The "Hands")
# =============================================================================

def search_worker(state: OrchestratorState) -> dict:
    """
    Search Worker: Especialista en búsqueda de información.

    Simula búsqueda en bases de conocimiento, documentación, etc.
    """
    print(f'\n🔍 SEARCH WORKER ejecutando...')

    query = state['query']

    prompt = f'''Eres un worker especializado en búsqueda de información.

Tarea: Buscar información relevante sobre: {query}

Instrucciones:
- Simula una búsqueda en bases de conocimiento
- Proporciona datos relevantes y específicos
- Formato: "Búsqueda completada: [información encontrada]"
- Máximo 80 palabras'''

    response = llm.invoke(prompt)
    result = f"[SEARCH] {response.content}"

    # Agregar a resultados existentes
    current_results = state.get('worker_results', [])
    updated_results = current_results + [result]

    print(f'   ✅ Búsqueda completada')

    return {'worker_results': updated_results}


def analyze_worker(state: OrchestratorState) -> dict:
    """
    Analyze Worker: Especialista en análisis de datos.

    Procesa, analiza y extrae insights de información.
    """
    print(f'\n📊 ANALYZE WORKER ejecutando...')

    query = state['query']
    previous_results = state.get('worker_results', [])

    prompt = f'''Eres un worker especializado en análisis de datos.

Tarea: Analizar información sobre: {query}

Contexto previo:
{chr(10).join(previous_results) if previous_results else "Ninguno"}

Instrucciones:
- Analiza la información disponible
- Proporciona insights y conclusiones
- Formato: "Análisis completado: [insights encontrados]"
- Máximo 80 palabras'''

    response = llm.invoke(prompt)
    result = f"[ANALYZE] {response.content}"

    # Agregar a resultados existentes
    current_results = state.get('worker_results', [])
    updated_results = current_results + [result]

    print(f'   ✅ Análisis completado')

    return {'worker_results': updated_results}


def calculate_worker(state: OrchestratorState) -> dict:
    """
    Calculate Worker: Especialista en cálculos y operaciones.

    Realiza cálculos, estimaciones, proyecciones.
    """
    print(f'\n🔢 CALCULATE WORKER ejecutando...')

    query = state['query']
    previous_results = state.get('worker_results', [])

    prompt = f'''Eres un worker especializado en cálculos y operaciones.

Tarea: Realizar cálculos relacionados con: {query}

Contexto previo:
{chr(10).join(previous_results) if previous_results else "Ninguno"}

Instrucciones:
- Identifica qué cálculos son necesarios
- Realiza estimaciones o cálculos relevantes
- Formato: "Cálculo completado: [resultados]"
- Máximo 80 palabras'''

    response = llm.invoke(prompt)
    result = f"[CALCULATE] {response.content}"

    # Agregar a resultados existentes
    current_results = state.get('worker_results', [])
    updated_results = current_results + [result]

    print(f'   ✅ Cálculos completados')

    return {'worker_results': updated_results}


# =============================================================================
# Synthesis Node
# =============================================================================

def synthesize(state: OrchestratorState) -> dict:
    """
    Sintetiza todos los resultados de workers en una respuesta final.

    Combina información de:
    - Search worker
    - Analyze worker
    - Calculate worker

    En una respuesta coherente y completa.
    """
    print(f'\n🔨 SYNTHESIZE consolidando resultados...')

    query = state['query']
    results = state.get('worker_results', [])

    prompt = f'''Sintetiza los resultados de múltiples workers en una respuesta final.

CONSULTA ORIGINAL: {query}

RESULTADOS DE WORKERS:
{chr(10).join(results)}

INSTRUCCIONES:
- Combina toda la información en una respuesta coherente
- Responde directamente a la consulta original
- Incluye datos, análisis y conclusiones
- Formato claro y profesional
- Máximo 200 palabras'''

    response = llm.invoke(prompt)
    final_answer = response.content

    print(f'   ✅ Síntesis completada')

    return {'final_answer': final_answer}


# =============================================================================
# Routing Logic
# =============================================================================

def route_decision(state: OrchestratorState) -> str:
    """
    Función de routing basada en la decisión del orchestrator.

    Mapea el 'plan' del orchestrator al siguiente nodo:
    - search_worker → nodo 'search'
    - analyze_worker → nodo 'analyze'
    - calculate_worker → nodo 'calculate'
    - synthesize/done → nodo 'synthesize'
    """
    plan = state['plan']

    if plan == 'search_worker':
        return 'search'
    elif plan == 'analyze_worker':
        return 'analyze'
    elif plan == 'calculate_worker':
        return 'calculate'
    elif plan == 'synthesize' or plan == 'done':
        return 'synthesize'
    else:
        # Fallback: Si no reconoce el plan, ir a synthesize
        return 'synthesize'


# =============================================================================
# Graph Construction
# =============================================================================

def create_graph():
    """
    Construye el grafo orchestrator-workers.

    Arquitectura (con LOOP de re-planificación):

        START
          ↓
      orchestrator ←──────────┐
          ↓                    │
        route                  │
          ↓                    │
    ┌─────┴─────┬──────────┐  │
    ↓           ↓          ↓  │
  search     analyze   calculate
    │           │          │  │
    └───────────┴──────────┘  │
                │              │
                └──────────────┘ (loop back)
                ↓
           synthesize
                ↓
              END

    El orchestrator puede ejecutar múltiples workers antes de sintetizar.

    Returns:
        CompiledGraph: Grafo compilado listo para ejecutar
    """
    # 1. Crear el builder
    builder = StateGraph(OrchestratorState)
    print("✅ StateGraph creado")

    # 2. Agregar nodos
    builder.add_node("orchestrator", orchestrator)
    builder.add_node("search", search_worker)
    builder.add_node("analyze", analyze_worker)
    builder.add_node("calculate", calculate_worker)
    builder.add_node("synthesize", synthesize)
    print("✅ Nodos agregados")

    # 3. Conectar edges
    # START → orchestrator
    builder.add_edge(START, "orchestrator")

    # orchestrator → routing condicional
    builder.add_conditional_edges(
        "orchestrator",
        route_decision,
        {
            'search': 'search',
            'analyze': 'analyze',
            'calculate': 'calculate',
            'synthesize': 'synthesize'
        }
    )

    # Workers → orchestrator (loop para re-planificación)
    builder.add_edge("search", "orchestrator")
    builder.add_edge("analyze", "orchestrator")
    builder.add_edge("calculate", "orchestrator")

    # synthesize → END
    builder.add_edge("synthesize", END)

    print("✅ Edges conectados (con loops)")

    # 4. Compilar
    graph = builder.compile()
    print("🎉 Grafo orchestrator-workers compilado exitosamente\n")

    return graph


# =============================================================================
# Create the graph (for LangGraph Studio)
# =============================================================================

graph = create_graph()


# =============================================================================
# Testing Function (optional)
# =============================================================================

def main():
    """
    Función de prueba con consultas complejas.
    """
    print("="*70)
    print("🎼 Sistema Orchestrator-Workers")
    print("="*70)

    # Consultas de prueba
    test_queries = [
        "Investiga las tendencias de LangGraph en 2024 y proyecta su adopción",
        "Analiza el mercado de IA generativa y calcula el ROI estimado",
        "Busca información sobre multi-agent systems y sus aplicaciones",
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*70}")
        print(f"TEST {i}/{len(test_queries)}")
        print(f"{'='*70}")
        print(f"\n📥 CONSULTA:")
        print(f"   '{query}'")
        print()

        # Ejecutar el grafo
        result = graph.invoke({
            'query': query,
            'plan': '',
            'worker_results': [],
            'final_answer': ''
        })

        # Mostrar resultados
        print(f"\n{'='*70}")
        print(f"📊 RESULTADOS FINALES")
        print(f"{'='*70}")
        print(f"\n📝 Workers ejecutados: {len(result.get('worker_results', []))}")
        for j, worker_result in enumerate(result.get('worker_results', []), 1):
            print(f"\n   {j}. {worker_result[:100]}...")

        print(f"\n💡 RESPUESTA FINAL:")
        print(f"{result.get('final_answer', 'N/A')}")
        print(f"\n{'='*70}\n")

    print("\n✅ Todos los tests completados")

    # Estadísticas
    print(f"\n📊 ESTADÍSTICAS:")
    print(f"   Total de consultas: {len(test_queries)}")
    print(f"   Workers disponibles: 3 (search, analyze, calculate)")
    print(f"   Patrón: Orchestrator coordina workers especializados")
    print(f"   Característica clave: Re-planificación dinámica con loops")


if __name__ == "__main__":
    main()
