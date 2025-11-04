"""
EJEMPLO: Sistema de Routing con Múltiples Agentes (Módulo 2.1)

Este ejemplo demuestra cómo rutear consultas a agentes especializados.
"""

from typing import TypedDict, Literal
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()

# Estado
class RoutingState(TypedDict):
    query: str
    category: str
    response: str

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# Clasificador
def classifier_node(state: RoutingState) -> dict:
    """Clasifica la consulta en una categoría."""
    prompt = f"""Clasifica esta consulta en UNA categoría:

Consulta: {state['query']}

Categorías:
- TECH: Preguntas técnicas, programación, tecnología
- SALES: Preguntas sobre precios, compras, productos
- GENERAL: Otras preguntas generales

Responde SOLO con: TECH, SALES, o GENERAL

Categoría:"""

    response = llm.invoke(prompt)
    category = response.content.strip().upper()

    if category not in ["TECH", "SALES", "GENERAL"]:
        category = "GENERAL"

    print(f"   📍 Categoría: {category}")
    return {"category": category}

# Agentes especializados
def tech_agent(state: RoutingState) -> dict:
    """Agente técnico."""
    prompt = f"""Eres un especialista técnico. Responde esta consulta:

{state['query']}

Respuesta técnica y detallada:"""

    response = llm.invoke(prompt)
    return {"response": f"[TECH SPECIALIST] {response.content}"}

def sales_agent(state: RoutingState) -> dict:
    """Agente de ventas."""
    prompt = f"""Eres un especialista en ventas. Responde esta consulta:

{state['query']}

Respuesta enfocada en ventas:"""

    response = llm.invoke(prompt)
    return {"response": f"[SALES SPECIALIST] {response.content}"}

def general_agent(state: RoutingState) -> dict:
    """Agente general."""
    prompt = f"""Responde esta consulta de manera clara y concisa:

{state['query']}

Respuesta:"""

    response = llm.invoke(prompt)
    return {"response": f"[GENERAL AGENT] {response.content}"}

# Routing
def route_query(state: RoutingState) -> Literal["tech", "sales", "general"]:
    """Rutea según la categoría."""
    category_map = {
        "TECH": "tech",
        "SALES": "sales",
        "GENERAL": "general"
    }
    return category_map.get(state["category"], "general")

# Construir grafo
def build_routing_system():
    workflow = StateGraph(RoutingState)

    # Nodos
    workflow.add_node("classifier", classifier_node)
    workflow.add_node("tech", tech_agent)
    workflow.add_node("sales", sales_agent)
    workflow.add_node("general", general_agent)

    # Flujo
    workflow.set_entry_point("classifier")
    workflow.add_conditional_edges(
        "classifier",
        route_query,
        {
            "tech": "tech",
            "sales": "sales",
            "general": "general"
        }
    )
    workflow.add_edge("tech", END)
    workflow.add_edge("sales", END)
    workflow.add_edge("general", END)

    return workflow.compile()

# Ejecutar
if __name__ == "__main__":
    app = build_routing_system()

    queries = [
        "¿Cómo implemento un API REST en Python?",
        "¿Cuánto cuesta el plan enterprise?",
        "¿Cuál es el horario de atención?"
    ]

    for query in queries:
        print(f"\n{'='*60}")
        print(f"💬 Consulta: {query}")
        print(f"{'='*60}")

        result = app.invoke({
            "query": query,
            "category": "",
            "response": ""
        })

        print(f"\n✅ {result['response'][:200]}...")
