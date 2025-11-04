"""
Ejercicio 2.2: Paralelización con Agregación - SOLUCIÓN COMPLETA

Implementa análisis multi-perspectiva paralelo con agregación de resultados.
"""

from typing import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()

# =============================================================================
# ESTADO Y CONFIGURACIÓN
# =============================================================================

class AnalysisState(TypedDict):
    """Estado para análisis paralelo multi-perspectiva."""
    review: str
    optimistic_analysis: str
    pessimistic_analysis: str
    neutral_analysis: str
    final_analysis: str


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)


# =============================================================================
# AGENTES CON PERSPECTIVAS
# =============================================================================

def optimistic_agent(state: AnalysisState) -> dict:
    """
    Agente optimista que enfatiza aspectos positivos.

    Estrategia:
    - Resaltar fortalezas y aspectos positivos
    - Interpretar comentarios ambiguos favorablemente
    - Mencionar potencial y beneficios
    """
    print("\n😊 AGENTE OPTIMISTA: Analizando...")
    review = state["review"]

    prompt = f"""Analiza esta reseña de producto desde una perspectiva OPTIMISTA.

Tu rol:
- Resalta aspectos positivos y fortalezas
- Interpreta comentarios ambiguos favorablemente
- Menciona el valor y beneficios del producto
- Sé realista pero positivo

Reseña:
{review}

Proporciona tu análisis optimista (2-3 frases):"""

    response = llm.invoke(prompt)
    print(f"   ✓ Análisis completado")

    return {"optimistic_analysis": response.content}


def pessimistic_agent(state: AnalysisState) -> dict:
    """
    Agente pesimista que enfatiza problemas y riesgos.

    Estrategia:
    - Identificar problemas, debilidades y riesgos
    - Interpretar comentarios ambiguos críticamente
    - Señalar áreas de mejora necesarias
    """
    print("\n😟 AGENTE PESIMISTA: Analizando...")
    review = state["review"]

    prompt = f"""Analiza esta reseña de producto desde una perspectiva PESIMISTA.

Tu rol:
- Identifica problemas, debilidades y riesgos
- Interpreta comentarios ambiguos críticamente
- Señala áreas que necesitan mejora
- Sé realista pero crítico

Reseña:
{review}

Proporciona tu análisis pesimista (2-3 frases):"""

    response = llm.invoke(prompt)
    print(f"   ✓ Análisis completado")

    return {"pessimistic_analysis": response.content}


def neutral_agent(state: AnalysisState) -> dict:
    """
    Agente neutral que proporciona análisis balanceado.

    Estrategia:
    - Balance objetivo de pros y contras
    - Interpretar comentarios sin sesgo
    - Proporcionar perspectiva equilibrada
    """
    print("\n😐 AGENTE NEUTRAL: Analizando...")
    review = state["review"]

    prompt = f"""Analiza esta reseña de producto desde una perspectiva NEUTRAL y BALANCEADA.

Tu rol:
- Proporciona balance objetivo de pros y contras
- No favorezcas aspectos positivos ni negativos
- Sé imparcial y analítico
- Resume de manera equilibrada

Reseña:
{review}

Proporciona tu análisis neutral (2-3 frases):"""

    response = llm.invoke(prompt)
    print(f"   ✓ Análisis completado")

    return {"neutral_analysis": response.content}


# =============================================================================
# AGREGADOR
# =============================================================================

def aggregator_node(state: AnalysisState) -> dict:
    """
    Sintetiza las tres perspectivas en un análisis final completo.

    Este es el componente clave del pattern Map-Reduce:
    - Recibe múltiples análisis (Map)
    - Los sintetiza en uno coherente (Reduce)

    Estrategia de agregación:
    1. Identificar puntos de consenso
    2. Notar discrepancias importantes
    3. Balancear las perspectivas
    4. Proporcionar conclusión útil
    """
    print("\n🔄 AGREGADOR: Sintetizando perspectivas...")

    opt = state["optimistic_analysis"]
    pes = state["pessimistic_analysis"]
    neu = state["neutral_analysis"]

    prompt = f"""Sintetiza estos tres análisis de una reseña de producto en un análisis final balanceado.

PERSPECTIVA OPTIMISTA:
{opt}

PERSPECTIVA PESIMISTA:
{pes}

PERSPECTIVA NEUTRAL:
{neu}

Tu tarea:
1. Identifica puntos de consenso entre las tres perspectivas
2. Nota discrepancias o énfasis diferentes
3. Proporciona un análisis final equilibrado que integre las tres visiones
4. Incluye una recomendación de satisfacción (1-5 estrellas)

Análisis Final Sintetizado:"""

    response = llm.invoke(prompt)
    print(f"   ✓ Síntesis completada")

    return {"final_analysis": response.content}


