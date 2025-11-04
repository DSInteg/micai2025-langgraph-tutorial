"""
Ejercicio 3.1: Agente Autónomo con Planificación Dinámica - SOLUCIÓN COMPLETA

Implementa el pattern Plan-Execute-Evaluate para agentes autónomos avanzados.
"""

from typing import TypedDict, Literal, List, Dict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

load_dotenv()

# =============================================================================
# ESTADO Y HERRAMIENTAS
# =============================================================================

class PlanExecuteState(TypedDict):
    """Estado para agente con planificación."""
    objective: str
    plan: str
    current_step: int
    observations: List[Dict]
    decision: str
    final_response: str


@tool
def search_web(query: str) -> str:
    """Busca información en la web (simulado)."""
    simulated_results = {
        "inteligencia artificial": "La IA es el campo de la informática que busca crear sistemas inteligentes. Incluye ML, NLP, visión computacional y robótica.",
        "aplicaciones ia": "IA se usa en: asistentes virtuales (Siri, Alexa), diagnóstico médico, vehículos autónomos, sistemas de recomendación, detección de fraude.",
        "tendencias ia": "Tendencias 2024: LLMs como GPT-4, IA generativa (DALL-E, Midjourney), agentes autónomos, IA multimodal.",
        "machine learning": "ML es subcampo de IA donde sistemas aprenden de datos sin ser explícitamente programados.",
    }

    query_lower = query.lower()
    for key, value in simulated_results.items():
        if key in query_lower:
            return value

    return f"Información general sobre: {query}. Se encontraron múltiples recursos relevantes."


@tool
def calculator(expression: str) -> str:
    """Calcula expresiones matemáticas."""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error al calcular: {str(e)}"


tools = [search_web, calculator]
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools(tools)


# =============================================================================
# NODO DE PLANIFICACIÓN
# =============================================================================

def planner_node(state: PlanExecuteState) -> dict:
    """
    Crea un plan explícito de acción.

    Este nodo es crucial en el pattern Plan-Execute-Evaluate.
    A diferencia de ReAct que decide paso a paso, aquí creamos
    un plan completo antes de ejecutar.

    Beneficios:
    - Visibilidad: Podemos ver el plan antes de ejecutar
    - Optimización: El plan puede ser más eficiente
    - Debugging: Fácil identificar problemas en el plan
    """
    print("\n" + "="*70)
    print("📋 PLANNER: Creando plan de acción...")
    print("="*70)

    objective = state["objective"]

    prompt = f"""Eres un agente planificador experto. Tu trabajo es crear planes detallados.

Objetivo a alcanzar:
{objective}

Herramientas disponibles:
- search_web(query): Busca información en la web
- calculator(expression): Realiza cálculos matemáticos

Crea un plan paso a paso para alcanzar el objetivo.

Requisitos del plan:
1. Pasos numerados y específicos
2. Indicar qué herramienta usar en cada paso
3. Orden lógico de ejecución
4. Cada paso debe ser accionable

Formato:
1. [Acción específica con herramienta]
2. [Siguiente acción]
...

PLAN:"""

    response = llm.invoke(prompt)
    plan = response.content

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
    Ejecuta un paso del plan usando herramientas.

    Este nodo implementa la fase "Execute" del pattern.
    Toma el plan y ejecuta el paso actual.
    """
    print("\n" + "="*70)
    print(f"⚙️  EXECUTOR: Ejecutando paso {state['current_step'] + 1}...")
    print("="*70)

    plan = state["plan"]
    current_step = state["current_step"]
    observations = state.get("observations", [])

    # Extraer pasos del plan
    steps = [line.strip() for line in plan.split('\n') if line.strip() and line.strip()[0].isdigit()]

    if current_step >= len(steps):
        # No hay más pasos
        return {
            "observations": observations,
            "current_step": current_step
        }

    step_to_execute = steps[current_step]

    # Crear contexto para el executor
    context = "\n".join([f"Paso {obs['step'] + 1}: {obs['result']}" for obs in observations])

    prompt = f"""Ejecuta el siguiente paso del plan:

