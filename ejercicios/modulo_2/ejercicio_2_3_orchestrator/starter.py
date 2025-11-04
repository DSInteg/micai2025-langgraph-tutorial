"""
Ejercicio 2.3: Orchestrator-Workers Pattern

Este módulo implementa un sistema que:
- Divide documentos complejos en secciones
- Asigna cada sección a un worker especializado
- Ensambla los análisis en un reporte coherente

Conceptos clave:
- Pattern Orchestrator-Workers
- División de problemas complejos
- Coordinación centralizada
- Ensamblaje de resultados parciales
"""

from typing import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()

# =============================================================================
# DEFINICIÓN DEL ESTADO
# =============================================================================

class DocumentAnalysisState(TypedDict):
    """
    Estado para análisis orquestado de documentos.

    Flujo:
    1. document: Input original
    2. Orchestrator identifica: executive, technical, financial
    3. Workers analizan sus secciones
    4. Orchestrator ensambla: final_report
    """
    document: str
    executive: str
    technical: str
    financial: str
    executive_analysis: str
    technical_analysis: str
    financial_analysis: str
    final_report: str


# =============================================================================
# CONFIGURACIÓN
# =============================================================================

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)


# =============================================================================
# ORCHESTRATOR - PLANIFICACIÓN
# =============================================================================

def orchestrator_plan(state: DocumentAnalysisState) -> dict:
    """
    Orchestrator que divide el documento en secciones.

    TODO: Implementar división del documento
    - Analizar el documento para identificar secciones
    - Extraer texto de cada sección
    - Retornar {"executive": ..., "technical": ..., "financial": ...}

    Estrategia simple:
    - Buscar keywords para identificar secciones
    - O usar el LLM para clasificar párrafos
    - Agrupar contenido relacionado
    """
    print("\n" + "="*70)
    print("🎯 ORCHESTRATOR: Planificando división del documento...")
    print("="*70)

    document = state["document"]

    # TODO: Tu código aquí
    # Dividir el documento en secciones
    # Pista: Puedes usar párrafos, keywords, o análisis con LLM

    executive = "TODO: Extraer sección ejecutiva"
    technical = "TODO: Extraer sección técnica"
    financial = "TODO: Extraer sección financiera"

    print(f"✓ Documento dividido en 3 secciones")
    return {
        "executive": executive,
        "technical": technical,
        "financial": financial
    }


# =============================================================================
# WORKERS ESPECIALIZADOS
# =============================================================================

def executive_summary_worker(state: DocumentAnalysisState) -> dict:
    """
    Worker especializado en análisis ejecutivo.

    TODO: Implementar análisis ejecutivo
    - Leer state["executive"]
    - Analizar desde perspectiva ejecutiva
    - Retornar {"executive_analysis": análisis}

    Enfoque:
    - Puntos clave y decisiones
    - Recomendaciones de alto nivel
    - Impacto estratégico
    """
    print("\n👔 WORKER EJECUTIVO: Analizando...")

    section = state["executive"]

    # TODO: Tu código aquí
    analysis = "TODO: Análisis ejecutivo"

    print(f"   ✓ Análisis completado")
    return {"executive_analysis": analysis}


def technical_details_worker(state: DocumentAnalysisState) -> dict:
    """
    Worker especializado en detalles técnicos.

    TODO: Implementar análisis técnico
    - Leer state["technical"]
    - Analizar desde perspectiva técnica
    - Retornar {"technical_analysis": análisis}

    Enfoque:
    - Especificaciones y requisitos
    - Consideraciones de implementación
    - Riesgos técnicos
    """
    print("\n🔧 WORKER TÉCNICO: Analizando...")

    section = state["technical"]

    # TODO: Tu código aquí
    analysis = "TODO: Análisis técnico"

    print(f"   ✓ Análisis completado")
    return {"technical_analysis": analysis}


def financial_analysis_worker(state: DocumentAnalysisState) -> dict:
    """
    Worker especializado en análisis financiero.

    TODO: Implementar análisis financiero
    - Leer state["financial"]
    - Analizar desde perspectiva financiera
    - Retornar {"financial_analysis": análisis}

    Enfoque:
    - Costos e inversiones
    - ROI y beneficios económicos
    - Riesgos financieros
    """
    print("\n💰 WORKER FINANCIERO: Analizando...")

    section = state["financial"]

    # TODO: Tu código aquí
    analysis = "TODO: Análisis financiero"

    print(f"   ✓ Análisis completado")
    return {"financial_analysis": analysis}


# =============================================================================
# ORCHESTRATOR - SÍNTESIS
# =============================================================================

def orchestrator_synthesize(state: DocumentAnalysisState) -> dict:
    """
    Orchestrator que ensambla los análisis parciales.

    TODO: Implementar ensamblaje
    - Recibir los tres análisis del estado
    - Crear un reporte coherente que integre todo
    - Retornar {"final_report": reporte}

    El reporte debe:
    - Ser coherente y fluido
    - Integrar las tres perspectivas
    - No perder información importante
    - Proporcionar conclusiones integradas
    """
    print("\n" + "="*70)
    print("🔄 ORCHESTRATOR: Ensamblando reporte final...")
    print("="*70)

    exec_analysis = state["executive_analysis"]
    tech_analysis = state["technical_analysis"]
    fin_analysis = state["financial_analysis"]

    # TODO: Tu código aquí
    # Crear prompt que sintetice los tres análisis
    # Invocar el LLM
    # Retornar el reporte final

    final_report = "TODO: Reporte final sintetizado"

    print(f"✓ Reporte final completado")
    return {"final_report": final_report}


