"""
Ejercicio 4.1: Sistema de Atención al Cliente - SOLUCIÓN COMPLETA

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
    """Estado compartido del sistema de atención al cliente."""
    user_query: str                 # Consulta del usuario
    user_id: str                    # ID del usuario
    conversation_history: List[BaseMessage]  # Historial de mensajes
    category: str                   # "product", "support", "order"
    urgency: str                    # "low", "medium", "high"
    product_analysis: str           # Análisis del product agent
    support_analysis: str           # Análisis del support agent
    order_analysis: str             # Análisis del order agent
    kb_results: List[Dict]          # Resultados de knowledge base
    final_response: str             # Respuesta final al usuario
    confidence_score: float         # Score de confianza (0-1)
    should_escalate: bool           # Si escalar a humano
    escalation_reason: str          # Razón del escalamiento


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)


# =============================================================================
# KNOWLEDGE BASE (Simulado)
# =============================================================================

knowledge_base = {
    "products": [
        {
            "id": "LAPTOP001",
            "name": "Laptop Pro X15",
            "price": 1299.99,
            "specs": "Intel i7 11th Gen, 16GB RAM DDR4, 512GB SSD NVMe, Intel Iris Xe Graphics, 15.6\" Full HD IPS",
            "warranty": "2 years",
            "category": "laptops",
            "stock": 25
        },
        {
            "id": "LAPTOP002",
            "name": "Laptop Pro X15 Gaming",
            "price": 1799.99,
            "specs": "Intel i7 11th Gen, 32GB RAM DDR4, 1TB SSD NVMe, NVIDIA RTX 3060 6GB, 15.6\" Full HD 144Hz",
            "warranty": "2 years",
            "category": "laptops",
            "stock": 12
        },
        {
            "id": "PHONE001",
            "name": "Smartphone Ultra Z",
            "price": 899.99,
            "specs": "Snapdragon 8 Gen 2, 12GB RAM, 256GB Storage, 6.7\" AMOLED 120Hz, 108MP Camera",
            "warranty": "1 year",
            "category": "phones",
            "stock": 50
        },
        {
            "id": "TABLET001",
            "name": "Tablet Pro 12",
            "price": 649.99,
            "specs": "Apple M1, 8GB RAM, 256GB Storage, 12.9\" Liquid Retina XDR",
            "warranty": "1 year",
            "category": "tablets",
            "stock": 18
        }
    ],
    "faqs": [
        {
            "question": "¿Cuál es la política de devoluciones?",
            "answer": "Aceptamos devoluciones dentro de 30 días de la compra sin preguntas. El producto debe estar en su empaque original y en condiciones de reventa. El reembolso se procesa en 5-7 días hábiles.",
            "category": "policy"
        },
        {
            "question": "¿Cuánto tarda el envío?",
            "answer": "Envío estándar: 5-7 días hábiles. Envío express: 2-3 días hábiles. Envío same-day disponible en Ciudad de México, Guadalajara y Monterrey para pedidos antes de las 2 PM.",
            "category": "shipping"
        },
        {
            "question": "¿Qué métodos de pago aceptan?",
            "answer": "Aceptamos: Tarjetas de crédito/débito (Visa, Mastercard, American Express), PayPal, transferencia bancaria, y pago en efectivo en tiendas OXXO.",
            "category": "payment"
        },
        {
            "question": "¿Cómo puedo rastrear mi pedido?",
            "answer": "Recibirás un correo con el número de rastreo 24 horas después del envío. Puedes rastrear tu pedido en nuestra página de tracking o directamente en el sitio de la paquetería.",
            "category": "shipping"
        },
        {
            "question": "¿La garantía cubre qué?",
            "answer": "La garantía cubre defectos de fabricación y fallas de hardware. NO cubre: daño por agua, caídas, mal uso, o software de terceros. Incluye reparación o reemplazo sin costo.",
            "category": "warranty"
        }
    ],
    "technical_docs": [
        {
            "product": "LAPTOP001",
            "issue": "No enciende",
            "solution": "1. Verificar que el cargador esté conectado correctamente y el LED de carga esté encendido. 2. Mantener presionado el botón de encendido por 10-15 segundos para hard reset. 3. Desconectar batería (si es removible), conectar solo el cargador y probar. 4. Verificar que no haya daño físico en puerto de carga. Si persiste, contactar soporte técnico para diagnóstico avanzado."
        },
        {
            "product": "LAPTOP001",
            "issue": "Sobrecalentamiento",
            "solution": "1. Limpiar ventiladores con aire comprimido. 2. Usar en superficie dura y plana (no sobre cama/alfombra). 3. Actualizar drivers de gráficos y BIOS. 4. Verificar apps con alto uso de CPU en Task Manager. 5. Considerar pasta térmica nueva si tiene más de 2 años."
        },
        {
            "product": "PHONE001",
            "issue": "Batería se agota rápido",
            "solution": "1. Verificar apps con alto consumo en Settings > Battery > Battery Usage. 2. Reducir brillo de pantalla y activar modo adaptativo. 3. Desactivar servicios de ubicación no necesarios. 4. Cerrar apps en segundo plano. 5. Activar modo de ahorro de energía. 6. Actualizar a última versión de software. Si tiene más de 2 años, considerar reemplazo de batería."
        },
        {
            "product": "PHONE001",
            "issue": "No carga",
            "solution": "1. Probar con cable y cargador diferentes (usar originales si es posible). 2. Limpiar puerto de carga con aire comprimido (sin líquidos). 3. Reiniciar el teléfono. 4. Probar carga inalámbrica si está disponible. 5. Verificar que cable no esté dañado. Si no carga con múltiples cables/cargadores, contactar soporte."
        }
    ]
}


# =============================================================================
# FUNCIONES DE KNOWLEDGE BASE
# =============================================================================

def search_knowledge_base(query: str, category: str, kb: Dict = knowledge_base) -> List[Dict]:
    """
    Busca información relevante en la base de conocimiento.

    Implementa búsqueda simple por keywords. En producción,
    usarías embeddings y búsqueda semántica.
    """
    results = []
    query_lower = query.lower()
    query_words = set(query_lower.split())

    # Buscar en productos si es consulta de producto
    if category == "product":
        for product in kb["products"]:
            # Buscar en nombre y specs
            product_text = f"{product['name']} {product['specs']}".lower()
            product_words = set(product_text.split())
            overlap = len(query_words & product_words)

            if overlap > 0:
                results.append({
                    "type": "product",
                    "data": product,
                    "relevance": overlap
                })

    # Buscar en docs técnicas si es soporte
    elif category == "support":
        for doc in kb["technical_docs"]:
            doc_text = f"{doc['issue']} {doc['solution']}".lower()
            doc_words = set(doc_text.split())
            overlap = len(query_words & doc_words)

            if overlap > 1:
                results.append({
                    "type": "technical_doc",
                    "data": doc,
                    "relevance": overlap
                })

    # Siempre buscar en FAQs (son útiles para todas las categorías)
    for faq in kb["faqs"]:
        faq_text = f"{faq['question']} {faq['answer']}".lower()
        faq_words = set(faq_text.split())
        overlap = len(query_words & faq_words)

        if overlap > 1:
            results.append({
                "type": "faq",
                "data": faq,
                "relevance": overlap
            })

    # Ordenar por relevancia y retornar top 5
    results.sort(key=lambda x: x.get("relevance", 0), reverse=True)

    return results[:5]


# =============================================================================
# AGENTES
# =============================================================================

def intake_agent(state: CustomerSupportState) -> dict:
    """
    Agente inicial que clasifica la consulta y busca en KB.

    Este agente es el punto de entrada del sistema y establece
    el contexto para todo el flujo posterior.
    """
    print("\n" + "="*70)
    print("🎯 INTAKE AGENT: Clasificando consulta...")
    print("="*70)

    query = state["user_query"]

    # Clasificación usando LLM
    classification_prompt = f"""Eres un agente de clasificación de consultas de atención al cliente para TechStore (tienda de tecnología).

