"""
Sistema de Análisis Paralelo de Documentos
===========================================

Ejercicio 2.2: Demuestra el patrón de Paralelización con múltiples agentes.

Conceptos:
- Fan-out: Disparar múltiples nodos en paralelo
- Fan-in: Agregar resultados de múltiples nodos
- Send() API para ejecución concurrente
- Performance: Ejecutar en paralelo es MUCHO más rápido que secuencial

Este grafo se puede abrir en LangGraph Studio.
"""

from typing import TypedDict, List
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
import time


# =============================================================================
# State Definition
# =============================================================================

class AnalysisState(TypedDict):
    """Estado del análisis de documentos."""
    document: str           # Documento a analizar
    sentiment: str          # Análisis de sentimiento
    entities: List[str]     # Entidades extraídas
    summary: str            # Resumen del documento
    final_report: str       # Reporte final consolidado


# =============================================================================
# LLM Configuration
# =============================================================================

llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)


# =============================================================================
# Parallel Analyst Nodes
# =============================================================================

def sentiment_analyst(state: AnalysisState) -> dict:
    """
    Analista de Sentimiento.

    Determina el tono emocional del documento:
    - Positivo
    - Negativo
    - Neutral
    - Mixto
    """
    print('🎭 Analista de Sentimiento trabajando...')

    # Simular trabajo (en paralelo con otros analistas)
    time.sleep(0.5)

    prompt = f'''Analiza el sentimiento de este texto.

Texto: {state["document"]}

Instrucciones:
- Determina si el sentimiento general es: Positivo, Negativo, Neutral, o Mixto
- Proporciona una breve justificación (máximo 2 líneas)
- Formato: "SENTIMIENTO: [tu análisis]"'''

    response = llm.invoke(prompt)

    return {'sentiment': response.content}


def entity_analyst(state: AnalysisState) -> dict:
    """
    Analista de Entidades.

    Extrae entidades nombradas del documento:
    - Personas
    - Organizaciones
    - Lugares
    - Productos
    - Tecnologías
    """
    print('👤 Analista de Entidades trabajando...')

    # Simular trabajo (en paralelo con otros analistas)
    time.sleep(0.5)

    prompt = f'''Extrae las entidades principales de este texto.

Texto: {state["document"]}

Instrucciones:
- Identifica personas, organizaciones, productos, tecnologías mencionadas
- Lista solo las entidades MÁS importantes (máximo 5)
- Separa con comas
- Formato: "Entidad1, Entidad2, Entidad3"'''

    response = llm.invoke(prompt)

    # Convertir a lista
    entities_text = response.content.strip()
    entities_list = [e.strip() for e in entities_text.split(',') if e.strip()]

    return {'entities': entities_list}


def summary_analyst(state: AnalysisState) -> dict:
    """
    Analista de Resumen.

    Genera un resumen conciso del documento:
    - Idea principal
    - Puntos clave
    - Conclusión
    """
    print('📝 Analista de Resumen trabajando...')

    # Simular trabajo (en paralelo con otros analistas)
    time.sleep(0.5)

    prompt = f'''Resume este texto en 1-2 oraciones.

Texto: {state["document"]}

Instrucciones:
- Captura la idea principal
- Máximo 2 oraciones
- Claro y conciso'''

    response = llm.invoke(prompt)

    return {'summary': response.content}


# =============================================================================
# Fan-out and Aggregation Nodes
# =============================================================================

def fan_out(state: AnalysisState):
    """
    Fan-out: Dispara los 3 analistas EN PARALELO.

    Usa la Send() API para crear 3 ejecuciones paralelas:
    - Una para sentiment_analyst
    - Una para entity_analyst
    - Una para summary_analyst

    Esto es MUCHO más rápido que ejecutarlos secuencialmente.
    """
    print('\n⚡ FAN-OUT: Disparando 3 analistas en PARALELO...\n')

    # Send() crea ejecuciones paralelas
    return [
        Send('sentiment', state),
        Send('entities', state),
        Send('summary', state)
    ]


def aggregate(state: AnalysisState) -> dict:
    """
    Fan-in: Agrega todos los resultados en un reporte final.

    Espera a que TODOS los analistas terminen y luego consolida:
    - Sentimiento
    - Entidades
    - Resumen

    En un reporte final estructurado.
    """
    print('\n🔨 AGGREGATOR: Consolidando resultados...\n')

    # Construir reporte final
    report = f"""
╔════════════════════════════════════════════════════════════════╗
║                    REPORTE DE ANÁLISIS                          ║
╚════════════════════════════════════════════════════════════════╝

📄 DOCUMENTO:
{state.get('document', 'N/A')[:200]}...

🎭 SENTIMIENTO:
{state.get('sentiment', 'N/A')}

👤 ENTIDADES IDENTIFICADAS:
{', '.join(state.get('entities', [])) or 'Ninguna'}

📝 RESUMEN:
{state.get('summary', 'N/A')}

╚════════════════════════════════════════════════════════════════╝
"""

    return {'final_report': report}


