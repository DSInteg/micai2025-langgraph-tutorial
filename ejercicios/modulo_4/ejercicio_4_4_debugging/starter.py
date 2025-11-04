"""
Ejercicio 4.4: Debugging y Observabilidad con LangSmith - STARTER

En este ejercicio implementarás un sistema con bugs intencionales y
luego usarás LangSmith para identificarlos y resolverlos.

IMPORTANTE: Lee el README.md antes de empezar.
"""

import operator
from typing import Annotated, TypedDict, Literal, Optional
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool

# Importar utilidades de LangSmith
from utils.langsmith_config import (
    LangSmithConfig,
    get_runnable_config,
    add_run_metadata,
    trace_section,
    log_agent_decision,
    trace_agent
)
from utils.llm_config import get_llm


# ============================================================================
# PARTE 1: CONFIGURACIÓN DE LANGSMITH
# ============================================================================

def verify_langsmith_setup():
    """
    Verifica que LangSmith esté configurado correctamente.

    TODO: Descomenta y completa esta función
    """
    # config = LangSmithConfig(project_name="micai-debugging-exercise")
    # config.print_status()
    # return config
    pass


# ============================================================================
# PARTE 2: DEFINIR ESTADO
# ============================================================================

class DocumentState(TypedDict):
    """
    Estado del sistema de análisis de documentos.

    TODO: Añade campos adicionales que te ayuden con debugging:
    - iteration_count: para detectar loops
    - tools_used: para rastrear qué herramientas se han usado
    - current_phase: para saber en qué fase estamos
    - errors: para acumular errores si ocurren
    """
    document: str
    document_type: Optional[str]
    extracted_data: Optional[dict]
    summary: Optional[str]
    validated: bool
    messages: Annotated[list, operator.add]


# ============================================================================
# PARTE 3: HERRAMIENTAS (CON BUGS INTENCIONALES)
# ============================================================================

# TODO: Implementa estas herramientas con descripciones AMBIGUAS (bug intencional)
# El objetivo es que el LLM se confunda al elegir la herramienta correcta

@tool
def extract_pdf_text(document: str) -> str:
    """
    TODO: Escribe una descripción AMBIGUA (bug intencional)
    Descripción genérica que no deja claro cuándo usar esta herramienta

    Ejemplo de bug: "Extract text from a document"
    (No especifica que es para PDFs específicamente)
    """
    # Simulación de extracción
    return f"Texto extraído de PDF: {document[:100]}..."


@tool
def extract_image_text(document: str) -> str:
    """
    TODO: Escribe una descripción AMBIGUA (bug intencional)
    Similar a extract_pdf_text, causará confusión
    """
    # Simulación de OCR
    return f"Texto OCR de imagen: {document[:100]}..."


@tool
def parse_structured_data(document: str) -> dict:
    """
    TODO: Escribe una descripción AMBIGUA (bug intencional)
    No especifica qué tipo de documentos procesa
    """
    # Simulación de parsing
    return {
        "title": "Document Title",
        "content": document[:50],
        "metadata": {"type": "structured"}
    }


# ============================================================================
# PARTE 4: NODOS DEL GRAFO (CON BUGS)
# ============================================================================

def classifier_node(state: DocumentState) -> DocumentState:
    """
    Clasifica el tipo de documento.

    BUG INTENCIONAL: Usa herramientas con descripciones ambiguas
    que causarán selección incorrecta.

    TODO:
    1. Implementa la lógica de clasificación
    2. USA las herramientas definidas arriba (con bugs)
    3. NO arregles las descripciones todavía
    4. Añade metadata para debugging

    PISTAS:
    - Usa trace_section para agrupar la clasificación
    - Usa log_agent_decision para registrar la decisión
    - Añade metadata con add_run_metadata
    """
    # TODO: Implementar
    pass


def extractor_node(state: DocumentState) -> DocumentState:
    """
    Extrae información del documento.

    BUG INTENCIONAL: Hace MÚLTIPLES llamadas al LLM cuando una sería suficiente.
    Esto causará alta latencia y costos innecesarios.

    TODO:
    1. Implementa extracción de datos
    2. INTENCIONALMENTE haz 3 llamadas separadas al LLM:
       - Una para extraer entidades
       - Otra para extraer fechas
       - Otra para extraer números
    3. (En la solución, combinarás en una sola llamada)

    PISTAS:
    - Cada llamada al LLM se verá en LangSmith
    - Podrás comparar latencia y costos
    """
    # TODO: Implementar con múltiples llamadas redundantes
    pass


def summarizer_node(state: DocumentState) -> DocumentState:
    """
    Resume el documento.

    TODO:
    1. Implementa generación de resumen
    2. Añade logging de decisiones
    3. Registra métricas (longitud del resumen, etc.)
    """
    # TODO: Implementar
    pass


def validator_node(state: DocumentState) -> DocumentState:
    """
    Valida que el procesamiento fue exitoso.

    TODO:
    1. Verifica que hay datos extraídos
    2. Verifica que hay resumen
    3. Marca como validado
    """
    # TODO: Implementar
    pass


# ============================================================================
# PARTE 5: ROUTING (CON BUG DE LOOP INFINITO)
# ============================================================================

