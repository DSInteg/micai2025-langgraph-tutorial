"""
EJEMPLO: Red Colaborativa con Handoffs (Módulo 3.2)

Este ejemplo demuestra agentes que se pasan el control dinámicamente.
"""

from typing import TypedDict, Literal, List, Dict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()

# Estado
class HandoffState(TypedDict):
    query: str
    current_agent: str
    reports: Dict[str, str]
    handoff_history: List[str]
    final_answer: str

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# Agentes especializados
def code_agent(state: HandoffState) -> dict:
    """Agente de código."""
    print(f"\n💻 CODE AGENT: Analizando aspectos de código...")

    query = state["query"]
    reports = state.get("reports", {})

    prompt = f"""Eres un especialista en código. Analiza:

QUERY: {query}

CONTEXTO DE OTROS AGENTES:
{reports}

Tu análisis de código:"""

    response = llm.invoke(prompt)
    analysis = response.content

    # Decidir handoff
    decision_prompt = f"""Tu análisis: {analysis[:200]}

¿Necesitas ayuda de otro especialista?
- SECURITY: Si hay aspectos de seguridad
- FINISH: Si puedes terminar

DECISIÓN:"""

    decision = llm.invoke(decision_prompt)
    next_agent = "finish" if "FINISH" in decision.content.upper() else "security"

    reports_updated = reports.copy()
    reports_updated["code"] = analysis

    history = state.get("handoff_history", []) + ["code → " + next_agent]

    return {
        "current_agent": next_agent,
        "reports": reports_updated,
        "handoff_history": history
    }

def security_agent(state: HandoffState) -> dict:
    """Agente de seguridad."""
    print(f"\n🔒 SECURITY AGENT: Analizando aspectos de seguridad...")

    query = state["query"]
    reports = state.get("reports", {})

    prompt = f"""Eres un especialista en seguridad. Analiza:

QUERY: {query}

ANÁLISIS PREVIO DE CÓDIGO:
{reports.get('code', 'N/A')}

Tu análisis de seguridad:"""

    response = llm.invoke(prompt)
    analysis = response.content

    reports_updated = reports.copy()
    reports_updated["security"] = analysis

    history = state.get("handoff_history", []) + ["security → finish"]

    return {
        "current_agent": "finish",
        "reports": reports_updated,
        "handoff_history": history
    }

def finish_node(state: HandoffState) -> dict:
    """Genera respuesta final."""
    print(f"\n✅ FINISH: Sintetizando respuesta...")

    reports = state.get("reports", {})

    prompt = f"""Sintetiza estos análisis en una respuesta final:

QUERY: {state['query']}

ANÁLISIS:
{reports}

RESPUESTA FINAL:"""

    response = llm.invoke(prompt)

    return {"final_answer": response.content}

# Routing
def route_handoff(state: HandoffState) -> Literal["code", "security", "finish"]:
    """Rutea según current_agent."""
    agent_map = {
        "code": "code",
        "security": "security",
        "finish": "finish"
    }
    return agent_map.get(state.get("current_agent", "code"), "finish")

# Construir grafo
def build_handoff_system():
    workflow = StateGraph(HandoffState)

    workflow.add_node("code", code_agent)
    workflow.add_node("security", security_agent)
    workflow.add_node("finish", finish_node)

    workflow.set_entry_point("code")

    # Conditional edges permiten handoffs dinámicos
    workflow.add_conditional_edges(
        "code",
        route_handoff,
        {
            "code": "code",
            "security": "security",
            "finish": "finish"
        }
    )

    workflow.add_conditional_edges(
        "security",
        route_handoff,
        {
            "code": "code",
            "security": "security",
            "finish": "finish"
        }
    )

    workflow.add_edge("finish", END)

    return workflow.compile()

# Ejecutar
if __name__ == "__main__":
    app = build_handoff_system()

    queries = [
        "¿Cómo implemento autenticación JWT en mi API?",
        "Tengo un bug en mi función de login"
    ]

    for query in queries:
        print("\n" + "="*70)
        print(f"💬 QUERY: {query}")
        print("="*70)

        result = app.invoke({
            "query": query,
            "current_agent": "code",
            "reports": {},
            "handoff_history": [],
            "final_answer": ""
        })

        print("\n" + "="*70)
        print("📊 RESULTADO")
        print("="*70)
        print(f"Flujo de handoffs: {' → '.join(result['handoff_history'])}")
        print(f"\n{result['final_answer'][:300]}...")
