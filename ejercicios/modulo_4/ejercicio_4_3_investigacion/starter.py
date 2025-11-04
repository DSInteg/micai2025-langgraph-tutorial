"""
Ejercicio 4.3: Asistente de Investigación - STARTER
"""

from typing import TypedDict, List, Dict, Annotated
from operator import add
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
    """TODO: Crear plan de investigación"""
    pass

def web_researcher(state: ResearchState) -> dict:
    """TODO: Buscar información web"""
    pass

def doc_researcher(state: ResearchState) -> dict:
    """TODO: Buscar en documentos"""
    pass

def analyzer_node(state: ResearchState) -> dict:
    """TODO: Analizar hallazgos"""
    pass

def synthesizer_node(state: ResearchState) -> dict:
    """TODO: Generar reporte"""
    pass

def validator_node(state: ResearchState) -> dict:
    """TODO: Validar calidad"""
    pass

def build_graph():
    """TODO: Construir pipeline"""
    workflow = StateGraph(ResearchState)
    # TODO: Implementar
    return workflow.compile()

def main():
    print("="*70)
    print("🔬 ASISTENTE DE INVESTIGACIÓN")
    print("="*70)

    app = build_graph()
    # TODO: Ejecutar con topic de ejemplo

if __name__ == "__main__":
    main()
