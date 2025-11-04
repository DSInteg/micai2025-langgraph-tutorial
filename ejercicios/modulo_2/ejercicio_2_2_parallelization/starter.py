"""
Ejercicio 2.2: Paralelización con Agregación

Este módulo implementa un sistema que:
- Ejecuta múltiples agentes simultáneamente sobre el mismo input
- Obtiene perspectivas diversas del mismo problema
- Agrega y sintetiza los resultados

Conceptos clave:
- Pattern de Paralelización (Map-Reduce)
- Múltiples perspectivas
- Agregación y síntesis
- Ejecución paralela en LangGraph
"""

from typing import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()

# =============================================================================
# DEFINICIÓN DEL ESTADO
# =============================================================================

class AnalysisState(TypedDict):
    """
    Estado para análisis paralelo de reseñas.

    Flujo:
    1. review: Input inicial
    2. optimistic_analysis, pessimistic_analysis, neutral_analysis: Análisis paralelos
    3. final_analysis: Síntesis agregada
    """
    review: str
    optimistic_analysis: str
    pessimistic_analysis: str
    neutral_analysis: str
    final_analysis: str


# =============================================================================
# CONFIGURACIÓN DEL LLM
# =============================================================================

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)


# =============================================================================
# AGENTES CON PERSPECTIVAS
# =============================================================================

def optimistic_agent(state: AnalysisState) -> dict:
    """
    Agente que analiza enfocándose en aspectos positivos.

    TODO: Implementar análisis optimista
    - Crear prompt que enfatice lo positivo
    - Analizar la reseña con esa perspectiva
    - Retornar {"optimistic_analysis": resultado}
    """
    print("\n😊 AGENTE OPTIMISTA: Analizando...")
    review = state["review"]

    # Tu código aquí
    analysis = "TODO: Implementar análisis optimista"

    return {"optimistic_analysis": analysis}


def pessimistic_agent(state: AnalysisState) -> dict:
    """
    Agente que analiza enfocándose en aspectos negativos.

    TODO: Implementar análisis pesimista
    - Crear prompt que enfatice lo negativo
    - Identificar problemas y debilidades
    - Retornar {"pessimistic_analysis": resultado}
    """
    print("\n😟 AGENTE PESIMISTA: Analizando...")
    review = state["review"]

    # Tu código aquí
    analysis = "TODO: Implementar análisis pesimista"

    return {"pessimistic_analysis": analysis}


def neutral_agent(state: AnalysisState) -> dict:
    """
    Agente que proporciona análisis balanceado.

    TODO: Implementar análisis neutral
    - Crear prompt para análisis objetivo
    - Balance de pros y contras
    - Retornar {"neutral_analysis": resultado}
    """
    print("\n😐 AGENTE NEUTRAL: Analizando...")
    review = state["review"]

    # Tu código aquí
    analysis = "TODO: Implementar análisis neutral"

    return {"neutral_analysis": analysis}


# =============================================================================
# NODO AGREGADOR
# =============================================================================

def aggregator_node(state: AnalysisState) -> dict:
    """
    Sintetiza las tres perspectivas en un análisis final.

    TODO: Implementar agregación
    - Recibir los tres análisis del estado
    - Crear prompt que sintetice las perspectivas
    - Identificar consenso y discrepancias
    - Retornar {"final_analysis": síntesis}

    Pista: El estado ya tiene optimistic_analysis, pessimistic_analysis, y neutral_analysis
    """
    print("\n🔄 AGREGADOR: Sintetizando perspectivas...")

    # Obtener los tres análisis
    opt = state["optimistic_analysis"]
    pes = state["pessimistic_analysis"]
    neu = state["neutral_analysis"]

    # Tu código aquí
    # Crear prompt que sintetice las tres perspectivas
    # Invocar el LLM
    final = "TODO: Implementar agregación"

    return {"final_analysis": final}


# =============================================================================
# CONSTRUCCIÓN DEL GRAFO
# =============================================================================

def build_graph():
    """
    Construye el grafo con paralelización.

    TODO: Implementar grafo paralelo
    - Agregar los 4 nodos (3 agentes + aggregator)
    - Configurar paralelismo: múltiples edges desde START a los agentes
    - Configurar agregación: todos los agentes → aggregator
    - Conectar aggregator → END

    Arquitectura:
                START
                  │
         ┌────────┼────────┐
         ▼        ▼        ▼
      [opt]    [pes]    [neu]  (PARALELO)
         │        │        │
         └────────┼────────┘
                  ▼
             [aggregator]
                  │
                 END
    """
    workflow = StateGraph(AnalysisState)

    # Tu código aquí
    # workflow.add_node(...)
    # workflow.set_entry_point(...)
    # workflow.add_edge(...)  # Para paralelismo, múltiples edges desde entry

    return workflow.compile()


# =============================================================================
# EJECUCIÓN
# =============================================================================

def main():
    print("\n" + "="*70)
    print("🔬 ANÁLISIS PARALELO MULTI-PERSPECTIVA")
    print("="*70)

    app = build_graph()

    # Reseñas de prueba
    reviews = [
        "El producto es excelente, muy buena calidad. El envío fue rápido. "
        "El único problema es que el manual está en inglés.",

        "Terrible experiencia. El producto llegó dañado y el soporte no responde. "
        "No lo recomiendo para nada.",

        "Es un producto decente. Tiene sus pros y contras. "
        "Funciona bien para el precio, pero podría mejorar en varios aspectos.",
    ]

    for i, review in enumerate(reviews, 1):
        print(f"\n{'='*70}")
        print(f"📝 RESEÑA {i}/{len(reviews)}")
        print('='*70)
        print(f"\n{review}")

        initial_state = {
            "review": review,
            "optimistic_analysis": "",
            "pessimistic_analysis": "",
            "neutral_analysis": "",
            "final_analysis": ""
        }

        final_state = app.invoke(initial_state)

        print(f"\n{'='*70}")
        print("📊 RESULTADOS")
        print('='*70)

        print(f"\n😊 Perspectiva Optimista:")
        print(final_state["optimistic_analysis"])

        print(f"\n😟 Perspectiva Pesimista:")
        print(final_state["pessimistic_analysis"])

        print(f"\n😐 Perspectiva Neutral:")
        print(final_state["neutral_analysis"])

        print(f"\n✨ ANÁLISIS FINAL (Sintetizado):")
        print(final_state["final_analysis"])

        if i < len(reviews):
            input("\n[Presiona Enter...]")

    print("\n" + "="*70)
    print("🎉 ¡Ejercicio completado!")
    print("="*70)


if __name__ == "__main__":
    main()
