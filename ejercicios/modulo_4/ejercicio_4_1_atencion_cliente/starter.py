"""
Ejercicio 4.1: Sistema de Atención al Cliente - STARTER

Sistema completo que integra routing, especialización, KB search y escalamiento.
"""

from typing import TypedDict, List, Dict, Literal
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END

load_dotenv()

# =============================================================================
# ESTADO GLOBAL
# =============================================================================

class CustomerSupportState(TypedDict):
    """
    Estado compartido del sistema de atención al cliente.

    Este estado fluye por todos los agentes y contiene:
    - Input del usuario y contexto
    - Clasificación de la consulta
    - Análisis de agentes especializados
    - Resultados de knowledge base
    - Respuesta final y métricas
    """
    # TODO: Define los campos del estado
    # - user_query: str
    # - user_id: str
    # - conversation_history: List[BaseMessage]
    # - category: str ("product", "support", "order")
    # - urgency: str ("low", "medium", "high")
    # - product_analysis: str
    # - support_analysis: str
    # - order_analysis: str
    # - kb_results: List[Dict]
    # - final_response: str
    # - confidence_score: float
    # - should_escalate: bool
    # - escalation_reason: str
    pass


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)


# =============================================================================
# KNOWLEDGE BASE (Simulado)
# =============================================================================

# TODO: Completar knowledge base con más datos
knowledge_base = {
    "products": [
        {
            "id": "LAPTOP001",
            "name": "Laptop Pro X15",
            "price": 1299.99,
            "specs": "Intel i7 11th Gen, 16GB RAM DDR4, 512GB SSD NVMe, Intel Iris Xe Graphics",
            "warranty": "2 years",
            "category": "laptops"
        },
        {
            "id": "PHONE001",
            "name": "Smartphone Ultra Z",
            "price": 899.99,
            "specs": "Snapdragon 8 Gen 2, 12GB RAM, 256GB Storage, 6.7\" AMOLED",
            "warranty": "1 year",
            "category": "phones"
        },
        # TODO: Agregar más productos
    ],
    "faqs": [
        {
            "question": "¿Cuál es la política de devoluciones?",
            "answer": "Aceptamos devoluciones dentro de 30 días de la compra sin preguntas. El producto debe estar en su empaque original y en condiciones de reventa.",
            "category": "policy"
        },
        {
            "question": "¿Cuánto tarda el envío?",
            "answer": "Envío estándar: 5-7 días hábiles. Envío express: 2-3 días hábiles. Envío same-day disponible en ciudades principales.",
            "category": "shipping"
        },
        # TODO: Agregar más FAQs
    ],
    "technical_docs": [
        {
            "product": "LAPTOP001",
            "issue": "No enciende",
            "solution": "1. Verificar que el cargador esté conectado correctamente. 2. Mantener presionado el botón de encendido por 10 segundos. 3. Conectar a corriente directa (sin batería) y probar. 4. Si persiste, contactar soporte para diagnóstico."
        },
        {
            "product": "PHONE001",
            "issue": "Batería se agota rápido",
            "solution": "1. Verificar apps con alto consumo en Settings > Battery. 2. Reducir brillo de pantalla. 3. Desactivar servicios de ubicación no necesarios. 4. Actualizar a última versión de software. 5. Considerar reemplazo de batería si tiene más de 2 años."
        },
        # TODO: Agregar más docs técnicas
    ]
}


# =============================================================================
# FUNCIONES DE KNOWLEDGE BASE
# =============================================================================

def search_knowledge_base(query: str, category: str, kb: Dict = knowledge_base) -> List[Dict]:
    """
    Busca información relevante en la base de conocimiento.

    TODO: Implementar búsqueda
    1. Tokenizar query
    2. Buscar en secciones relevantes según categoría
    3. Calcular relevancia por overlap de palabras
    4. Ordenar resultados
    5. Retornar top-k (máximo 5)
    """
    # TODO: Implementar

    pass


# =============================================================================
# AGENTES
# =============================================================================

def intake_agent(state: CustomerSupportState) -> dict:
    """
    Agente inicial que clasifica la consulta y busca en KB.

    Este agente es crítico porque:
    - Determina qué especialista debe atender
    - Identifica urgencia
    - Hace búsqueda inicial en KB
    - Prepara contexto para especialistas

    TODO:
    1. Analizar user_query
    2. Clasificar en: PRODUCT, SUPPORT, ORDER
    3. Determinar urgencia: LOW, MEDIUM, HIGH
    4. Buscar en knowledge base
    5. Retornar actualizaciones de estado
    """
    print("\n" + "="*70)
    print("🎯 INTAKE AGENT: Clasificando consulta...")
    print("="*70)

    query = state["user_query"]

    # TODO: Crear prompt de clasificación

    # TODO: Invocar LLM

    # TODO: Parsear respuesta (category, urgency)

    # TODO: Buscar en knowledge base

    print(f"   → Categoría: [CATEGORY]")
    print(f"   → Urgencia: [URGENCY]")
    print(f"   → KB Results: [COUNT] resultados")

    # TODO: Retornar estado actualizado

    return {}


