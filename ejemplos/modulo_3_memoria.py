"""
EJEMPLO: Memoria Compartida (Módulo 3.3)

Este ejemplo demuestra agentes que aprenden de interacciones pasadas.
"""

from typing import TypedDict, List, Dict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()

# Estado
class MemoryState(TypedDict):
    query: str
    similar_cases: List[Dict]
    response: str
    memory: Dict  # Memoria compartida persistente

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

# Funciones de memoria
def search_memory(query: str, memory: Dict) -> List[Dict]:
    """Busca casos similares en memoria."""
    query_words = set(query.lower().split())
    results = []

    for case in memory.get("cases", []):
        case_words = set(case["query"].lower().split())
        overlap = len(query_words & case_words)

        if overlap > 1:
            results.append({
                "query": case["query"],
                "response": case["response"],
                "relevance": overlap
            })

    results.sort(key=lambda x: x["relevance"], reverse=True)
    return results[:3]

def save_to_memory(query: str, response: str, memory: Dict):
    """Guarda caso en memoria."""
    if "cases" not in memory:
        memory["cases"] = []

    memory["cases"].append({
        "query": query,
        "response": response
    })

# Nodos
def memory_search_node(state: MemoryState) -> dict:
    """Busca en memoria."""
    print(f"\n🧠 MEMORY: Buscando casos similares...")

    similar = search_memory(state["query"], state["memory"])

    if similar:
        print(f"   ✓ Encontrados {len(similar)} casos similares")
    else:
        print(f"   ℹ  Sin casos previos (primera vez)")

    return {"similar_cases": similar}

def response_node(state: MemoryState) -> dict:
    """Genera respuesta usando memoria."""
    print(f"\n💬 RESPONSE: Generando respuesta...")

    query = state["query"]
    similar = state.get("similar_cases", [])

    context = ""
    if similar:
        context = "\n\nCASOS SIMILARES PREVIOS:\n"
        for case in similar:
            context += f"- Q: {case['query']}\n  A: {case['response'][:100]}...\n"

    prompt = f"""Responde esta pregunta:

PREGUNTA: {query}

{context}

{'Usa los casos previos como referencia pero adapta tu respuesta.' if similar else 'Es un caso nuevo, responde lo mejor que puedas.'}

RESPUESTA:"""

    response = llm.invoke(prompt)

    return {"response": response.content}

def memory_update_node(state: MemoryState) -> dict:
    """Actualiza memoria."""
    print(f"\n💾 MEMORY UPDATE: Guardando caso...")

    save_to_memory(
        state["query"],
        state["response"],
        state["memory"]
    )

    total = len(state["memory"]["cases"])
    print(f"   ✓ Total casos en memoria: {total}")

    return {}

# Construir grafo
def build_memory_system():
    workflow = StateGraph(MemoryState)

    workflow.add_node("search", memory_search_node)
    workflow.add_node("respond", response_node)
    workflow.add_node("update", memory_update_node)

    workflow.set_entry_point("search")
    workflow.add_edge("search", "respond")
    workflow.add_edge("respond", "update")
    workflow.add_edge("update", END)

    return workflow.compile()

# Ejecutar
if __name__ == "__main__":
    app = build_memory_system()

    # Memoria compartida (persiste entre invocaciones)
    shared_memory = {"cases": []}

    queries = [
        "¿Cómo implemento un API REST en Python?",
        "¿Cuál es la mejor forma de crear una API REST con Python?",
        "¿Cómo hago tests unitarios en Python?",
        "Necesito crear una API REST, ¿algún consejo?"
    ]

    for i, query in enumerate(queries, 1):
        print("\n" + "="*70)
        print(f"💬 CONSULTA {i}: {query}")
        print("="*70)

        result = app.invoke({
            "query": query,
            "similar_cases": [],
            "response": "",
            "memory": shared_memory  # Misma memoria compartida
        })

        print("\n📝 RESPUESTA:")
        print(result["response"][:250] + "...")

        if i == 2:
            print("\n💡 OBSERVA: Las consultas 2 y 4 encontrarán casos similares de la 1")

    print("\n" + "="*70)
    print(f"📊 RESUMEN: {len(shared_memory['cases'])} casos guardados en memoria")
    print("="*70)
