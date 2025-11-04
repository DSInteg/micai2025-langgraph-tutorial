"""
EJEMPLO: Paralelización con Agregación (Módulo 2.2)

Este ejemplo demuestra análisis paralelo y agregación de resultados.
"""

from typing import TypedDict, Annotated, List
from operator import add
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()

# Estado con reducer para análisis
class ParallelState(TypedDict):
    topic: str
    analyses: Annotated[List[dict], add]  # Reducer: concatena listas
    final_summary: str

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Nodo broadcast
def broadcast_node(state: ParallelState) -> dict:
    """Prepara el tema para análisis."""
    print(f"📢 Broadcasting topic: {state['topic']}")
    return {}

# Analistas paralelos
def optimistic_analyst(state: ParallelState) -> dict:
    """Análisis optimista."""
    prompt = f"""Analiza este tema desde una perspectiva OPTIMISTA:

Tema: {state['topic']}

¿Qué oportunidades y beneficios ves?

Análisis optimista:"""

    response = llm.invoke(prompt)
    return {
        "analyses": [{
            "perspective": "optimistic",
            "content": response.content
        }]
    }

def pessimistic_analyst(state: ParallelState) -> dict:
    """Análisis pesimista."""
    prompt = f"""Analiza este tema desde una perspectiva PESIMISTA:

Tema: {state['topic']}

¿Qué riesgos y problemas ves?

Análisis pesimista:"""

    response = llm.invoke(prompt)
    return {
        "analyses": [{
            "perspective": "pessimistic",
            "content": response.content
        }]
    }

def neutral_analyst(state: ParallelState) -> dict:
    """Análisis neutral."""
    prompt = f"""Analiza este tema desde una perspectiva NEUTRAL y objetiva:

Tema: {state['topic']}

Análisis balanceado:"""

    response = llm.invoke(prompt)
    return {
        "analyses": [{
            "perspective": "neutral",
            "content": response.content
        }]
    }

# Agregador
def aggregator_node(state: ParallelState) -> dict:
    """Agrega todos los análisis."""
    print(f"\n🔄 Agregando {len(state['analyses'])} análisis...")

    # Preparar contexto
    context = ""
    for analysis in state["analyses"]:
        context += f"\n\n{analysis['perspective'].upper()}:\n{analysis['content']}"

    prompt = f"""Sintetiza estos tres análisis en un resumen ejecutivo balanceado:

{context}

Genera un resumen que integre las tres perspectivas:

RESUMEN EJECUTIVO:"""

    response = llm.invoke(prompt)
    return {"final_summary": response.content}

# Construir grafo
def build_parallel_system():
    workflow = StateGraph(ParallelState)

    # Nodos
    workflow.add_node("broadcast", broadcast_node)
    workflow.add_node("optimistic", optimistic_analyst)
    workflow.add_node("pessimistic", pessimistic_analyst)
    workflow.add_node("neutral", neutral_analyst)
    workflow.add_node("aggregator", aggregator_node)

    # Flujo
    workflow.set_entry_point("broadcast")

    # Parallelization: broadcast → 3 analistas
    workflow.add_edge("broadcast", "optimistic")
    workflow.add_edge("broadcast", "pessimistic")
    workflow.add_edge("broadcast", "neutral")

    # Convergencia: analistas → aggregator
    workflow.add_edge("optimistic", "aggregator")
    workflow.add_edge("pessimistic", "aggregator")
    workflow.add_edge("neutral", "aggregator")

    workflow.add_edge("aggregator", END)

    return workflow.compile()

# Ejecutar
if __name__ == "__main__":
    app = build_parallel_system()

    topics = [
        "La adopción de Inteligencia Artificial en empresas",
        "Trabajo remoto vs. presencial"
    ]

    for topic in topics:
        print(f"\n{'='*70}")
        print(f"📊 TEMA: {topic}")
        print(f"{'='*70}")

        result = app.invoke({
            "topic": topic,
            "analyses": [],
            "final_summary": ""
        })

        print("\n" + "="*70)
        print("📋 RESUMEN EJECUTIVO")
        print("="*70)
        print(result["final_summary"])
        print(f"\n✓ Integró {len(result['analyses'])} perspectivas diferentes")