def product_agent(state: CustomerSupportState) -> dict:
    """
    Agente especializado en consultas sobre productos.

    Maneja:
    - Preguntas sobre especificaciones
    - Comparaciones de productos
    - Recomendaciones
    - Información de precios y garantía

    TODO:
    1. Analizar consulta desde perspectiva de productos
    2. Usar kb_results si hay productos relevantes
    3. Generar análisis detallado
    4. Actualizar product_analysis
    """
    print("\n💻 PRODUCT AGENT: Analizando consulta de producto...")

    query = state["user_query"]
    kb_results = state.get("kb_results", [])

    # TODO: Preparar contexto de KB
    kb_context = ""
    # Si hay productos en kb_results, incluirlos

    # TODO: Crear prompt de análisis de producto

    # TODO: Invocar LLM

    print(f"   ✓ Análisis de producto generado")

    # TODO: Retornar product_analysis

    return {}


def support_agent(state: CustomerSupportState) -> dict:
    """
    Agente especializado en soporte técnico.

    Maneja:
    - Problemas técnicos
    - Troubleshooting
    - Soluciones paso a paso
    - Referencias a documentación

    TODO:
    1. Analizar problema técnico
    2. Buscar soluciones en technical_docs
    3. Proporcionar pasos de troubleshooting
    4. Actualizar support_analysis
    """
    print("\n🔧 SUPPORT AGENT: Analizando problema técnico...")

    query = state["user_query"]
    kb_results = state.get("kb_results", [])

    # TODO: Filtrar technical_docs de kb_results

    # TODO: Crear prompt de soporte técnico

    # TODO: Invocar LLM

    print(f"   ✓ Análisis de soporte generado")

    # TODO: Retornar support_analysis

    return {}


def order_agent(state: CustomerSupportState) -> dict:
    """
    Agente especializado en consultas sobre órdenes.

    Maneja:
    - Estado de pedidos
    - Tracking
    - Devoluciones
    - Facturación

    TODO:
    1. Analizar consulta sobre orden
    2. Buscar políticas relevantes en FAQs
    3. Generar análisis de orden
    4. Actualizar order_analysis
    """
    print("\n📦 ORDER AGENT: Analizando consulta de orden...")

    query = state["user_query"]
    kb_results = state.get("kb_results", [])

    # TODO: Filtrar FAQs relevantes de kb_results

    # TODO: Crear prompt de análisis de orden

    # TODO: Invocar LLM

    print(f"   ✓ Análisis de orden generado")

    # TODO: Retornar order_analysis

    return {}


def synthesizer_agent(state: CustomerSupportState) -> dict:
    """
    Sintetiza la respuesta final y decide si escalar.

    Este agente:
    - Integra análisis de especialista
    - Incorpora información de KB
    - Genera respuesta profesional
    - Calcula confidence score
    - Decide escalamiento a humano

    TODO:
    1. Recopilar análisis del especialista que ejecutó
    2. Preparar contexto con KB results
    3. Generar respuesta final profesional
    4. Calcular confidence score
    5. Decidir si escalar (confidence < 0.7 o urgency HIGH)
    """
    print("\n" + "="*70)
    print("✅ SYNTHESIZER: Generando respuesta final...")
    print("="*70)

    query = state["user_query"]
    category = state["category"]
    urgency = state["urgency"]
    kb_results = state.get("kb_results", [])

    # TODO: Obtener el análisis relevante según categoría
    specialist_analysis = ""
    # if category == "product": usar product_analysis
    # if category == "support": usar support_analysis
    # if category == "order": usar order_analysis

    # TODO: Preparar contexto de KB

    # TODO: Crear prompt de síntesis

    # TODO: Invocar LLM

    # TODO: Calcular confidence score
    confidence = 0.0
    # Factores:
    # - ¿Hay KB results? +0.3
    # - ¿Análisis es largo (>100 chars)? +0.3
    # - ¿No hay palabras de incertidumbre? +0.2
    # - ¿Urgency no es HIGH? +0.2

    # TODO: Decidir escalamiento
    should_escalate = False
    escalation_reason = ""

    print(f"   → Confidence Score: {confidence:.2f}")
    print(f"   → Decisión: {'ESCALAR' if should_escalate else 'RESPONDER'}")

    # TODO: Retornar estado actualizado

    return {}


