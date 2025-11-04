"""
EJEMPLO: Sistema de Atención al Cliente (Módulo 4.1)

Este ejemplo integra múltiples patterns para un caso de uso real.
"""

from typing import TypedDict, Literal
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()

# Estado
class SupportState(TypedDict):
    query: str
    category: str
    analysis: str
    confidence: float
    response: str
    escalate: bool

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# Base de conocimiento simulada
KB = {
    "products": [
        {"name": "Laptop Pro", "price": "$1299", "warranty": "2 years"},
        {"name": "Phone Ultra", "price": "$899", "warranty": "1 year"}
    ],
    "faqs": [
        {"q": "¿Política de devoluciones?", "a": "30 días sin preguntas"}
    ]
}

# Clasificador
def classify_node(state: SupportState) -> dict:
    """Clasifica la consulta."""
    print(f"\n🎯 CLASSIFY: Categorizando consulta...")

    prompt = f"""Clasifica en: PRODUCT, SUPPORT, ORDER

Query: {state['query']}

Categoría:"""

    response = llm.invoke(prompt)
    category = response.content.strip().lower()

    if category not in ["product", "support", "order"]:
        category = "product"

    print(f"   → Categoría: {category.upper()}")
    return {"category": category}

# Agentes especializados
def product_agent(state: SupportState) -> dict:
    """Analiza productos."""
    print(f"\n💻 PRODUCT AGENT: Analizando...")

    prompt = f"""Responde sobre productos:

Query: {state['query']}

Productos disponibles:
{KB['products']}

Análisis:"""

    response = llm.invoke(prompt)
    return {
        "analysis": response.content,
        "confidence": 0.8
    }

def support_agent(state: SupportState) -> dict:
    """Soporte técnico."""
    print(f"\n🔧 SUPPORT AGENT: Analizando...")

    prompt = f"""Resuelve problema técnico:

Query: {state['query']}

Solución:"""

    response = llm.invoke(prompt)
    return {
        "analysis": response.content,
        "confidence": 0.7
    }

def order_agent(state: SupportState) -> dict:
    """Gestión de órdenes."""
    print(f"\n📦 ORDER AGENT: Analizando...")

    prompt = f"""Ayuda con orden:

Query: {state['query']}

FAQs: {KB['faqs']}

Respuesta:"""

    response = llm.invoke(prompt)
    return {
        "analysis": response.content,
        "confidence": 0.75
    }

# Síntesis
def synthesize_node(state: SupportState) -> dict:
    """Genera respuesta final."""
    print(f"\n✅ SYNTHESIZE: Generando respuesta...")

    confidence = state.get("confidence", 0.5)
    escalate = confidence < 0.6

    response = f"""Estimado cliente,

{state['analysis']}

¿Puedo ayudarle con algo más?

Saludos,
Sistema de Atención"""

    return {
        "response": response,
        "escalate": escalate
    }

# Nodos finales
def respond_node(state: SupportState) -> dict:
    """Responde al usuario."""
    print(f"\n📨 RESPOND: Enviando respuesta...")
    print(state["response"])
    return {}

def escalate_node(state: SupportState) -> dict:
    """Escala a humano."""
    print(f"\n🚨 ESCALATE: Transferiendo a agente humano...")
    print(f"   Confidence: {state.get('confidence', 0):.2f}")
    return {}

# Routing
def route_category(state: SupportState) -> Literal["product", "support", "order"]:
    return state["category"]

def route_escalate(state: SupportState) -> Literal["respond", "escalate"]:
    return "escalate" if state.get("escalate", False) else "respond"

# Construir grafo
def build_support_system():
    workflow = StateGraph(SupportState)

    # Nodos
    workflow.add_node("classify", classify_node)
    workflow.add_node("product", product_agent)
    workflow.add_node("support", support_agent)
    workflow.add_node("order", order_agent)
    workflow.add_node("synthesize", synthesize_node)
    workflow.add_node("respond", respond_node)
    workflow.add_node("escalate", escalate_node)

    # Flujo
    workflow.set_entry_point("classify")

    workflow.add_conditional_edges(
        "classify",
        route_category,
        {"product": "product", "support": "support", "order": "order"}
    )

    workflow.add_edge("product", "synthesize")
    workflow.add_edge("support", "synthesize")
    workflow.add_edge("order", "synthesize")

    workflow.add_conditional_edges(
        "synthesize",
        route_escalate,
        {"respond": "respond", "escalate": "escalate"}
    )

    workflow.add_edge("respond", END)
    workflow.add_edge("escalate", END)

    return workflow.compile()

# Ejecutar
if __name__ == "__main__":
    app = build_support_system()

    queries = [
        "¿Cuánto cuesta el Laptop Pro?",
        "Mi phone no enciende",
        "Quiero devolver un producto"
    ]

    for query in queries:
        print("\n" + "="*70)
        print(f"💬 {query}")
        print("="*70)

        app.invoke({
            "query": query,
            "category": "",
            "analysis": "",
            "confidence": 0.0,
            "response": "",
            "escalate": False
        })