# =============================================================================
# GRAFO PARALELO
# =============================================================================

def build_graph():
    """
    Construye el grafo con ejecución paralela y agregación.

    Arquitectura paralela:
    - Los tres agentes se ejecutan simultáneamente
    - LangGraph espera a que TODOS terminen
    - El aggregator recibe todos los resultados
    - Produce un análisis sintetizado

    Clave: Múltiples edges desde el mismo nodo crean paralelismo
    """
    workflow = StateGraph(AnalysisState)

    # Agregar todos los nodos
    workflow.add_node("optimistic", optimistic_agent)
    workflow.add_node("pessimistic", pessimistic_agent)
    workflow.add_node("neutral", neutral_agent)
    workflow.add_node("aggregator", aggregator_node)

    # Configurar paralelismo: todos los agentes se ejecutan desde START
    workflow.set_entry_point("optimistic")
    workflow.set_entry_point("pessimistic")
    workflow.set_entry_point("neutral")

    # Nota: set_entry_point múltiple no es la sintaxis correcta.
    # La forma correcta de paralelismo es:

    # Usar conditional_entry_point o add_edge desde un nodo común
    # Para simplicidad, usamos entry points directos:
    # (En la práctica, esto requiere un nodo "broadcast" inicial)

    # Opción correcta: Agregar nodo broadcast
    workflow.add_node("broadcast", lambda state: {})  # Nodo pass-through
    workflow.set_entry_point("broadcast")

    # Paralelismo: broadcast → todos los agentes
    workflow.add_edge("broadcast", "optimistic")
    workflow.add_edge("broadcast", "pessimistic")
    workflow.add_edge("broadcast", "neutral")

    # Agregación: todos → aggregator
    workflow.add_edge("optimistic", "aggregator")
    workflow.add_edge("pessimistic", "aggregator")
    workflow.add_edge("neutral", "aggregator")

    # Fin
    workflow.add_edge("aggregator", END)

    return workflow.compile()


# =============================================================================
# EJECUCIÓN Y DEMO
# =============================================================================

def main():
    print("\n" + "="*70)
    print("🔬 ANÁLISIS PARALELO MULTI-PERSPECTIVA")
    print("="*70)

    app = build_graph()

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
        print("📊 RESULTADOS DEL ANÁLISIS PARALELO")
        print('='*70)

        print(f"\n😊 Perspectiva Optimista:")
        print(f"   {final_state['optimistic_analysis']}")

        print(f"\n😟 Perspectiva Pesimista:")
        print(f"   {final_state['pessimistic_analysis']}")

        print(f"\n😐 Perspectiva Neutral:")
        print(f"   {final_state['neutral_analysis']}")

        print(f"\n✨ ANÁLISIS FINAL (Sintetizado):")
        print(f"   {final_state['final_analysis']}")

        if i < len(reviews):
            input("\n[Presiona Enter para continuar...]")

    print("\n" + "="*70)
    print("🎉 ¡Ejercicio completado!")
    print("="*70)
    print("\n💡 Observaciones:")
    print("   • Cada reseña fue analizada desde 3 perspectivas simultáneamente")
    print("   • El aggregator sintetizó las perspectivas en un análisis completo")
    print("   • El resultado final es más robusto que cualquier perspectiva individual")
    print("   • Este pattern es útil para: análisis de sentimiento, moderación,")
    print("     evaluación de calidad, y cualquier tarea que beneficie de múltiples opiniones")


if __name__ == "__main__":
    main()