CONSULTA DEL USUARIO:
{query}

Clasifica la consulta en UNA de estas categorías:
- PRODUCT: Preguntas sobre productos, especificaciones, comparaciones, recomendaciones, precios
- SUPPORT: Problemas técnicos, troubleshooting, cómo usar productos, reparaciones
- ORDER: Estado de pedidos, tracking, devoluciones, facturación, envíos

También determina el nivel de URGENCIA:
- LOW: Pregunta informativa, no urgente, exploración
- MEDIUM: Problema que necesita resolución pronto pero no es crítico
- HIGH: Problema crítico, cliente bloqueado, frustrado, o usa palabras como "urgente", "YA", "inmediatamente"

Responde en formato exacto:
CATEGORY: [PRODUCT/SUPPORT/ORDER]
URGENCY: [LOW/MEDIUM/HIGH]

CLASIFICACIÓN:"""

    response = llm.invoke(classification_prompt)
    classification_text = response.content

    # Parsear respuesta
    lines = classification_text.strip().split('\n')
    category = "product"  # default
    urgency = "medium"    # default

    for line in lines:
        if "CATEGORY:" in line.upper():
            cat = line.split(":")[-1].strip().lower()
            if cat in ["product", "support", "order"]:
                category = cat
        elif "URGENCY:" in line.upper():
            urg = line.split(":")[-1].strip().lower()
            if urg in ["low", "medium", "high"]:
                urgency = urg

    # Buscar en knowledge base
    kb_results = search_knowledge_base(query, category)

    print(f"   → Categoría: {category.upper()}")
    print(f"   → Urgencia: {urgency.upper()}")
    print(f"   → KB Results: {len(kb_results)} resultados encontrados")

    if kb_results:
        print(f"   → Top result: {kb_results[0]['type']}")

    return {
        "category": category,
        "urgency": urgency,
        "kb_results": kb_results
    }


def product_agent(state: CustomerSupportState) -> dict:
    """Agente especializado en consultas sobre productos."""
    print("\n💻 PRODUCT AGENT: Analizando consulta de producto...")

    query = state["user_query"]
    kb_results = state.get("kb_results", [])

    # Preparar contexto de productos de KB
    kb_context = ""
    if kb_results:
        kb_context = "\n\nINFORMACIÓN DE PRODUCTOS EN BASE DE CONOCIMIENTO:\n"
        for result in kb_results:
            if result["type"] == "product":
                product = result["data"]
                kb_context += f"\n{product['name']} (ID: {product['id']})\n"
                kb_context += f"  Precio: ${product['price']}\n"
                kb_context += f"  Specs: {product['specs']}\n"
                kb_context += f"  Garantía: {product['warranty']}\n"
                kb_context += f"  Stock: {product['stock']} unidades\n"
            elif result["type"] == "faq":
                faq = result["data"]
                kb_context += f"\nFAQ: {faq['question']}\n"
                kb_context += f"  Respuesta: {faq['answer']}\n"

    # Análisis de producto
    analysis_prompt = f"""Eres un especialista en productos de TechStore.

