"""
EJEMPLO: Plan-Execute-Evaluate Pattern (Módulo 3.1)

Este ejemplo demuestra un agente con planificación explícita.
"""

from typing import TypedDict, Literal
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.graph import StateGraph, END

load_dotenv()

# Estado
class PlanExecuteState(TypedDict):
    objective: str
    plan: str
    current_step: int
    observations: list
    decision: str
    result: str

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Herramientas
@tool
def search_info(query: str) -> str:
    """Busca información (simulado)."""
    responses = {
        "python": "Python es un lenguaje de programación de alto nivel.",
        "langgraph": "LangGraph es un framework para construir agentes multi-agente.",
        "default": "Información no disponible."
    }
    for key in responses:
        if key in query.lower():
            return responses[key]
    return responses["default"]

# Planner
def planner_node(state: PlanExecuteState) -> dict:
    """Crea un plan explícito."""
    print(f"\n📋 PLANNER: Creando plan para '{state['objective']}'")

    prompt = f"""Crea un plan detallado para lograr este objetivo:

OBJETIVO: {state['objective']}

Genera un plan con pasos numerados y específicos.

PLAN:"""

    response = llm.invoke(prompt)
    print(f"   ✓ Plan creado")

    return {
        "plan": response.content,
        "current_step": 0,
        "observations": []
    }

# Executor
def executor_node(state: PlanExecuteState) -> dict:
    """Ejecuta el paso actual del plan."""
    plan_lines = [l for l in state["plan"].split('\n') if l.strip() and l[0].isdigit()]

    if state["current_step"] >= len(plan_lines):
        return {"current_step": state["current_step"]}

    step = plan_lines[state["current_step"]]
    print(f"\n⚙️  EXECUTOR: Ejecutando paso {state['current_step'] + 1}")
    print(f"   {step}")

    # Simular ejecución (en realidad usaría herramientas)
    result = f"Completado: {step}"

    observations = state["observations"] + [{
        "step": state["current_step"],
        "action": step,
        "result": result
    }]

    return {
        "observations": observations,
        "current_step": state["current_step"] + 1
    }

# Evaluator
def evaluator_node(state: PlanExecuteState) -> dict:
    """Evalúa progreso y decide siguiente acción."""
    print(f"\n🔍 EVALUATOR: Evaluando progreso...")

    plan_lines = [l for l in state["plan"].split('\n') if l.strip() and l[0].isdigit()]
    total_steps = len(plan_lines)
    completed = len(state["observations"])

    prompt = f"""Evalúa el progreso:

OBJETIVO: {state['objective']}
PLAN: {state['plan']}
PASOS COMPLETADOS: {completed}/{total_steps}
OBSERVACIONES: {state['observations'][-1] if state['observations'] else 'Ninguna'}

Decisión:
- CONTINUE: Si hay más pasos y todo va bien
- FINISH: Si el objetivo está completado

DECISIÓN:"""

    response = llm.invoke(prompt)
    decision = response.content.strip().upper()

    if "FINISH" in decision or completed >= total_steps:
        decision = "FINISH"
    else:
        decision = "CONTINUE"

    print(f"   → Decisión: {decision}")
    return {"decision": decision}

# Finish
def finish_node(state: PlanExecuteState) -> dict:
    """Genera resultado final."""
    print(f"\n✅ FINISH: Objetivo completado")

    result = f"Objetivo '{state['objective']}' completado con éxito.\n"
    result += f"Pasos ejecutados: {len(state['observations'])}"

    return {"result": result}

# Routing
def route_decision(state: PlanExecuteState) -> Literal["executor", "finish"]:
    """Rutea según la decisión del evaluator."""
    if state.get("decision") == "FINISH":
        return "finish"
    return "executor"

# Construir grafo
def build_plan_execute():
    workflow = StateGraph(PlanExecuteState)

    workflow.add_node("planner", planner_node)
    workflow.add_node("executor", executor_node)
    workflow.add_node("evaluator", evaluator_node)
    workflow.add_node("finish", finish_node)

    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "executor")
    workflow.add_edge("executor", "evaluator")

    workflow.add_conditional_edges(
        "evaluator",
        route_decision,
        {
            "executor": "executor",
            "finish": "finish"
        }
    )

    workflow.add_edge("finish", END)

    return workflow.compile()

# Ejecutar
if __name__ == "__main__":
    app = build_plan_execute()

    objective = "Investigar qué es LangGraph y crear un ejemplo simple"

    print("="*70)
    print(f"🎯 OBJETIVO: {objective}")
    print("="*70)

    result = app.invoke({
        "objective": objective,
        "plan": "",
        "current_step": 0,
        "observations": [],
        "decision": "",
        "result": ""
    })

    print("\n" + "="*70)
    print("📊 RESULTADO FINAL")
    print("="*70)
    print(result["result"])