# =============================================================================
# Graph Construction
# =============================================================================

def create_graph():
    """
    Construye el grafo de análisis paralelo.

    Arquitectura (ejecución PARALELA):

        START
          ↓
        fan_out
          ↓
        ┌─────────┬───────────┬─────────┐
        ↓         ↓           ↓         ↓
    sentiment  entities   summary    (en paralelo)
        ↓         ↓           ↓
        └─────────┴───────────┘
                  ↓
              aggregate
                  ↓
                END

    Returns:
        CompiledGraph: Grafo compilado listo para ejecutar
    """
    # 1. Crear el builder
    builder = StateGraph(AnalysisState)
    print("✅ StateGraph creado")

    # 2. Agregar nodos
    builder.add_node("sentiment", sentiment_analyst)
    builder.add_node("entities", entity_analyst)
    builder.add_node("summary", summary_analyst)
    builder.add_node("aggregate", aggregate)
    print("✅ Nodos agregados")

    # 3. Conectar edges
    # START → fan_out (dispara los 3 analistas EN PARALELO)
    builder.add_conditional_edges(START, fan_out)

    # Fan-in: Todos los analistas → aggregate
    builder.add_edge("sentiment", "aggregate")
    builder.add_edge("entities", "aggregate")
    builder.add_edge("summary", "aggregate")

    # aggregate → END
    builder.add_edge("aggregate", END)

    print("✅ Edges conectados (con paralelización)")

    # 4. Compilar
    graph = builder.compile()
    print("🎉 Grafo paralelo compilado exitosamente\n")

    return graph


# =============================================================================
# Create the graph (for LangGraph Studio)
# =============================================================================

graph = create_graph()


# =============================================================================
# Testing Function (optional)
# =============================================================================

def main():
    """
    Función de prueba con documentos de ejemplo.
    Mide el tiempo de ejecución para demostrar el beneficio de la paralelización.
    """
    print("="*70)
    print("⚡ Sistema de Análisis Paralelo de Documentos")
    print("="*70)

    # Documentos de prueba
    test_documents = [
        """LangGraph de LangChain es una herramienta excelente para construir sistemas
        multi-agente complejos. Permite crear workflows sofisticados con múltiples LLMs
        trabajando en conjunto. La comunidad está muy emocionada con sus capacidades.""",

        """El nuevo producto lanzado por TechCorp ha recibido críticas mixtas. Mientras
        algunos usuarios elogian su innovación, otros se quejan de problemas de rendimiento.
        La compañía prometió mejoras en la próxima versión.""",

        """El cambio climático continúa siendo uno de los mayores desafíos de nuestra era.
        Científicos de la ONU advierten sobre la necesidad de acción inmediata. Países como
        Noruega y Costa Rica están liderando iniciativas de energía renovable.""",
    ]

    for i, doc in enumerate(test_documents, 1):
        print(f"\n{'='*70}")
        print(f"TEST {i}/{len(test_documents)}")
        print(f"{'='*70}")

        # Medir tiempo de ejecución
        start_time = time.time()

        # Ejecutar análisis
        result = graph.invoke({
            'document': doc,
            'sentiment': '',
            'entities': [],
            'summary': '',
            'final_report': ''
        })

        elapsed_time = time.time() - start_time

        # Mostrar resultados
        print(result['final_report'])
        print(f"\n⏱️  TIEMPO DE EJECUCIÓN: {elapsed_time:.2f} segundos")
        print(f"\n💡 Los 3 analistas trabajaron EN PARALELO (mucho más rápido que secuencial)")
        print(f"\n{'='*70}\n")

    print("\n✅ Todos los análisis completados")

    # Estadísticas
    print(f"\n📊 ESTADÍSTICAS:")
    print(f"   Total de documentos analizados: {len(test_documents)}")
    print(f"   Analistas trabajando en paralelo: 3")
    print(f"   Tipos de análisis: Sentimiento, Entidades, Resumen")
    print(f"   Beneficio: ~3x más rápido que ejecución secuencial")


if __name__ == "__main__":
    main()