CONSULTA DEL USUARIO:
{query}

{kb_context}

Tu trabajo es:
1. Responder preguntas específicas sobre productos
2. Comparar productos si se solicita
3. Proporcionar recomendaciones basadas en necesidades
4. Incluir información de specs, precio, garantía
5. Mencionar disponibilidad de stock si es relevante

Genera un análisis DETALLADO Y ESPECÍFICO desde la perspectiva de productos.
Usa información del catálogo cuando esté disponible.

ANÁLISIS DE PRODUCTOS:"""

    response = llm.invoke(analysis_prompt)
    analysis = response.content

    print(f"   ✓ Análisis de producto generado ({len(analysis)} caracteres)")

    return {"product_analysis": analysis}


def support_agent(state: CustomerSupportState) -> dict:
    """Agente especializado en soporte técnico."""
    print("\n🔧 SUPPORT AGENT: Analizando problema técnico...")

    query = state["user_query"]
    kb_results = state.get("kb_results", [])

    # Preparar contexto de documentación técnica
    kb_context = ""
    if kb_results:
        kb_context = "\n\nDOCUMENTACIÓN TÉCNICA RELEVANTE:\n"
        for result in kb_results:
            if result["type"] == "technical_doc":
                doc = result["data"]
                kb_context += f"\nProducto: {doc['product']}\n"
                kb_context += f"  Problema: {doc['issue']}\n"
                kb_context += f"  Solución: {doc['solution']}\n"
            elif result["type"] == "faq" and "warranty" in result["data"].get("category", ""):
                faq = result["data"]
                kb_context += f"\nPolítica: {faq['question']}\n"
                kb_context += f"  {faq['answer']}\n"

    # Análisis de soporte
    analysis_prompt = f"""Eres un especialista en soporte técnico de TechStore.

CONSULTA DEL USUARIO:
{query}

{kb_context}

