"""
Ejercicio 2.3: Orchestrator-Workers Pattern - SOLUCIÓN COMPLETA

Implementa el pattern orchestrator-workers para análisis de documentos complejos.
"""

from typing import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()

# =============================================================================
# ESTADO Y CONFIGURACIÓN
# =============================================================================

class DocumentAnalysisState(TypedDict):
    """Estado para análisis orquestado de documentos."""
    document: str
    executive: str
    technical: str
    financial: str
    executive_analysis: str
    technical_analysis: str
    financial_analysis: str
    final_report: str


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)


# =============================================================================
# ORCHESTRATOR - PLANIFICACIÓN
# =============================================================================

def orchestrator_plan(state: DocumentAnalysisState) -> dict:
    """
    Orchestrator que divide el documento en secciones lógicas.

    Este es el primer paso del pattern: análisis y división.
    El orchestrator debe entender la estructura del documento
    y extraer las secciones relevantes para cada worker.
    """
    print("\n" + "="*70)
    print("🎯 ORCHESTRATOR: Planificando división del documento...")
    print("="*70)

    document = state["document"]

    # Extraer secciones usando la función helper
    sections = extract_sections_smart(document)

    print(f"✓ Documento dividido en 3 secciones:")
    print(f"   - Ejecutivo: {len(sections['executive'])} caracteres")
    print(f"   - Técnico: {len(sections['technical'])} caracteres")
    print(f"   - Financiero: {len(sections['financial'])} caracteres")

    return sections


# =============================================================================
# WORKERS ESPECIALIZADOS
# =============================================================================

def executive_summary_worker(state: DocumentAnalysisState) -> dict:
    """
    Worker especializado en análisis ejecutivo de alto nivel.
    """
    print("\n👔 WORKER EJECUTIVO: Analizando sección ejecutiva...")

    section = state["executive"]

    if not section or section == "Sin sección ejecutiva.":
        return {"executive_analysis": "No se encontró contenido ejecutivo para analizar."}

    prompt = f"""Como consultor ejecutivo senior, analiza esta sección de un documento:

{section}

Proporciona un análisis ejecutivo que incluya:
1. Puntos clave estratégicos
2. Decisiones críticas identificadas
3. Impacto para stakeholders
4. Recomendaciones de alto nivel

Análisis ejecutivo:"""

    response = llm.invoke(prompt)
    print(f"   ✓ Análisis completado ({len(response.content)} caracteres)")

    return {"executive_analysis": response.content}


def technical_details_worker(state: DocumentAnalysisState) -> dict:
    """
    Worker especializado en análisis técnico detallado.
    """
    print("\n🔧 WORKER TÉCNICO: Analizando sección técnica...")

    section = state["technical"]

    if not section or section == "Sin sección técnica.":
        return {"technical_analysis": "No se encontró contenido técnico para analizar."}

    prompt = f"""Como arquitecto técnico senior, analiza esta sección:

{section}

Proporciona un análisis técnico que incluya:
1. Especificaciones y tecnologías clave
2. Requisitos de arquitectura
3. Consideraciones de implementación
4. Riesgos técnicos y mitigaciones

Análisis técnico:"""

    response = llm.invoke(prompt)
    print(f"   ✓ Análisis completado ({len(response.content)} caracteres)")

    return {"technical_analysis": response.content}


def financial_analysis_worker(state: DocumentAnalysisState) -> dict:
    """
    Worker especializado en análisis financiero y de costos.
    """
    print("\n💰 WORKER FINANCIERO: Analizando sección financiera...")

    section = state["financial"]

    if not section or section == "Sin sección financiera.":
        return {"financial_analysis": "No se encontró contenido financiero para analizar."}

    prompt = f"""Como analista financiero, analiza esta sección:

{section}

Proporciona un análisis financiero que incluya:
1. Resumen de costos e inversiones
2. Análisis de ROI y beneficios
3. Riesgos financieros
4. Recomendaciones económicas

Análisis financiero:"""

    response = llm.invoke(prompt)
    print(f"   ✓ Análisis completado ({len(response.content)} caracteres)")

    return {"financial_analysis": response.content}


# =============================================================================
# ORCHESTRATOR - SÍNTESIS
# =============================================================================

def orchestrator_synthesize(state: DocumentAnalysisState) -> dict:
    """
    Orchestrator que ensambla los análisis parciales en un reporte coherente.

    Este es el segundo paso del pattern: integración y síntesis.
    El orchestrator debe crear un reporte unificado que:
    - Integre las tres perspectivas
    - Sea coherente y fluido
    - No pierda información crítica
    - Proporcione conclusiones integradas
    """
    print("\n" + "="*70)
    print("🔄 ORCHESTRATOR: Ensamblando reporte final...")
    print("="*70)

    exec_analysis = state["executive_analysis"]
    tech_analysis = state["technical_analysis"]
    fin_analysis = state["financial_analysis"]

    prompt = f"""Eres un consultor senior que debe crear un reporte ejecutivo integrando
estos tres análisis especializados de un proyecto:

═══ ANÁLISIS EJECUTIVO ═══
{exec_analysis}

═══ ANÁLISIS TÉCNICO ═══
{tech_analysis}

═══ ANÁLISIS FINANCIERO ═══
{fin_analysis}

Crea un REPORTE EJECUTIVO INTEGRADO que:
1. Comience con un resumen de 2-3 frases
2. Integre los hallazgos clave de cada área
3. Identifique interdependencias entre aspectos ejecutivos, técnicos y financieros
4. Proporcione recomendaciones integradas
5. Concluya con una valoración general del proyecto

El reporte debe ser coherente, profesional y ejecutivo (no técnico en exceso).

REPORTE EJECUTIVO INTEGRADO:"""

    response = llm.invoke(prompt)
    print(f"✓ Reporte final completado ({len(response.content)} caracteres)")

    return {"final_report": response.content}


# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def extract_sections_smart(document: str) -> dict:
    """
    Extrae secciones del documento usando clasificación por keywords.

    En un sistema de producción, considerarías:
    - Usar un LLM para clasificar cada párrafo
    - Embeddings para similaridad semántica
    - Análisis de estructura (headers, bullets, etc.)
    - Patrones de lenguaje específicos del dominio
    """
    paragraphs = [p.strip() for p in document.split("\n\n") if p.strip()]

    executive = []
    technical = []
    financial = []

    # Keywords para clasificación
    executive_keywords = [
        "resumen", "ejecutivo", "overview", "estrategia", "objetivo",
        "visión", "iniciativa", "propone", "proyecto"
    ]

    technical_keywords = [
        "técnico", "sistema", "arquitectura", "implementación",
        "api", "base de datos", "tecnología", "desarrollo",
        "infraestructura", "monitoreo"
    ]

    financial_keywords = [
        "costo", "precio", "inversión", "financiero", "presupuesto",
        "roi", "ahorro", "económico", "usd", "$"
    ]

    for para in paragraphs:
        para_lower = para.lower()

        # Contar matches de cada categoría
        exec_score = sum(1 for kw in executive_keywords if kw in para_lower)
        tech_score = sum(1 for kw in technical_keywords if kw in para_lower)
        fin_score = sum(1 for kw in financial_keywords if kw in para_lower)

        # Asignar a la categoría con mayor score
        if exec_score >= tech_score and exec_score >= fin_score:
            executive.append(para)
        elif tech_score >= fin_score:
            technical.append(para)
        else:
            financial.append(para)

    return {
        "executive": "\n\n".join(executive) if executive else "Sin sección ejecutiva.",
        "technical": "\n\n".join(technical) if technical else "Sin sección técnica.",
        "financial": "\n\n".join(financial) if financial else "Sin sección financiera."
    }


# =============================================================================
# CONSTRUCCIÓN DEL GRAFO
# =============================================================================

def build_graph():
    """
    Construye el grafo orchestrator-workers.

    Arquitectura "diamante":
    - Orchestrator de planificación divide el trabajo
    - Workers especializados procesan en paralelo
    - Orchestrator de síntesis ensambla los resultados
    """
    workflow = StateGraph(DocumentAnalysisState)

    # Agregar nodos
    workflow.add_node("orchestrator_plan", orchestrator_plan)
    workflow.add_node("executive_worker", executive_summary_worker)
    workflow.add_node("technical_worker", technical_details_worker)
    workflow.add_node("financial_worker", financial_analysis_worker)
    workflow.add_node("orchestrator_synthesize", orchestrator_synthesize)

    # Entry point: orchestrator de planificación
    workflow.set_entry_point("orchestrator_plan")

    # Paralelismo: del orchestrator a los workers
    workflow.add_edge("orchestrator_plan", "executive_worker")
    workflow.add_edge("orchestrator_plan", "technical_worker")
    workflow.add_edge("orchestrator_plan", "financial_worker")

    # Convergencia: de los workers al orchestrator de síntesis
    workflow.add_edge("executive_worker", "orchestrator_synthesize")
    workflow.add_edge("technical_worker", "orchestrator_synthesize")
    workflow.add_edge("financial_worker", "orchestrator_synthesize")

    # Fin
    workflow.add_edge("orchestrator_synthesize", END)

    return workflow.compile()


# =============================================================================
# EJECUCIÓN Y DEMO
# =============================================================================

def main():
    print("\n" + "="*70)
    print("🎭 ORCHESTRATOR-WORKERS: Análisis de Documentos")
    print("="*70)

    document = """
Resumen Ejecutivo

Este proyecto propone la implementación de un sistema de automatización
inteligente para mejorar la eficiencia operativa. La iniciativa estratégica
busca reducir costos y mejorar la experiencia del cliente mediante IA.
El objetivo es transformar digitalmente los procesos clave del negocio.

Detalles Técnicos

El sistema estará basado en una arquitectura de microservicios con
contenedores Docker. La implementación incluirá:
- API REST con autenticación OAuth2
- Base de datos PostgreSQL con replicación
- Cola de mensajes con RabbitMQ
- Monitoreo con Prometheus y Grafana
- Despliegue en Kubernetes para alta disponibilidad

Análisis Financiero

La inversión inicial estimada es de $250,000 USD, distribuidos en:
- Desarrollo: $150,000
- Infraestructura: $50,000
- Capacitación: $30,000
- Contingencia: $20,000

El ROI proyectado es de 18 meses, con ahorros anuales estimados de $200,000
por reducción de costos operativos y mejora de eficiencia. El análisis
de costo-beneficio muestra un retorno positivo en el primer año.
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
    print("📊 ANÁLISIS POR SECCIÓN (Workers Especializados)")
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
    print("📋 REPORTE FINAL INTEGRADO (Orchestrator Synthesis)")
    print("="*70)
    print(final_state["final_report"])

    print("\n" + "="*70)
    print("🎉 ¡Ejercicio completado!")
    print("="*70)
    print("\n💡 Observaciones:")
    print("   • El orchestrator dividió el documento inteligentemente")
    print("   • Cada worker analizó con expertise específico")
    print("   • El reporte final integra las tres perspectivas")
    print("   • Este pattern escala: puedes agregar más workers fácilmente")


if __name__ == "__main__":
    main()
