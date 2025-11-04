"""
EJEMPLO: Pipeline de Análisis de Documentos (Módulo 4.2)

Este ejemplo demuestra un pipeline multi-etapa con análisis paralelos.
"""

from typing import TypedDict, Annotated, List, Dict
from operator import add
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()

# Estado con reducer
class PipelineState(TypedDict):
    document: str
    sections: Dict[str, str]
    analyses: Annotated[List[Dict], add]  # Reducer
    summary: str
    validated: bool

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

# Etapa 1: Preprocessing
def preprocess_node(state: PipelineState) -> dict:
    """Detecta secciones del documento."""
    print("\n📄 PREPROCESS: Analizando estructura...")

    doc = state["document"]

    # Detección simple de secciones
    sections = {}
    if "SCOPE" in doc:
        sections["scope"] = "Found scope section"
    if "PAYMENT" in doc:
        sections["payment"] = "Found payment section"
    if "TERM" in doc:
        sections["term"] = "Found term section"

    print(f"   ✓ Secciones detectadas: {len(sections)}")

    return {"sections": sections}

# Etapa 2: Analistas paralelos
def financial_analyst(state: PipelineState) -> dict:
    """Analiza aspectos financieros."""
    print("\n💰 FINANCIAL: Analizando finanzas...")

    prompt = f"""Extrae información financiera:

{state['document'][:500]}

Montos, plazos, penalizaciones:"""

    response = llm.invoke(prompt)

    return {
        "analyses": [{
            "type": "financial",
            "content": response.content[:200]
        }]
    }

def risk_analyst(state: PipelineState) -> dict:
    """Analiza riesgos."""
    print("\n⚠️  RISK: Evaluando riesgos...")

    prompt = f"""Identifica riesgos:

{state['document'][:500]}

Riesgos principales:"""

    response = llm.invoke(prompt)

    return {
        "analyses": [{
            "type": "risk",
            "content": response.content[:200]
        }]
    }

def legal_analyst(state: PipelineState) -> dict:
    """Analiza aspectos legales."""
    print("\n⚖️  LEGAL: Revisando cláusulas...")

    prompt = f"""Identifica cláusulas críticas:

{state['document'][:500]}

Cláusulas importantes:"""

    response = llm.invoke(prompt)

    return {
        "analyses": [{
            "type": "legal",
            "content": response.content[:200]
        }]
    }

# Etapa 3: Agregación
def aggregate_node(state: PipelineState) -> dict:
    """Agrega todos los análisis."""
    print(f"\n🔄 AGGREGATE: Integrando {len(state['analyses'])} análisis...")

    context = "\n\n".join([
        f"{a['type'].upper()}: {a['content']}"
        for a in state["analyses"]
    ])

    prompt = f"""Sintetiza estos análisis en un resumen ejecutivo:

{context}

RESUMEN EJECUTIVO:"""

    response = llm.invoke(prompt)

    return {"summary": response.content}

# Etapa 4: Validación
def validate_node(state: PipelineState) -> dict:
    """Valida completitud."""
    print(f"\n✓ VALIDATE: Verificando calidad...")

    # Validación simple
    has_all = len(state["analyses"]) >= 3
    has_summary = len(state.get("summary", "")) > 50

    validated = has_all and has_summary

    print(f"   → Validado: {'✅' if validated else '❌'}")

    return {"validated": validated}

# Construir pipeline
def build_pipeline():
    workflow = StateGraph(PipelineState)

    # Nodos
    workflow.add_node("preprocess", preprocess_node)
    workflow.add_node("financial", financial_analyst)
    workflow.add_node("risk", risk_analyst)
    workflow.add_node("legal", legal_analyst)
    workflow.add_node("aggregate", aggregate_node)
    workflow.add_node("validate", validate_node)

    # Flujo
    workflow.set_entry_point("preprocess")

    # Paralelo: 3 analistas
    workflow.add_edge("preprocess", "financial")
    workflow.add_edge("preprocess", "risk")
    workflow.add_edge("preprocess", "legal")

    # Convergencia
    workflow.add_edge("financial", "aggregate")
    workflow.add_edge("risk", "aggregate")
    workflow.add_edge("legal", "aggregate")

    # Secuencial
    workflow.add_edge("aggregate", "validate")
    workflow.add_edge("validate", END)

    return workflow.compile()

# Ejecutar
if __name__ == "__main__":
    app = build_pipeline()

    document = """
SERVICE AGREEMENT

SCOPE OF WORK:
Provider will develop a custom web application.

PAYMENT TERMS:
Total: $150,000 USD
- Milestone 1: $50,000 due March 31
- Milestone 2: $50,000 due June 30
- Milestone 3: $50,000 due Sept 30

TERM:
Effective March 1, 2024 to December 31, 2024.

TERMINATION:
30 days notice required.
Early termination penalty: 20% of remaining value.
"""

    print("="*70)
    print("📊 PIPELINE DE ANÁLISIS DE DOCUMENTOS")
    print("="*70)

    result = app.invoke({
        "document": document,
        "sections": {},
        "analyses": [],
        "summary": "",
        "validated": False
    })

    print("\n" + "="*70)
    print("📋 RESUMEN EJECUTIVO")
    print("="*70)
    print(result["summary"])
    print(f"\n✓ Análisis validado: {result['validated']}")
    print(f"✓ Total de análisis: {len(result['analyses'])}")
