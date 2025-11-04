"""
Ejercicio 3.1: Agente Autónomo con Planificación Dinámica

Este módulo implementa el pattern Plan-Execute-Evaluate donde:
- El agente crea un plan explícito
- Ejecuta el plan paso a paso
- Evalúa progreso y se adapta dinámicamente

Conceptos clave:
- Planificación explícita
- Ejecución iterativa
- Evaluación continua
- Adaptación dinámica
"""

from typing import TypedDict, Literal, List, Dict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

load_dotenv()

# =============================================================================
# DEFINICIÓN DEL ESTADO
# =============================================================================

class PlanExecuteState(TypedDict):
    """
    Estado para agente con planificación.

    Flujo:
    1. objective: Objetivo del usuario
    2. plan: Plan creado por el planner
    3. current_step: Paso actual en ejecución
    4. observations: Resultados de pasos ejecutados
    5. decision: Decisión del evaluator (CONTINUE/REPLAN/FINISH)
    6. final_response: Respuesta final
    """
    objective: str
    plan: str
    current_step: int
    observations: List[Dict]
    decision: str
    final_response: str


# =============================================================================
# HERRAMIENTAS
# =============================================================================

@tool
def search_web(query: str) -> str:
    """
    Busca información en la web (simulado).

    Args:
        query: Consulta de búsqueda

    Returns:
        Información encontrada
    """
    # Simulación de búsqueda
    simulated_results = {
        "inteligencia artificial": "La IA es el campo de la informática que busca crear sistemas inteligentes. Incluye ML, NLP, visión computacional.",
        "aplicaciones ia": "IA se usa en: asistentes virtuales, diagnóstico médico, vehículos autónomos, recomendaciones personalizadas.",
        "tendencias ia": "Tendencias actuales: LLMs, IA generativa, agentes autónomos, IA multimodal.",
    }

    query_lower = query.lower()
    for key, value in simulated_results.items():
        if key in query_lower:
            return value

    return f"Información general sobre: {query}"


@tool
def calculator(expression: str) -> str:
    """
    Calcula expresiones matemáticas.

    Args:
        expression: Expresión a calcular

    Returns:
        Resultado del cálculo
    """
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


tools = [search_web, calculator]
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools(tools)


# =============================================================================
# NODO DE PLANIFICACIÓN
# =============================================================================

def planner_node(state: PlanExecuteState) -> dict:
    """
    Crea un plan de acción para alcanzar el objetivo.

    TODO: Implementar planificador
    - Analizar el objetivo
    - Crear plan paso a paso
    - Retornar {"plan": plan, "current_step": 0, "observations": []}

    El plan debe ser:
    - Específico y accionable
    - En orden lógico
    - Indicar herramientas a usar
    """
    print("\n" + "="*70)
    print("📋 PLANNER: Creando plan de acción...")
    print("="*70)

    objective = state["objective"]

    # TODO: Tu código aquí
    # Crear prompt que genere un plan detallado
    # Invocar el LLM
    # Retornar el plan

    plan = "TODO: Implementar planificador"

    print(f"\n✓ Plan creado:")
    print(plan)

    return {
        "plan": plan,
        "current_step": 0,
        "observations": []
    }


# =============================================================================
# NODO DE EJECUCIÓN
# =============================================================================

def executor_node(state: PlanExecuteState) -> dict:
    """
    Ejecuta un paso del plan.

    TODO: Implementar ejecutor
    - Leer el paso actual del plan
    - Ejecutar usando herramientas disponibles
    - Registrar observación
    - Incrementar current_step
    - Retornar {"observations": [...], "current_step": step + 1}

    Pista: Puedes usar llm_with_tools para que el agente
    decida qué herramienta usar.
    """
    print("\n" + "="*70)
    print(f"⚙️  EXECUTOR: Ejecutando paso {state['current_step'] + 1}...")
    print("="*70)

    plan = state["plan"]
    current_step = state["current_step"]
    observations = state.get("observations", [])

    # TODO: Tu código aquí
    # 1. Extraer el paso actual del plan
    # 2. Crear prompt para ejecutar ese paso
    # 3. Invocar llm_with_tools
    # 4. Si hay tool_calls, ejecutar herramientas
    # 5. Registrar observación
    # 6. Incrementar paso

    observation = {
        "step": current_step,
        "action": "TODO",
        "result": "TODO"
    }

    observations.append(observation)

    print(f"✓ Paso ejecutado: {observation['result'][:100]}...")

    return {
        "observations": observations,
        "current_step": current_step + 1
    }