Tu trabajo es:
1. Diagnosticar el problema técnico
2. Proporcionar pasos de troubleshooting específicos y numerados
3. Usar documentación técnica cuando esté disponible
4. Ser claro y preciso en las instrucciones
5. Mencionar cuándo es necesario contactar soporte avanzado

Genera un análisis TÉCNICO DETALLADO con pasos accionables.

ANÁLISIS DE SOPORTE TÉCNICO:"""

    response = llm.invoke(analysis_prompt)
    analysis = response.content

    print(f"   ✓ Análisis de soporte generado ({len(analysis)} caracteres)")

    return {"support_analysis": analysis}


def order_agent(state: CustomerSupportState) -> dict:
    """Agente especializado en consultas sobre órdenes."""
    print("\n📦 ORDER AGENT: Analizando consulta de orden...")

    query = state["user_query"]
    kb_results = state.get("kb_results", [])

    # Preparar contexto de políticas
    kb_context = ""
    if kb_results:
        kb_context = "\n\nPOLÍTICAS Y PROCEDIMIENTOS RELEVANTES:\n"
        for result in kb_results:
            if result["type"] == "faq":
                faq = result["data"]
                if faq["category"] in ["policy", "shipping", "payment", "warranty"]:
                    kb_context += f"\n{faq['question']}\n"
                    kb_context += f"  {faq['answer']}\n"

    # Análisis de orden
    analysis_prompt = f"""Eres un especialista en gestión de órdenes de TechStore.

CONSULTA DEL USUARIO:
{query}

{kb_context}

Tu trabajo es:
1. Responder sobre estado de pedidos, tracking, envíos
2. Explicar proceso de devoluciones y reembolsos
3. Aclarar políticas de envío y pagos
4. Proporcionar información de contacto para casos especiales
5. Ser preciso con tiempos y procedimientos

Genera un análisis DETALLADO sobre la gestión de la orden.
Si necesitas información específica del sistema de órdenes que no tienes,
indícalo claramente.

ANÁLISIS DE ORDEN:"""

    response = llm.invoke(analysis_prompt)
    analysis = response.content

    print(f"   ✓ Análisis de orden generado ({len(analysis)} caracteres)")

    return {"order_analysis": analysis}


def synthesizer_agent(state: CustomerSupportState) -> dict:
    """
    Sintetiza la respuesta final y decide si escalar.

    Este es el agente más importante porque determina
    la calidad de la respuesta final y si se puede manejar
    automáticamente o requiere intervención humana.
    """
    print("\n" + "="*70)
    print("✅ SYNTHESIZER: Generando respuesta final...")
    print("="*70)

    query = state["user_query"]
    category = state["category"]
    urgency = state["urgency"]
    kb_results = state.get("kb_results", [])

    # Obtener el análisis relevante
    specialist_analysis = ""
    if category == "product":
        specialist_analysis = state.get("product_analysis", "")
    elif category == "support":
        specialist_analysis = state.get("support_analysis", "")
    elif category == "order":
        specialist_analysis = state.get("order_analysis", "")

    # Preparar contexto de KB para síntesis
    kb_summary = ""
    if kb_results:
        kb_summary = f"\n\nSe encontraron {len(kb_results)} recursos en la base de conocimiento."

    # Síntesis de respuesta
    synthesis_prompt = f"""Eres un agente que genera respuestas finales profesionales para atención al cliente de TechStore.

CONSULTA ORIGINAL DEL USUARIO:
{query}

ANÁLISIS DEL ESPECIALISTA ({category.upper()}):
{specialist_analysis}

{kb_summary}

URGENCIA: {urgency.upper()}

Genera una RESPUESTA FINAL PROFESIONAL que:

1. SALUDO: Comienza con "Estimado cliente,"

2. CUERPO PRINCIPAL:
   - Sea clara, específica y directa
   - Use información del análisis del especialista
   - Incluya todos los detalles relevantes
   - Sea estructurada (usa listas, secciones si es apropiado)
   - Proporcione pasos accionables cuando aplique

3. CIERRE:
   - Ofrezca ayuda adicional
   - Sea cortés y profesional
   - Firma: "Saludos, Sistema de Atención TechStore"

IMPORTANTE:
- Si el análisis menciona que necesita información de sistemas externos (órdenes, RMA, etc.)
  que no tienes, incluye al final: [REQUIERE_ESCALAMIENTO]