def respond_node(state: CustomerSupportState) -> dict:
    """
    Nodo final que muestra la respuesta al usuario.
    """
    print("\n" + "="*70)
    print("📨 RESPUESTA AL USUARIO")
    print("="*70)
    print(state["final_response"])

    return {}


def escalate_node(state: CustomerSupportState) -> dict:
    """
    Nodo que escala a agente humano.
    """
    print("\n" + "="*70)
    print("🚨 ESCALADO A AGENTE HUMANO")
    print("="*70)
    print(f"Razón: {state['escalation_reason']}")
    print("\nInformación recopilada para agente humano:")
    print(f"   • Categoría: {state['category']}")
    print(f"   • Urgencia: {state['urgency']}")
    print(f"   • Consulta: {state['user_query']}")

    return {}


# =============================================================================
# FUNCIONES DE ROUTING
# =============================================================================

def route_to_specialist(state: CustomerSupportState) -> Literal["product", "support", "order"]:
    """
    Rutea al especialista apropiado según categoría.

    TODO: Implementar mapeo
    category "product" → nodo "product"
    category "support" → nodo "support"
    category "order" → nodo "order"
    """
    # TODO: Implementar

    pass


def route_after_synthesis(state: CustomerSupportState) -> Literal["respond", "escalate"]:
    """
    Decide si responder directamente o escalar a humano.

    TODO: Implementar decisión
    should_escalate == True → "escalate"
    should_escalate == False → "respond"
    """
    # TODO: Implementar

    pass


# =============================================================================
# CONSTRUCCIÓN DEL GRAFO
# =============================================================================

def build_graph():
    """
    Construye el grafo del sistema de atención al cliente.

    Flujo:
    1. intake → clasifica y busca KB
    2. conditional edge → [product, support, order]
    3. specialist → genera análisis
    4. synthesizer → genera respuesta + decide escalamiento
    5. conditional edge → [respond, escalate]
    6. END
    """
    workflow = StateGraph(CustomerSupportState)

    # TODO: Agregar nodos
    # - intake
    # - product
    # - support
    # - order
    # - synthesizer
    # - respond
    # - escalate

    # TODO: Set entry point a "intake"

    # TODO: Conditional edge: intake → specialist
    # workflow.add_conditional_edges(
    #     "intake",
    #     route_to_specialist,
    #     {...}
    # )

    # TODO: Edges: specialists → synthesizer

    # TODO: Conditional edge: synthesizer → [respond, escalate]
    # workflow.add_conditional_edges(
    #     "synthesizer",
    #     route_after_synthesis,
    #     {...}
    # )

    # TODO: Edges finales a END

    return workflow.compile()


# =============================================================================
# EJECUCIÓN Y DEMO
# =============================================================================

def main():
    print("\n" + "="*70)
    print("🏪 SISTEMA DE ATENCIÓN AL CLIENTE - TECHSTORE")
    print("="*70)

    # Consultas de ejemplo
    queries = [
        ("user_001", "¿La Laptop Pro X15 es buena para diseño gráfico? ¿Cuánta RAM tiene?"),
        ("user_002", "Mi smartphone no carga, ya probé con diferentes cables. ¿Qué hago?"),
        ("user_003", "Quiero devolver un producto que compré hace 15 días. ¿Cuál es el proceso?"),
        ("user_004", "URGENTE: Mi laptop no enciende y tengo presentación mañana. ¡Necesito ayuda YA!"),
    ]

    app = build_graph()

    for i, (user_id, query) in enumerate(queries, 1):
        print(f"\n{'='*70}")
        print(f"💬 CONSULTA {i}/{len(queries)} (Usuario: {user_id})")
        print(f"{'='*70}")
        print(f"Query: {query}")

        initial_state = {
            "user_query": query,
            "user_id": user_id,
            "conversation_history": [HumanMessage(content=query)],
            "category": "",
            "urgency": "",
            "product_analysis": "",
            "support_analysis": "",
            "order_analysis": "",
            "kb_results": [],
            "final_response": "",
            "confidence_score": 0.0,
            "should_escalate": False,
            "escalation_reason": ""
        }

        # TODO: Invocar el grafo
        # final_state = app.invoke(initial_state)

        print("\n" + "="*70)
        print("📊 RESUMEN DE INTERACCIÓN")
        print("="*70)
        # TODO: Mostrar métricas
        # print(f"Categoría: {final_state['category']}")
        # print(f"Urgencia: {final_state['urgency']}")
        # print(f"Confidence: {final_state['confidence_score']:.2f}")
        # print(f"Escalado: {'Sí' if final_state['should_escalate'] else 'No'}")

        if i < len(queries):
            input("\n[Presiona Enter para siguiente consulta...]")


if __name__ == "__main__":
    main()
