"""
Ejercicio 4.2: Pipeline de Análisis de Documentos - STARTER

Pipeline multi-etapa con paralelización para análisis de documentos.
"""

from typing import TypedDict, List, Dict, Annotated, Literal
from operator import add
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
import re

load_dotenv()

# =============================================================================
# ESTADO DEL PIPELINE
# =============================================================================

class DocumentAnalysisState(TypedDict):
    """
    Estado del pipeline de análisis.

    Usa Annotated con reducers para campos que múltiples nodos actualizan.
    """
    # TODO: Define los campos
    # Input
    # - document_text: str
    # - document_type: str
    #
    # Preprocessing
    # - cleaned_text: str
    # - sections: Dict[str, str]
    # - metadata: Dict
    #
    # Análisis (paralelos)
    # - financial_analysis: Dict
    # - risk_analysis: Dict
    # - legal_analysis: Dict
    # - obligations_analysis: Dict
    #
    # Agregación
    # - combined_insights: Annotated[List[Dict], add]  # Reducer
    # - executive_summary: str
    #
    # Validación
    # - validation_results: Dict
    # - confidence_score: float
    # - requires_human_review: bool
    # - review_reasons: List[str]
    pass


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)


# =============================================================================
# ETAPA 1: PREPROCESSING
# =============================================================================

def preprocess_node(state: DocumentAnalysisState) -> dict:
    """
    Preprocesa el documento.

    TODO:
    1. Limpiar texto (opcional: remover headers repetitivos)
    2. Detectar secciones principales
    3. Extraer metadata (fechas, montos, partes)
    """
    print("\n" + "="*70)
    print("📄 PREPROCESSING: Preparando documento...")
    print("="*70)

    # TODO: Implementar

    pass


# =============================================================================
# ETAPA 2: ANALISTAS (PARALELOS)
# =============================================================================

def financial_analyst(state: DocumentAnalysisState) -> dict:
    """
    Analiza aspectos financieros.

    TODO:
    1. Extraer montos, plazos, penalizaciones
    2. Analizar términos de pago
    3. Identificar riesgos financieros
    """
    print("\n💰 FINANCIAL ANALYST: Analizando finanzas...")

    # TODO: Implementar

    pass


def risk_analyst(state: DocumentAnalysisState) -> dict:
    """
    Analiza riesgos.

    TODO: Identificar riesgos legales, operacionales, financieros
    """
    print("\n⚠️  RISK ANALYST: Evaluando riesgos...")

    # TODO: Implementar

    pass


def legal_analyst(state: DocumentAnalysisState) -> dict:
    """
    Analiza aspectos legales.

    TODO: Cláusulas críticas, jurisdicción, compliance
    """
    print("\n⚖️  LEGAL ANALYST: Revisando aspectos legales...")

    # TODO: Implementar

    pass


def obligations_analyst(state: DocumentAnalysisState) -> dict:
    """
    Analiza obligaciones.

    TODO: Obligaciones de cada parte, entregables, deadlines
    """
    print("\n📋 OBLIGATIONS ANALYST: Identificando obligaciones...")

    # TODO: Implementar

    pass


# =============================================================================
# ETAPA 3: AGGREGATION
# =============================================================================

def aggregator_node(state: DocumentAnalysisState) -> dict:
    """
    Agrega todos los análisis.

    TODO:
    1. Recopilar análisis de todos los analistas
    2. Integrar hallazgos
    3. Priorizar por criticidad
    4. Generar executive summary
    """
    print("\n" + "="*70)
    print("🔄 AGGREGATOR: Integrando análisis...")
    print("="*70)

    # TODO: Implementar

    pass


# =============================================================================
# ETAPA 4: VALIDATION
# =============================================================================

def validator_node(state: DocumentAnalysisState) -> dict:
    """
    Valida calidad y decide revisión.

    TODO:
    1. Verificar completitud
    2. Calcular confidence score
    3. Decidir si requiere revisión humana
    """
    print("\n" + "="*70)
    print("✓ VALIDATOR: Verificando calidad...")
    print("="*70)

    # TODO: Implementar

    pass


def approve_node(state: DocumentAnalysisState) -> dict:
    """Output aprobado."""
    print("\n✅ ANÁLISIS APROBADO - Listo para entrega")
    return {}


def review_node(state: DocumentAnalysisState) -> dict:
    """Requiere revisión humana."""
    print("\n🔍 REQUIERE REVISIÓN HUMANA")
    print(f"Razones: {', '.join(state.get('review_reasons', []))}")
    return {}


# =============================================================================
# ROUTING
# =============================================================================

def route_after_validation(state: DocumentAnalysisState) -> Literal["approve", "review"]:
    """TODO: Implementar decisión basada en requires_human_review"""
    pass


# =============================================================================
# CONSTRUCCIÓN DEL GRAFO
# =============================================================================

def build_graph():
    """
    TODO:
    1. Agregar nodos
    2. Entry: preprocess
    3. Edges paralelos a los 4 analistas
    4. Edges de analistas a aggregator
    5. aggregator → validator
    6. Conditional: validator → [approve, review]
    """
    workflow = StateGraph(DocumentAnalysisState)

    # TODO: Implementar

    return workflow.compile()


# =============================================================================
# EJECUCIÓN
# =============================================================================

def main():
    print("\n" + "="*70)
    print("📊 PIPELINE DE ANÁLISIS DE DOCUMENTOS")
    print("="*70)

    # Documento de ejemplo (contrato simplificado)
    sample_document = """
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
        "document_text": sample_document,
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

    # TODO: Ejecutar pipeline
    # final_state = app.invoke(initial_state)

    # TODO: Mostrar resultados


if __name__ == "__main__":
    main()