- Si la urgencia es HIGH y el problema es complejo, incluye: [REQUIERE_ESCALAMIENTO]
- Si hay incertidumbre significativa, incluye: [REQUIERE_ESCALAMIENTO]

RESPUESTA FINAL:"""

    response = llm.invoke(synthesis_prompt)
    final_response = response.content

    # Calcular confidence score
    confidence = 0.0

    # Factor 1: ¿Hay resultados en KB? (+0.3)
    if kb_results:
        confidence += 0.3

    # Factor 2: ¿El análisis es sustancial? (+0.3)
    if len(specialist_analysis) > 100:
        confidence += 0.3

    # Factor 3: ¿No hay palabras de incertidumbre? (+0.2)
    uncertainty_keywords = [
        "no estoy seguro", "podría ser", "tal vez", "posiblemente",
        "no tengo acceso", "necesito información", "requiere validación"
    ]
    has_uncertainty = any(kw in specialist_analysis.lower() for kw in uncertainty_keywords)
    if not has_uncertainty:
        confidence += 0.2

    # Factor 4: ¿Urgency no es HIGH? (+0.2)
    if urgency != "high":
        confidence += 0.2

    confidence = min(confidence, 1.0)

    # Decidir escalamiento
    should_escalate = False
    escalation_reason = ""

    # Criterio 1: Respuesta indica que requiere escalamiento
    if "[REQUIERE_ESCALAMIENTO]" in final_response:
        should_escalate = True
        escalation_reason = "La consulta requiere acceso a sistemas externos o validación manual"
        # Remover el tag de la respuesta
        final_response = final_response.replace("[REQUIERE_ESCALAMIENTO]", "").strip()

    # Criterio 2: Confidence muy bajo
    elif confidence < 0.5:
        should_escalate = True
        escalation_reason = f"Confidence score muy bajo ({confidence:.2f}). Requiere revisión humana"

    # Criterio 3: HIGH urgency + confidence bajo
    elif urgency == "high" and confidence < 0.7:
        should_escalate = True
        escalation_reason = f"Alta urgencia con confidence moderado ({confidence:.2f}). Mejor que lo maneje un humano"

    print(f"   → Confidence Score: {confidence:.2f}")
    print(f"   → Decisión: {'ESCALAR A HUMANO' if should_escalate else 'RESPONDER DIRECTAMENTE'}")

    return {
        "final_response": final_response,
        "confidence_score": confidence,
        "should_escalate": should_escalate,
        "escalation_reason": escalation_reason
    }


def respond_node(state: CustomerSupportState) -> dict:
    """Nodo final que muestra la respuesta al usuario."""
    print("\n" + "="*70)
    print("📨 RESPUESTA AL USUARIO")
    print("="*70)
    print(state["final_response"])

    return {}


def escalate_node(state: CustomerSupportState) -> dict:
    """Nodo que escala a agente humano."""
    print("\n" + "="*70)
    print("🚨 ESCALADO A AGENTE HUMANO")
    print("="*70)
    print(f"Razón: {state['escalation_reason']}\n")
    print("INFORMACIÓN RECOPILADA PARA AGENTE HUMANO:")
    print(f"   • Usuario: {state['user_id']}")
    print(f"   • Categoría: {state['category'].upper()}")
    print(f"   • Urgencia: {state['urgency'].upper()}")
    print(f"   • Confidence Score: {state['confidence_score']:.2f}")
    print(f"\n   • Consulta Original:")
    print(f"     {state['user_query']}")

    # Mostrar análisis recopilado
    if state["category"] == "product" and state.get("product_analysis"):
        print(f"\n   • Análisis de Productos (prelim):")
        print(f"     {state['product_analysis'][:200]}...")
    elif state["category"] == "support" and state.get("support_analysis"):
        print(f"\n   • Análisis Técnico (prelim):")
        print(f"     {state['support_analysis'][:200]}...")
    elif state["category"] == "order" and state.get("order_analysis"):
        print(f"\n   • Análisis de Orden (prelim):")
        print(f"     {state['order_analysis'][:200]}...")

    print(f"\n   • Tiempo estimado de respuesta: {'Inmediato' if state['urgency'] == 'high' else '5-15 minutos'}")

    return {}


# =============================================================================
# FUNCIONES DE ROUTING
# =============================================================================

def route_to_specialist(state: CustomerSupportState) -> Literal["product", "support", "order"]:
    """Rutea al especialista apropiado según categoría."""
    category = state["category"]

    # Mapeo directo
    category_map = {
        "product": "product",
        "support": "support",
        "order": "order"
    }

    next_node = category_map.get(category, "product")

    print(f"\n   → Routing a especialista: {next_node.upper()}")

    return next_node


def route_after_synthesis(state: CustomerSupportState) -> Literal["respond", "escalate"]:
    """Decide si responder directamente o escalar a humano."""
    should_escalate = state["should_escalate"]

    if should_escalate:
        return "escalate"
    else:
        return "respond"


# =============================================================================
# CONSTRUCCIÓN DEL GRAFO
# =============================================================================

def build_graph():
    """
    Construye el grafo del sistema de atención al cliente.

    Arquitectura:
    - Intake clasifica y prepara contexto
    - Router deriva a especialista apropiado
    - Especialista analiza en su dominio
    - Synthesizer integra y decide escalamiento
    - Router final decide responder o escalar
    """
    workflow = StateGraph(CustomerSupportState)

    # Agregar todos los nodos
    workflow.add_node("intake", intake_agent)
    workflow.add_node("product", product_agent)
    workflow.add_node("support", support_agent)
    workflow.add_node("order", order_agent)
    workflow.add_node("synthesizer", synthesizer_agent)
    workflow.add_node("respond", respond_node)
    workflow.add_node("escalate", escalate_node)

    # Entry point
    workflow.set_entry_point("intake")

    # Routing condicional a especialista
    workflow.add_conditional_edges(
        "intake",
        route_to_specialist,
        {
            "product": "product",
            "support": "support",
            "order": "order"
        }
    )

    # Todos los especialistas van a synthesizer
    workflow.add_edge("product", "synthesizer")
    workflow.add_edge("support", "synthesizer")
    workflow.add_edge("order", "synthesizer")

    # Routing condicional después de síntesis
    workflow.add_conditional_edges(
        "synthesizer",
        route_after_synthesis,
        {
            "respond": "respond",
            "escalate": "escalate"
        }
    )

    # Nodos finales
    workflow.add_edge("respond", END)
    workflow.add_edge("escalate", END)

    return workflow.compile()


# =============================================================================
# EJECUCIÓN Y DEMO
# =============================================================================

def main():
    print("\n" + "="*70)
    print("🏪 SISTEMA DE ATENCIÓN AL CLIENTE - TECHSTORE")
    print("="*70)
    print("\nEste sistema demuestra integración de múltiples patterns:")
    print("  • Routing inteligente")
    print("  • Agentes especializados")
    print("  • Knowledge base search")
    print("  • Confidence scoring")
    print("  • Escalamiento automático\n")

    # Consultas de ejemplo que cubren diferentes escenarios
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

        # Ejecutar grafo
        final_state = app.invoke(initial_state)

        # Mostrar métricas finales
        print("\n" + "="*70)
        print("📊 MÉTRICAS DE LA INTERACCIÓN")
        print("="*70)
        print(f"Categoría: {final_state['category'].upper()}")
        print(f"Urgencia: {final_state['urgency'].upper()}")
        print(f"Confidence Score: {final_state['confidence_score']:.2f}")
        print(f"Escalado a Humano: {'✅ SÍ' if final_state['should_escalate'] else '❌ NO'}")
        print(f"KB Results: {len(final_state['kb_results'])} recursos encontrados")

        if i < len(queries):
            input("\n[Presiona Enter para siguiente consulta...]")

    print("\n" + "="*70)
    print("🎉 ¡DEMO COMPLETADA!")
    print("="*70)
    print("\n💡 Este sistema integra todos los conceptos del tutorial:")
    print("   ✅ Routing basado en clasificación (Módulo 2.1)")
    print("   ✅ Agentes especializados con expertise (Módulo 3.2)")
    print("   ✅ Knowledge base como memoria (Módulo 3.3)")
    print("   ✅ Síntesis de múltiples fuentes (Módulo 2.3)")
    print("   ✅ Decision making con confidence (Módulo 3.1)")
    print("\n🚀 Listo para producción con:")
    print("   • Vector DB para KB search semántica")
    print("   • Integración con CRM/ticketing system")
    print("   • Logging y monitoring")
    print("   • A/B testing de respuestas")


if __name__ == "__main__":
    main()