PLAN COMPLETO:
{plan}

PASO ACTUAL A EJECUTAR:
{step_to_execute}

OBSERVACIONES PREVIAS:
{context if context else "Ninguna (primer paso)"}

Ejecuta el paso usando las herramientas disponibles.
Si el paso requiere una herramienta, úsala.
Proporciona el resultado de manera concisa."""

    # Invocar el agente con herramientas
    messages = [HumanMessage(content=prompt)]
    response = llm_with_tools.invoke(messages)

    # Ejecutar herramientas si el agente las solicitó
    result_text = response.content

    if hasattr(response, 'tool_calls') and response.tool_calls:
        print(f"   → Usando herramientas: {[tc['name'] for tc in response.tool_calls]}")

        # Ejecutar cada herramienta
        tool_results = []
        for tool_call in response.tool_calls:
            tool_name = tool_call['name']
            tool_args = tool_call['args']

            # Encontrar y ejecutar la herramienta
            tool_func = next((t for t in tools if t.name == tool_name), None)
            if tool_func:
                result = tool_func.invoke(tool_args)
                tool_results.append(result)

        result_text = " | ".join(tool_results)

    observation = {
        "step": current_step,
        "action": step_to_execute,
        "result": result_text
    }

    observations.append(observation)

    print(f"✓ Resultado: {result_text[:150]}...")

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

    Este es el nodo más importante del pattern.
    Determina si:
    - CONTINUE: Seguir ejecutando el plan
    - REPLAN: El plan no funciona, crear uno nuevo
    - FINISH: Objetivo completado
    """
    print("\n" + "="*70)
    print("🔍 EVALUATOR: Evaluando progreso...")
    print("="*70)

    objective = state["objective"]
    plan = state["plan"]
    observations = state["observations"]
    current_step = state["current_step"]

    # Formatear observaciones
    obs_text = "\n".join([
        f"Paso {obs['step'] + 1}: {obs['action']}\nResultado: {obs['result']}"
        for obs in observations
    ])

    prompt = f"""Evalúa el progreso del agente hacia su objetivo.

OBJETIVO ORIGINAL:
{objective}

PLAN:
{plan}

PASOS EJECUTADOS:
{obs_text if obs_text else "Ninguno aún"}

PASO ACTUAL: {current_step + 1}

Evalúa:
1. ¿Se ha completado el objetivo satisfactoriamente?
2. ¿El plan está funcionando o necesita ajuste?
3. ¿Hay suficiente información para terminar?

Decisiones posibles:
- CONTINUE: Si el plan está funcionando y aún hay pasos por ejecutar
- REPLAN: Si el plan no está funcionando o necesita ajuste
- FINISH: Si el objetivo está completado

Proporciona SOLO una palabra: CONTINUE, REPLAN, o FINISH

DECISIÓN:"""

    response = llm.invoke(prompt)
    decision = response.content.strip().upper()

    # Validar decisión
    if decision not in ["CONTINUE", "REPLAN", "FINISH"]:
        decision = "FINISH" if len(observations) >= 3 else "CONTINUE"

    print(f"✓ Decisión: {decision}")

    if decision == "FINISH":
        print("   → Objetivo completado, generando respuesta final")
    elif decision == "REPLAN":
        print("   → Plan necesita ajuste, replanificando...")
    else:
        print("   → Continuando con el plan actual")

    return {"decision": decision}


# =============================================================================
# NODO FINAL
# =============================================================================

def finish_node(state: PlanExecuteState) -> dict:
    """
    Genera la respuesta final sintetizando todas las observaciones.
    """
    print("\n" + "="*70)
    print("✅ FINISH: Generando respuesta final...")
    print("="*70)

    objective = state["objective"]
    observations = state["observations"]

    obs_text = "\n".join([
        f"- {obs['action']}: {obs['result']}"
        for obs in observations
    ])

    prompt = f"""Genera una respuesta final para el usuario basándote en el trabajo realizado.

OBJETIVO DEL USUARIO:
{objective}

ACCIONES REALIZADAS Y RESULTADOS:
{obs_text}

Crea una respuesta coherente que:
1. Responda directamente al objetivo del usuario
2. Integre la información recopilada
3. Sea clara y bien estructurada
4. No mencione el proceso interno (plan, pasos, etc.)

RESPUESTA FINAL:"""

    response = llm.invoke(prompt)
    final_response = response.content

    print(f"✓ Respuesta generada ({len(final_response)} caracteres)")

    return {"final_response": final_response}