# =============================================================================
# CONSTRUCCIÓN DEL GRAFO
# =============================================================================

def build_graph():
    """
    Construye el grafo orchestrator-workers.

    TODO: Implementar grafo
    - Agregar orchestrator_plan como entry point
    - Agregar los tres workers
    - Agregar orchestrator_synthesize
    - Conectar: plan → workers → synthesize

    Arquitectura:
        orchestrator_plan
              │
         ┌────┼────┐
         ▼    ▼    ▼
      [exec][tech][fin]  (Paralelo)
         │    │    │
         └────┼────┘
              ▼
      orchestrator_synthesize
              │
             END
    """
    workflow = StateGraph(DocumentAnalysisState)

    # TODO: Tu código aquí
    # workflow.add_node(...)
    # workflow.set_entry_point(...)
    # workflow.add_edge(...)  # Para paralelismo

    return workflow.compile()


# =============================================================================
# FUNCIÓN AUXILIAR PARA DIVIDIR DOCUMENTOS
# =============================================================================

def extract_sections(document: str) -> dict:
    """
    Función helper para extraer secciones de un documento.

    Estrategia simple: dividir por párrafos y clasificar.
    En un sistema real, usarías técnicas más sofisticadas.
    """
    paragraphs = document.split("\n\n")

    executive = []
    technical = []
    financial = []

    for para in paragraphs:
        para_lower = para.lower()

        # Clasificación simple por keywords
        if any(word in para_lower for word in ["resumen", "overview", "ejecutivo", "estrategia"]):
            executive.append(para)
        elif any(word in para_lower for word in ["técnico", "implementación", "arquitectura", "sistema"]):
            technical.append(para)
        elif any(word in para_lower for word in ["costo", "precio", "inversión", "financiero", "roi"]):
            financial.append(para)
        else:
            # Si no está claro, agregarlo a ejecutivo por default
            executive.append(para)

    return {
        "executive": "\n\n".join(executive) if executive else "Sin sección ejecutiva.",
        "technical": "\n\n".join(technical) if technical else "Sin sección técnica.",
        "financial": "\n\n".join(financial) if financial else "Sin sección financiera."
    }


# =============================================================================
# EJECUCIÓN
# =============================================================================

def main():
    print("\n" + "="*70)
    print("🎭 ORCHESTRATOR-WORKERS: Análisis de Documentos")
    print("="*70)

    # Documento de ejemplo: Propuesta de proyecto
    document = """
Resumen Ejecutivo

Este proyecto propone la implementación de un sistema de automatización
inteligente para mejorar la eficiencia operativa. La iniciativa estratégica
busca reducir costos y mejorar la experiencia del cliente mediante IA.

Detalles Técnicos

El sistema estará basado en una arquitectura de microservicios con
contenedores Docker. La implementación incluirá:
- API REST con autenticación OAuth2
- Base de datos PostgreSQL con replicación
- Cola de mensajes con RabbitMQ
- Monitoreo con Prometheus y Grafana

Análisis Financiero

La inversión inicial estimada es de $250,000 USD, distribuidos en:
- Desarrollo: $150,000
- Infraestructura: $50,000
- Capacitación: $30,000
- Contingencia: $20,000

El ROI proyectado es de 18 meses, con ahorros anuales estimados de $200,000
por reducción de costos operativos y mejora de eficiencia.
"""

    app = build_graph()

    initial_state = {
        "document": document,
        "executive": "",
        "technical": "",
        "financial": "",
        "executive_analysis": "",
        "technical_analysis": "",
        "financial_analysis": "",
        "final_report": ""
    }

    print("\n📄 DOCUMENTO ORIGINAL:")
    print("-" * 70)
    print(document.strip())

    print("\n⚙️  Ejecutando análisis orquestado...")

    final_state = app.invoke(initial_state)

    print("\n" + "="*70)
    print("📊 ANÁLISIS POR SECCIÓN")
    print("="*70)

    print("\n👔 ANÁLISIS EJECUTIVO:")
    print("-" * 70)
    print(final_state["executive_analysis"])

    print("\n🔧 ANÁLISIS TÉCNICO:")
    print("-" * 70)
    print(final_state["technical_analysis"])

    print("\n💰 ANÁLISIS FINANCIERO:")
    print("-" * 70)
    print(final_state["financial_analysis"])

    print("\n" + "="*70)
    print("📋 REPORTE FINAL INTEGRADO")
    print("="*70)
    print(final_state["final_report"])

    print("\n" + "="*70)
    print("🎉 ¡Ejercicio completado!")
    print("="*70)


if __name__ == "__main__":
    main()
