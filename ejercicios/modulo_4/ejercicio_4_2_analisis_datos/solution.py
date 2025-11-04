"""
Ejercicio 4.2: Pipeline de Análisis de Documentos - SOLUCIÓN COMPLETA
Pipeline multi-etapa con paralelización para análisis de documentos.
"""

from typing import TypedDict, List, Dict, Annotated, Literal
from operator import add
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
import re

load_dotenv()

class DocumentAnalysisState(TypedDict):
    document_text: str
    document_type: str
    cleaned_text: str
    sections: Dict[str, str]
    metadata: Dict
    financial_analysis: Dict
    risk_analysis: Dict
    legal_analysis: Dict
    obligations_analysis: Dict
    combined_insights: Annotated[List[Dict], add]
    executive_summary: str
    validation_results: Dict
    confidence_score: float
    requires_human_review: bool
    review_reasons: List[str]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

# ============= PREPROCESSING =============
def preprocess_node(state: DocumentAnalysisState) -> dict:
    print("\n📄 PREPROCESSING: Preparando documento...")
    text = state["document_text"]

    # Limpiar
    cleaned = text.strip()

    # Detectar secciones
    sections = {}
    section_keywords = ["SCOPE", "PAYMENT", "TERM", "TERMINATION", "LIABILITY", "PARTIES"]
    lines = text.split('\n')
    current_section = "PREAMBLE"
    current_content = []

    for line in lines:
        line_upper = line.strip().upper()
        is_section = False
        for keyword in section_keywords:
            if keyword in line_upper and len(line.strip()) < 50:
                if current_content:
                    sections[current_section] = '\n'.join(current_content)
                current_section = keyword
                current_content = []
                is_section = True
                break
        if not is_section:
            current_content.append(line)

    if current_content:
        sections[current_section] = '\n'.join(current_content)

    # Metadata
    metadata = {}
    date_pattern = r'\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2}'
    dates = re.findall(date_pattern, text)
    metadata["dates"] = dates[:5]

    money_pattern = r'\$\s*[\d,]+(?:\.\d{2})?'
    amounts = re.findall(money_pattern, text)
    metadata["amounts"] = amounts[:10]

    print(f"   ✓ Secciones detectadas: {len(sections)}")
    print(f"   ✓ Metadata extraída: {len(metadata['dates'])} fechas, {len(metadata['amounts'])} montos")

    return {
        "cleaned_text": cleaned,
        "sections": sections,
        "metadata": metadata
    }

# ============= ANALISTAS PARALELOS =============
def financial_analyst(state: DocumentAnalysisState) -> dict:
    print("\n💰 FINANCIAL ANALYST...")

    text = state["cleaned_text"][:2000]
    sections = state["sections"]

    prompt = f"""Analiza aspectos financieros:

DOCUMENTO:
{text}

SECCIONES: {list(sections.keys())}

Extrae:
1. Montos totales y desglose
2. Términos de pago
3. Penalizaciones financieras
4. Riesgos financieros

Genera análisis en JSON format.

ANÁLISIS FINANCIERO:"""

    response = llm.invoke(prompt)

    return {
        "financial_analysis": {"content": response.content},
        "combined_insights": [{"type": "financial", "summary": response.content[:200]}]
    }

def risk_analyst(state: DocumentAnalysisState) -> dict:
    print("\n⚠️  RISK ANALYST...")

    text = state["cleaned_text"][:2000]

    prompt = f"""Identifica riesgos:

DOCUMENTO:
{text}

Analiza:
1. Riesgos legales
2. Riesgos operacionales
3. Riesgos financieros
4. Nivel de exposición

ANÁLISIS DE RIESGOS:"""

    response = llm.invoke(prompt)

    return {
        "risk_analysis": {"content": response.content},
        "combined_insights": [{"type": "risk", "summary": response.content[:200]}]
    }

def legal_analyst(state: DocumentAnalysisState) -> dict:
    print("\n⚖️  LEGAL ANALYST...")

    text = state["cleaned_text"][:2000]

    prompt = f"""Analiza aspectos legales:

DOCUMENTO:
{text}

Identifica:
1. Cláusulas críticas
2. Jurisdicción
3. Resolución de disputas
4. Compliance

ANÁLISIS LEGAL:"""

    response = llm.invoke(prompt)

    return {
        "legal_analysis": {"content": response.content},
        "combined_insights": [{"type": "legal", "summary": response.content[:200]}]
    }

def obligations_analyst(state: DocumentAnalysisState) -> dict:
    print("\n📋 OBLIGATIONS ANALYST...")

    text = state["cleaned_text"][:2000]

    prompt = f"""Analiza obligaciones:

DOCUMENTO:
{text}

Identifica:
1. Obligaciones de cada parte
2. Entregables y deadlines
3. Condiciones
4. Consecuencias de incumplimiento

ANÁLISIS DE OBLIGACIONES:"""

    response = llm.invoke(prompt)

    return {
        "obligations_analysis": {"content": response.content},
        "combined_insights": [{"type": "obligations", "summary": response.content[:200]}]
    }

# ============= AGGREGATION =============
def aggregator_node(state: DocumentAnalysisState) -> dict:
    print(f"\n🔄 AGGREGATOR: Integrando {len(state['combined_insights'])} análisis...")

    insights_text = "\n\n".join([
        f"{insight['type'].upper()}:\n{insight['summary']}"
        for insight in state["combined_insights"]
    ])

    prompt = f"""Sintetiza estos análisis en un resumen ejecutivo:

{insights_text}

Genera un RESUMEN EJECUTIVO que:
1. Integre todos los hallazgos
2. Priorice por criticidad
3. Sea ejecutivo y accionable

RESUMEN EJECUTIVO:"""

    response = llm.invoke(prompt)

    return {"executive_summary": response.content}