def should_continue(state: DocumentState) -> Literal["extract", "summarize", "validate", "end"]:
    """
    Decide el siguiente paso en el procesamiento.

    BUG INTENCIONAL: NO hay límite de iteraciones, puede causar loop infinito.

    TODO:
    1. Implementa lógica de routing básica
    2. NO añadas protección contra loops todavía
    3. Añade metadata de la decisión de routing

    El flujo esperado:
    - Si no hay tipo de documento -> classifier
    - Si no hay datos extraídos -> extract
    - Si no hay resumen -> summarize
    - Si no está validado -> validate
    - Si todo está completo -> end

    BUG: Si algo falla en extracción, volverá a intentar indefinidamente
    """
    # TODO: Implementar sin protección contra loops
    pass


def should_extract(state: DocumentState) -> bool:
    """
    Decide si se necesita extraer datos.

    TODO: Implementar
    """
    pass


# ============================================================================
# PARTE 6: CONSTRUIR GRAFO
# ============================================================================

def create_document_analyzer_graph():
    """
    Crea el grafo del sistema de análisis de documentos.

    TODO:
    1. Crea StateGraph con DocumentState
    2. Añade todos los nodos
    3. Define edges y conditional_edges
    4. Compila y retorna

    Estructura sugerida:
    START -> classifier -> extractor -> summarizer -> validator -> END
    """
    # TODO: Implementar
    pass


# ============================================================================
# PARTE 7: FUNCIONES DE EJECUCIÓN
# ============================================================================

def run_analysis(
    document: str,
    document_type: Optional[str] = None,
    tags: list[str] = None
):
    """
    Ejecuta el análisis de documento con configuración de LangSmith.

    TODO:
    1. Crea configuración con get_runnable_config
    2. Añade tags y metadata apropiados
    3. Ejecuta el grafo
    4. Retorna resultados

    Args:
        document: El documento a analizar
        document_type: Tipo de documento (si se conoce)
        tags: Tags para LangSmith

    Returns:
        Estado final del procesamiento
    """
    # TODO: Implementar
    pass


# ============================================================================
# PARTE 8: DEBUGGING Y ANÁLISIS
# ============================================================================

def demonstrate_bugs():
    """
    Ejecuta ejemplos que demuestran cada uno de los bugs.

    TODO: Crea casos de prueba que expongan:
    1. Selección incorrecta de herramienta (descripciones ambiguas)
    2. Loop infinito (sin límite de iteraciones)
    3. Llamadas redundantes al LLM (múltiples llamadas innecesarias)
    """
    print("="*70)
    print("🐛 DEMOSTRACIÓN DE BUGS")
    print("="*70)
    print("\nEjecutando casos que exponen los bugs...")
    print("Ve a LangSmith para analizar cada problema.\n")

    # TODO: Caso 1 - Selección incorrecta de herramienta
    # Ejecuta con un PDF y verifica en LangSmith qué herramienta selecciona

    # TODO: Caso 2 - Loop infinito
    # Ejecuta con un documento que cause fallo en extracción

    # TODO: Caso 3 - Llamadas redundantes
    # Ejecuta y cuenta cuántas llamadas LLM se hacen en extractor_node


def analyze_performance():
    """
    Analiza el rendimiento usando métricas de LangSmith.

    TODO:
    1. Ejecuta múltiples análisis
    2. Recolecta métricas de LangSmith (puedes usar la UI)
    3. Identifica cuellos de botella
    4. Documenta hallazgos
    """
    print("="*70)
    print("📊 ANÁLISIS DE RENDIMIENTO")
    print("="*70)
    print("\nEn LangSmith, analiza:")
    print("1. Latencia total y por nodo")
    print("2. Número de tokens usados")
    print("3. Costo total")
    print("4. Patrones de ejecución")
    print("="*70)


# ============================================================================
# PARTE 9: TESTS
# ============================================================================

def test_with_langsmith():
    """
    Tests que usan LangSmith para validación.

    TODO: Implementa tests que:
    1. Verifican clasificación correcta
    2. Detectan loops infinitos
    3. Miden performance
    """
    pass


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("🔍 EJERCICIO 4.4: DEBUGGING CON LANGSMITH")
    print("="*70)

    # Paso 1: Verificar configuración
    print("\n📋 Paso 1: Verificando configuración de LangSmith...")
    # TODO: Descomenta cuando implementes verify_langsmith_setup()
    # config = verify_langsmith_setup()

    # Paso 2: Demostrar bugs
    print("\n🐛 Paso 2: Demostrando bugs intencionales...")
    # TODO: Descomenta cuando implementes demonstrate_bugs()
    # demonstrate_bugs()

    # Paso 3: Analizar performance
    print("\n📊 Paso 3: Analizando rendimiento...")
    # TODO: Descomenta cuando implementes analyze_performance()
    # analyze_performance()

    print("\n" + "="*70)
    print("📝 PRÓXIMOS PASOS:")
    print("="*70)
    print("""
1. Ve a LangSmith y analiza los traces
2. Identifica cada bug visualmente
3. Implementa las correcciones en solution.py
4. Compara métricas antes/después
5. Documenta tus hallazgos

Bugs a buscar:
- ❌ Herramientas con descripciones ambiguas
- ❌ Loop infinito en routing
- ❌ Múltiples llamadas LLM redundantes

Métricas a mejorar:
- ⚡ Reducir latencia al menos 30%
- 💰 Reducir costos eliminando llamadas redundantes
- ✅ Mejorar precisión de clasificación
""")
    print("="*70)
