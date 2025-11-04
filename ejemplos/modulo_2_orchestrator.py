"""
EJEMPLO: Orchestrator-Workers Pattern (Módulo 2.3)

Este ejemplo demuestra un orquestador que divide trabajo entre workers.
"""

from typing import TypedDict, Dict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()

# Estado
class OrchestratorState(TypedDict):
    document: str
    plan: str
    executive_summary: str
    technical_summary: str
    financial_summary: str
    final_report: str

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# Orchestrator: Planifica
def orchestrator_plan(state: OrchestratorState) -> dict:
    """Orquestador crea el plan de análisis."""
    print("🎯 ORCHESTRATOR: Creando plan de análisis...")

    prompt = f"""Analiza este documento y crea un plan de análisis:

DOCUMENTO:
{state['document'][:500]}...

Identifica:
1. Aspectos ejecutivos a analizar
2. Aspectos técnicos a analizar
3. Aspectos financieros a analizar

PLAN:"""

    response = llm.invoke(prompt)
    return {"plan": response.content}

# Workers especializados
def executive_worker(state: OrchestratorState) -> dict:
    """Worker de análisis ejecutivo."""
    print("👔 EXECUTIVE WORKER: Analizando aspectos ejecutivos...")

    prompt = f"""Analiza aspectos ejecutivos de este documento:

DOCUMENTO:
{state['document']}

GUÍA:
{state['plan']}

Genera resumen ejecutivo (estrategia, objetivos, impacto):"""

    response = llm.invoke(prompt)
    return {"executive_summary": response.content}

def technical_worker(state: OrchestratorState) -> dict:
    """Worker de análisis técnico."""
    print("🔧 TECHNICAL WORKER: Analizando aspectos técnicos...")

    prompt = f"""Analiza aspectos técnicos de este documento:

DOCUMENTO:
{state['document']}

GUÍA:
{state['plan']}

Genera resumen técnico (implementación, arquitectura, tecnologías):"""

    response = llm.invoke(prompt)
    return {"technical_summary": response.content}

def financial_worker(state: OrchestratorState) -> dict:
    """Worker de análisis financiero."""
    print("💰 FINANCIAL WORKER: Analizando aspectos financieros...")

    prompt = f"""Analiza aspectos financieros de este documento:

DOCUMENTO:
{state['document']}

GUÍA:
{state['plan']}

Genera resumen financiero (costos, ROI, presupuesto):"""

    response = llm.invoke(prompt)
    return {"financial_summary": response.content}

# Orchestrator: Sintetiza
def orchestrator_synthesize(state: OrchestratorState) -> dict:
    """Orquestador sintetiza los resultados."""
    print("\n🔄 ORCHESTRATOR: Sintetizando reportes...")

    prompt = f"""Integra estos tres análisis en un reporte final coherente:

ANÁLISIS EJECUTIVO:
{state['executive_summary']}

ANÁLISIS TÉCNICO:
{state['technical_summary']}

ANÁLISIS FINANCIERO:
{state['financial_summary']}

REPORTE FINAL INTEGRADO:"""

    response = llm.invoke(prompt)
    return {"final_report": response.content}

# Construir grafo
def build_orchestrator_system():
    workflow = StateGraph(OrchestratorState)

    # Nodos
    workflow.add_node("orchestrator_plan", orchestrator_plan)
    workflow.add_node("executive", executive_worker)
    workflow.add_node("technical", technical_worker)
    workflow.add_node("financial", financial_worker)
    workflow.add_node("orchestrator_synthesize", orchestrator_synthesize)

    # Flujo (Diamond Pattern)
    workflow.set_entry_point("orchestrator_plan")

    # Orchestrator → Workers (paralelo)
    workflow.add_edge("orchestrator_plan", "executive")
    workflow.add_edge("orchestrator_plan", "technical")
    workflow.add_edge("orchestrator_plan", "financial")

    # Workers → Orchestrator (convergencia)
    workflow.add_edge("executive", "orchestrator_synthesize")
    workflow.add_edge("technical", "orchestrator_synthesize")
    workflow.add_edge("financial", "orchestrator_synthesize")

    workflow.add_edge("orchestrator_synthesize", END)

    return workflow.compile()

# Ejecutar
if __name__ == "__main__":
    app = build_orchestrator_system()

    document = """
PROJECT PROPOSAL: AI-Powered Customer Service Platform

EXECUTIVE SUMMARY:
We propose developing an AI-powered customer service platform that will
revolutionize how our company interacts with customers. This platform will
reduce response time by 70% and improve customer satisfaction by 40%.

TECHNICAL APPROACH:
- LangGraph for multi-agent orchestration
- Vector database for knowledge management
- Real-time analytics dashboard
- Integration with existing CRM systems

BUDGET & TIMELINE:
Total cost: $500,000
Timeline: 6 months
Expected ROI: 200% in first year
Team: 5 engineers, 1 PM, 2 ML specialists
"""

    print("="*70)
    print("📄 ORCHESTRATOR-WORKERS PATTERN")
    print("="*70)

    result = app.invoke({
        "document": document,
        "plan": "",
        "executive_summary": "",
        "technical_summary": "",
        "financial_summary": "",
        "final_report": ""
    })

    print("\n" + "="*70)
    print("📊 REPORTE FINAL")
    print("="*70)
    print(result["final_report"])