# ============= VALIDATION =============
def validator_node(state: DocumentAnalysisState) -> dict:
    print("\n✓ VALIDATOR: Verificando calidad...")

    confidence = 1.0
    review_reasons = []

    # Verificar análisis
    analyses = [
        state.get("financial_analysis"),
        state.get("risk_analysis"),
        state.get("legal_analysis"),
        state.get("obligations_analysis")
    ]

    completed = sum(1 for a in analyses if a and a.get("content"))
    if completed < 4:
        confidence -= 0.3
        review_reasons.append(f"Solo {completed}/4 análisis completados")

    # Verificar resumen
    summary = state.get("executive_summary", "")
    if len(summary) < 100:
        confidence -= 0.2
        review_reasons.append("Resumen ejecutivo muy corto")

    # Verificar metadata
    if not state.get("metadata", {}).get("amounts"):
        confidence -= 0.1
        review_reasons.append("No se detectaron montos financieros")

    requires_review = confidence < 0.7 or len(review_reasons) > 2

    print(f"   → Confidence: {confidence:.2f}")
    print(f"   → Revisión requerida: {'SÍ' if requires_review else 'NO'}")

    return {
        "confidence_score": confidence,
        "requires_human_review": requires_review,
        "review_reasons": review_reasons,
        "validation_results": {
            "completed_analyses": completed,
            "summary_length": len(summary),
            "metadata_extracted": bool(state.get("metadata"))
        }
    }

def approve_node(state: DocumentAnalysisState) -> dict:
    print("\n✅ ANÁLISIS APROBADO")
    return {}

def review_node(state: DocumentAnalysisState) -> dict:
    print("\n🔍 REQUIERE REVISIÓN HUMANA")
    print(f"Razones: {', '.join(state['review_reasons'])}")
    return {}

# ============= ROUTING =============
def route_after_validation(state: DocumentAnalysisState) -> Literal["approve", "review"]:
    return "review" if state["requires_human_review"] else "approve"

# ============= GRAFO =============
def build_graph():
    workflow = StateGraph(DocumentAnalysisState)

    workflow.add_node("preprocess", preprocess_node)
    workflow.add_node("financial", financial_analyst)
    workflow.add_node("risk", risk_analyst)
    workflow.add_node("legal", legal_analyst)
    workflow.add_node("obligations", obligations_analyst)
    workflow.add_node("aggregator", aggregator_node)
    workflow.add_node("validator", validator_node)
    workflow.add_node("approve", approve_node)
    workflow.add_node("review", review_node)

    workflow.set_entry_point("preprocess")

    # Paralelo
    workflow.add_edge("preprocess", "financial")
    workflow.add_edge("preprocess", "risk")
    workflow.add_edge("preprocess", "legal")
    workflow.add_edge("preprocess", "obligations")

    # Convergencia
    workflow.add_edge("financial", "aggregator")
    workflow.add_edge("risk", "aggregator")
    workflow.add_edge("legal", "aggregator")
    workflow.add_edge("obligations", "aggregator")

    workflow.add_edge("aggregator", "validator")

    workflow.add_conditional_edges(
        "validator",
        route_after_validation,
        {"approve": "approve", "review": "review"}
    )

    workflow.add_edge("approve", END)
    workflow.add_edge("review", END)

    return workflow.compile()

# ============= MAIN =============
def main():
    print("="*70)
    print("📊 PIPELINE DE ANÁLISIS DE DOCUMENTOS")
    print("="*70)

    sample_doc = """
SERVICE AGREEMENT

This agreement is entered into on March 1, 2024, between TechCorp Inc.
("Client") and DevSolutions LLC ("Provider").

SCOPE OF WORK:
Provider will develop a custom web application according to specifications.

PAYMENT TERMS:
Total contract value: $150,000 USD
- Milestone 1: $50,000 due March 31, 2024
- Milestone 2: $50,000 due June 30, 2024
- Milestone 3: $50,000 due September 30, 2024

Late payment penalty: 1.5% monthly interest

TERM:
Effective from March 1, 2024 to December 31, 2024.

TERMINATION:
Either party may terminate with 30 days notice.
Early termination penalty: 20% of remaining contract value.

LIABILITY:
Provider's liability is limited to the total contract value.
"""

    initial_state = {
        "document_text": sample_doc,
        "document_type": "contract",
        "cleaned_text": "",
        "sections": {},
        "metadata": {},
        "financial_analysis": {},
        "risk_analysis": {},
        "legal_analysis": {},
        "obligations_analysis": {},
        "combined_insights": [],
        "executive_summary": "",
        "validation_results": {},
        "confidence_score": 0.0,
        "requires_human_review": False,
        "review_reasons": []
    }

    app = build_graph()
    final_state = app.invoke(initial_state)

    print("\n" + "="*70)
    print("📋 RESUMEN EJECUTIVO")
    print("="*70)
    print(final_state["executive_summary"])

    print("\n" + "="*70)
    print("📊 MÉTRICAS")
    print("="*70)
    print(f"Confidence: {final_state['confidence_score']:.2f}")
    print(f"Secciones: {len(final_state['sections'])}")
    print(f"Insights: {len(final_state['combined_insights'])}")
    print(f"Revisión: {'✅ Aprobado' if not final_state['requires_human_review'] else '🔍 Requiere revisión'}")

if __name__ == "__main__":
    main()