# =============================================================================
# NODO DE EVALUACIÓN
# =============================================================================

def evaluator_node(state: PlanExecuteState) -> dict:
    """
    Evalúa el progreso y decide el siguiente paso.

    TODO: Implementar evaluador
    - Analizar objetivo, plan y observaciones
    - Decidir: CONTINUE, REPLAN, o FINISH
    - Retornar {"decision": decision}

    Decisiones:
    - CONTINUE: Seguir con el plan actual
    - REPLAN: Crear nuevo plan (algo salió mal)
    - FINISH: Objetivo completado
    """
    print("\n" + "="*70)
    print("🔍 EVALUATOR: Evaluando progreso...")
    print("="*70)

    objective = state["objective"]
    plan = state["plan"]
    observations = state["observations"]
    current_step = state["current_step"]

    # TODO: Tu código aquí
    # Crear prompt que evalúe el progreso
    # Invocar el LLM
    # Parsear decisión (CONTINUE/REPLAN/FINISH)

    decision = "CONTINUE"  # TODO: Implementar evaluación real

    print(f"✓ Decisión: {decision}")

    return {"decision": decision}


# =============================================================================
# NODO FINAL
# =============================================================================

def finish_node(state: PlanExecuteState) -> dict:
    """
    Genera respuesta final basándose en las observaciones.

    TODO: Implementar finalización
    - Sintetizar todas las observaciones
    - Crear respuesta coherente
    - Retornar {"final_response": response}
    """
    print("\n" + "="*70)
    print("✅ FINISH: Generando respuesta final...")
    print("="*70)

    objective = state["objective"]
    observations = state["observations"]

    # TODO: Tu código aquí
    # Sintetizar observaciones en respuesta final

    final_response = "TODO: Implementar síntesis final"

    return {"final_response": final_response}


# =============================================================================
# FUNCIÓN DE ROUTING
# =============================================================================

def route_decision(state: PlanExecuteState) -> Literal["executor", "planner", "finish"]:
    """
    Routing basado en la decisión del evaluator.

    TODO: Implementar routing
    - Leer state["decision"]
    - Mapear a nombre de nodo
    - Retornar el nombre del nodo
    """
    decision = state["decision"]

    # TODO: Tu código aquí
    # Crear mapeo de decision → nodo
    # Retornar el nodo apropiado

    return "finish"  # TODO: Implementar routing real


# =============================================================================
# CONSTRUCCIÓN DEL GRAFO
# =============================================================================

def build_graph():
    """
    Construye el grafo Plan-Execute-Evaluate.

    TODO: Implementar grafo
    - Agregar nodos: planner, executor, evaluator, finish
    - Entry point: planner
    - Flujo: planner → executor → evaluator
    - Conditional edge desde evaluator
    - finish → END

    Arquitectura con ciclos:
        planner → executor → evaluator
                     ↑          ↓
                     └─────────┐│
                              │↓
                            finish
    """
    workflow = StateGraph(PlanExecuteState)

    # TODO: Tu código aquí
    # workflow.add_node(...)
    # workflow.set_entry_point(...)
    # workflow.add_edge(...)
    # workflow.add_conditional_edges(...)

    return workflow.compile()


# =============================================================================
# EJECUCIÓN
# =============================================================================

def main():
    print("\n" + "="*70)
    print("🤖 AGENTE AUTÓNOMO CON PLANIFICACIÓN DINÁMICA")
    print("="*70)

    objectives = [
        "Investiga sobre inteligencia artificial y crea un breve reporte con aplicaciones actuales",
        "Calcula cuánto es 15% de 1000 y luego multiplica el resultado por 3",
    ]

    app = build_graph()

    for i, objective in enumerate(objectives, 1):
        print(f"\n{'='*70}")
        print(f"🎯 OBJETIVO {i}: {objective}")
        print('='*70)

        initial_state = {
            "objective": objective,
            "plan": "",
            "current_step": 0,
            "observations": [],
            "decision": "",
            "final_response": ""
        }

        # Ejecutar con límite de iteraciones
        final_state = app.invoke(initial_state, {"recursion_limit": 20})

        print(f"\n{'='*70}")
        print("📊 RESULTADO FINAL")
        print('='*70)
        print(final_state["final_response"])

        if i < len(objectives):
            input("\n[Presiona Enter...]")

    print("\n" + "="*70)
    print("🎉 ¡Ejercicio completado!")
    print("="*70)


if __name__ == "__main__":
    main()