# =============================================================================
# FUNCIÓN DE ROUTING
# =============================================================================

def route_decision(state: PlanExecuteState) -> Literal["executor", "planner", "finish"]:
    """
    Routing basado en la decisión del evaluator.

    Este routing crea los ciclos del grafo:
    - CONTINUE → executor (ciclo: ejecutar siguiente paso)
    - REPLAN → planner (ciclo: crear nuevo plan)
    - FINISH → finish (terminar)
    """
    decision = state["decision"]

    routing_map = {
        "CONTINUE": "executor",
        "REPLAN": "planner",
        "FINISH": "finish"
    }

    next_node = routing_map.get(decision, "finish")
    print(f"   → Siguiente nodo: {next_node}")

    return next_node


# =============================================================================
# CONSTRUCCIÓN DEL GRAFO
# =============================================================================

def build_graph():
    """
    Construye el grafo Plan-Execute-Evaluate.

    Arquitectura:
    - Comienza con planner
    - Ciclo principal: executor → evaluator → [CONTINUE/REPLAN]
    - Si CONTINUE: vuelve a executor
    - Si REPLAN: vuelve a planner
    - Si FINISH: va a finish → END
    """
    workflow = StateGraph(PlanExecuteState)

    # Agregar nodos
    workflow.add_node("planner", planner_node)
    workflow.add_node("executor", executor_node)
    workflow.add_node("evaluator", evaluator_node)
    workflow.add_node("finish", finish_node)

    # Entry point: siempre comienza planificando
    workflow.set_entry_point("planner")

    # Flujo principal
    workflow.add_edge("planner", "executor")
    workflow.add_edge("executor", "evaluator")

    # Routing condicional desde evaluator
    workflow.add_conditional_edges(
        "evaluator",
        route_decision,
        {
            "executor": "executor",    # CONTINUE: siguiente paso
            "planner": "planner",      # REPLAN: nuevo plan
            "finish": "finish"         # FINISH: terminar
        }
    )

    # Fin
    workflow.add_edge("finish", END)

    return workflow.compile()


# =============================================================================
# EJECUCIÓN Y DEMO
# =============================================================================

def main():
    print("\n" + "="*70)
    print("🤖 AGENTE AUTÓNOMO CON PLANIFICACIÓN DINÁMICA")
    print("="*70)

    objectives = [
        "Investiga sobre inteligencia artificial y crea un breve reporte con sus principales aplicaciones actuales",
        "Calcula cuánto es 15% de 1000 y luego multiplica el resultado por 3. Dame el resultado final.",
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

        # Ejecutar con límite de iteraciones para evitar loops infinitos
        final_state = app.invoke(initial_state, {"recursion_limit": 20})

        print(f"\n{'='*70}")
        print("📊 RESULTADO FINAL")
        print('='*70)
        print(final_state["final_response"])

        print(f"\n📈 Estadísticas:")
        print(f"   • Pasos ejecutados: {len(final_state['observations'])}")
        print(f"   • Plan seguido: {final_state['decision']}")

        if i < len(objectives):
            input("\n[Presiona Enter para continuar...]")

    print("\n" + "="*70)
    print("🎉 ¡Ejercicio completado!")
    print("="*70)
    print("\n💡 Observaciones:")
    print("   • El agente creó un plan explícito antes de actuar")
    print("   • Ejecutó el plan paso a paso de manera estructurada")
    print("   • Evaluó su progreso después de cada paso")
    print("   • Se adaptó dinámicamente según los resultados")
    print("   • Este pattern es ideal para tareas complejas multi-paso")


if __name__ == "__main__":
    main()
