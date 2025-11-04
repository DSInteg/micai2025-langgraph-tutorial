"""
Ejercicio 4.3: Asistente de Investigación - SOLUCIÓN COMPLETA
"""

from typing import TypedDict, List, Dict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()

class ResearchState(TypedDict):
    topic: str
    research_plan: str
    web_findings: List[Dict]
    doc_findings: List[Dict]
    analysis: str
    report: str
    confidence: float
    validated: bool

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

def planner_node(state: ResearchState) -> dict:
    """Crea plan de investigación."""
    print(f"\n📋 PLANNER: Planificando investigación sobre '{state['topic']}'...")

    prompt = f"""Crea un plan de investigación para:

TEMA: {state['topic']}

Genera plan con:
1. Sub-temas clave a investigar
2. Preguntas específicas
3. Fuentes sugeridas

PLAN DE INVESTIGACIÓN:"""

    response = llm.invoke(prompt)
    print(f"   ✓ Plan creado")

    return {"research_plan": response.content}

def web_researcher(state: ResearchState) -> dict:
    """Simula búsqueda web."""
    print("\n🌐 WEB RESEARCHER: Buscando información online...")

    prompt = f"""Simula búsqueda web sobre:

TEMA: {state['topic']}
PLAN: {state['research_plan'][:300]}

Genera 3-5 hallazgos simulados con fuentes.

HALLAZGOS WEB:"""

    response = llm.invoke(prompt)

    findings = [{
        "source": "web",
        "content": response.content,
        "relevance": "high"
    }]

    print(f"   ✓ {len(findings)} hallazgos web")

    return {"web_findings": findings}

def doc_researcher(state: ResearchState) -> dict:
    """Simula búsqueda en documentos."""
    print("\n📚 DOCUMENT RESEARCHER: Buscando en documentos...")

    prompt = f"""Simula búsqueda en documentos internos sobre:

TEMA: {state['topic']}
PLAN: {state['research_plan'][:300]}

Genera 2-3 hallazgos de documentos.

HALLAZGOS DOCUMENTOS:"""

    response = llm.invoke(prompt)

    findings = [{
        "source": "documents",
        "content": response.content,
        "relevance": "medium"
    }]

    print(f"   ✓ {len(findings)} hallazgos documentales")

    return {"doc_findings": findings}

def analyzer_node(state: ResearchState) -> dict:
    """Analiza todos los hallazgos."""
    print("\n📊 ANALYZER: Analizando hallazgos...")

    all_findings = state.get("web_findings", []) + state.get("doc_findings", [])

    findings_text = "\n\n".join([
        f"[{f['source'].upper()}] {f['content'][:300]}..."
        for f in all_findings
    ])

    prompt = f"""Analiza estos hallazgos de investigación:

TEMA: {state['topic']}

HALLAZGOS:
{findings_text}

Genera análisis con:
1. Insights clave
2. Patrones identificados
3. Gaps de información

ANÁLISIS:"""

    response = llm.invoke(prompt)
    print(f"   ✓ Análisis completado")

    return {"analysis": response.content}

def synthesizer_node(state: ResearchState) -> dict:
    """Genera reporte ejecutivo."""
    print("\n📝 SYNTHESIZER: Generando reporte...")

    prompt = f"""Genera reporte ejecutivo de investigación:

TEMA: {state['topic']}
PLAN: {state['research_plan'][:200]}
ANÁLISIS: {state['analysis'][:500]}

Estructura del reporte:
1. RESUMEN EJECUTIVO (2-3 párrafos)
2. HALLAZGOS CLAVE (bullet points)
3. RECOMENDACIONES
4. CONCLUSIONES

REPORTE:"""

    response = llm.invoke(prompt)
    print(f"   ✓ Reporte generado ({len(response.content)} caracteres)")

    return {"report": response.content}

def validator_node(state: ResearchState) -> dict:
    """Valida calidad del reporte."""
    print("\n✅ VALIDATOR: Verificando calidad...")

    confidence = 1.0

    # Verificar plan
    if not state.get("research_plan") or len(state["research_plan"]) < 100:
        confidence -= 0.2

    # Verificar findings
    total_findings = len(state.get("web_findings", [])) + len(state.get("doc_findings", []))
    if total_findings < 2:
        confidence -= 0.3

    # Verificar análisis
    if not state.get("analysis") or len(state["analysis"]) < 200:
        confidence -= 0.2

    # Verificar reporte
    if not state.get("report") or len(state["report"]) < 500:
        confidence -= 0.2

    validated = confidence >= 0.7

    print(f"   → Confidence: {confidence:.2f}")
    print(f"   → Status: {'✅ APPROVED' if validated else '❌ NEEDS REVIEW'}")

    return {
        "confidence": confidence,
        "validated": validated
    }

def build_graph():
    """Construye pipeline de investigación."""
    workflow = StateGraph(ResearchState)

    workflow.add_node("planner", planner_node)
    workflow.add_node("web_research", web_researcher)
    workflow.add_node("doc_research", doc_researcher)
    workflow.add_node("analyzer", analyzer_node)
    workflow.add_node("synthesizer", synthesizer_node)
    workflow.add_node("validator", validator_node)

    workflow.set_entry_point("planner")

    # Paralelo: 2 researchers
    workflow.add_edge("planner", "web_research")
    workflow.add_edge("planner", "doc_research")

    # Convergencia
    workflow.add_edge("web_research", "analyzer")
    workflow.add_edge("doc_research", "analyzer")

    # Secuencial
    workflow.add_edge("analyzer", "synthesizer")
    workflow.add_edge("synthesizer", "validator")
    workflow.add_edge("validator", END)

    return workflow.compile()

def main():
    print("="*70)
    print("🔬 ASISTENTE DE INVESTIGACIÓN EMPRESARIAL")
    print("="*70)

    topics = [
        "Adopción de IA en el sector salud",
        "Tendencias de trabajo remoto post-pandemia"
    ]

    app = build_graph()

    for i, topic in enumerate(topics, 1):
        print(f"\n{'='*70}")
        print(f"📊 INVESTIGACIÓN {i}: {topic}")
        print(f"{'='*70}")

        initial_state = {
            "topic": topic,
            "research_plan": "",
            "web_findings": [],
            "doc_findings": [],
            "analysis": "",
            "report": "",
            "confidence": 0.0,
            "validated": False
        }

        final_state = app.invoke(initial_state)

        print("\n" + "="*70)
        print("📄 REPORTE FINAL")
        print("="*70)
        print(final_state["report"][:500] + "...")

        print(f"\n📈 Métricas:")
        print(f"   • Confidence: {final_state['confidence']:.2f}")
        print(f"   • Validated: {final_state['validated']}")
        print(f"   • Web findings: {len(final_state['web_findings'])}")
        print(f"   • Doc findings: {len(final_state['doc_findings'])}")

        if i < len(topics):
            input("\n[Presiona Enter para siguiente...]")

if __name__ == "__main__":
    main()
