"""
Ejercicio 2.1: Sistema de Routing con Agentes Especializados - SOLUCIÓN COMPLETA

Este módulo implementa un sistema de routing que:
- Clasifica consultas de usuarios en categorías
- Dirige cada consulta al agente especializado apropiado
- Coordina múltiples agentes especializados

Conceptos implementados:
- Pattern Routing
- Clasificación con LLM
- Agentes especializados con prompts focalizados
- Conditional edges con múltiples destinos
"""

from typing import TypedDict, Literal
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

# Cargar variables de entorno
load_dotenv()

# =============================================================================
# DEFINICIÓN DEL ESTADO
# =============================================================================

class RouterState(TypedDict):
    """
    Estado del sistema de routing.

    El flujo del estado a través del grafo:
    1. Usuario proporciona query
    2. Clasificador analiza y asigna category
    3. route_query() decide qué agente invocar
    4. Agente especializado procesa y genera response

    Este patrón de estado es típico en sistemas de routing:
    - Input inicial (query)
    - Metadata de routing (category)
    - Output final (response)

    Campos:
        query: Consulta original del usuario
        category: Categoría asignada ("technical", "sales", "support")
        response: Respuesta del agente especializado
    """
    query: str
    category: str
    response: str


# =============================================================================
# CONFIGURACIÓN DEL LLM
# =============================================================================

# Configurar el modelo de lenguaje
# Temperature=0 para clasificación más consistente y determinista
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0  # Determinista para clasificación
)


# =============================================================================
# NODO CLASIFICADOR
# =============================================================================

def classifier_node(state: RouterState) -> dict:
    """
    Nodo que clasifica la consulta del usuario en una categoría.

    Este es el componente más crítico del sistema de routing:
    - Si clasifica correctamente → la consulta va al agente apropiado
    - Si clasifica incorrectamente → experiencia de usuario pobre

    Estrategias para mejorar la clasificación:
    1. Prompt claro con ejemplos (few-shot)
    2. Descripciones precisas de cada categoría
    3. Pedir solo la categoría (no explicación)
    4. Temperature=0 para consistencia
    5. Validar que la respuesta sea una categoría válida

    Args:
        state: Estado con la consulta del usuario

    Returns:
        Diccionario con la categoría asignada
    """
    print("\n" + "="*70)
    print("🔍 CLASIFICADOR: Analizando consulta...")
    print("="*70)

    query = state["query"]
    print(f"Consulta: {query}")

    # Construir prompt de clasificación
    # Nota: Este prompt es crucial para el rendimiento del sistema
    prompt = f"""Analiza la siguiente consulta del cliente y clasifícala en UNA categoría.

Categorías disponibles:
- technical: Problemas técnicos, errores, bugs, no funciona, configuración, instalación, actualización
- sales: Precios, costos, productos disponibles, comparaciones, quiero comprar, planes, licencias
- support: Devoluciones, reembolsos, garantías, políticas, cambios de pedido, cancelaciones

Consulta del cliente: "{query}"

Responde SOLAMENTE con UNA palabra: technical, sales, o support.
No agregues explicación ni puntuación."""

    # Invocar el LLM
    response = llm.invoke(prompt)

    # Extraer y limpiar la categoría
    # Importante: Validar que sea una categoría válida
    category = response.content.strip().lower()

    # Validación: Si no es una categoría válida, usar default
    valid_categories = ["technical", "sales", "support"]
    if category not in valid_categories:
        print(f"⚠️  Categoría inválida '{category}', usando 'technical' como default")
        category = "technical"

    print(f"✓ Categoría detectada: {category.upper()}")
    return {"category": category}


# =============================================================================
# FUNCIÓN DE ROUTING
# =============================================================================

def route_query(state: RouterState) -> Literal["technical_agent", "sales_agent", "support_agent"]:
    """
    Función que decide a qué agente especializado enviar la consulta.

    Esta función se usa en conditional edges y su valor de retorno
    determina qué nodo se ejecutará a continuación.

    Importante:
    - El valor retornado debe coincidir EXACTAMENTE con el nombre del nodo
    - Si retorna un nombre que no existe, LangGraph lanzará un error
    - Esta función NO modifica el estado, solo decide el flujo

    Args:
        state: Estado con la categoría ya asignada

    Returns:
        Nombre del nodo del agente especializado

    Nota sobre el tipo de retorno:
    Usar Literal ayuda con type checking y autocomplete,
    pero no es estrictamente necesario.
    """
    category = state["category"]

    # Mapeo directo de categoría a nodo
    # En sistemas más complejos, esto podría incluir lógica adicional
    routing_map = {
        "technical": "technical_agent",
        "sales": "sales_agent",
        "support": "support_agent"
    }

    next_node = routing_map.get(category, "technical_agent")
    print(f"→ Dirigiendo a: {next_node.upper().replace('_', ' ')}")

    return next_node


# =============================================================================
# AGENTES ESPECIALIZADOS
# =============================================================================

def technical_agent(state: RouterState) -> dict:
    """
    Agente especializado en consultas técnicas.

    Este agente tiene un prompt específico que lo hace experto en:
    - Diagnosticar problemas técnicos
    - Resolver errores y bugs
    - Explicar configuración y setup
    - Proporcionar soluciones paso a paso

    La clave de un buen agente especializado:
    1. System prompt muy específico a su dominio
    2. Tono y estilo apropiados (técnico pero accesible)
    3. Estructura de respuesta predecible
    4. Conocimiento enfocado

    Args:
        state: Estado con la consulta técnica

    Returns:
        Diccionario con la respuesta técnica
    """
    print("\n" + "="*70)
    print("🔧 AGENTE TÉCNICO: Procesando consulta...")
    print("="*70)

    query = state["query"]

    # System prompt específico para agente técnico
    # Nota: Este prompt define el "expertise" del agente
    system_prompt = """Eres un experto técnico de soporte de primera línea.

Tu especialidad:
- Diagnosticar y resolver problemas técnicos
- Explicar soluciones de manera clara y paso a paso
- Proporcionar workarounds cuando no hay solución inmediata
- Ser técnico pero accesible

Tu estilo de respuesta:
1. Primero, muestra empatía con el problema
2. Identifica la causa probable
3. Proporciona una solución paso a paso
4. Ofrece alternativas si es relevante
5. Pregunta si necesitan más ayuda

Siempre sé claro, técnico pero no condescendiente."""

    # Construir mensajes
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=query)
    ]

    # Invocar el LLM con el contexto técnico
    response = llm.invoke(messages)
    response_content = response.content

    # Logging para debugging
    print(f"Respuesta: {response_content[:150]}...")

    return {"response": response_content}


def sales_agent(state: RouterState) -> dict:
    """
    Agente especializado en consultas de ventas.

    Este agente es experto en:
    - Información de productos y precios
    - Comparaciones de productos
    - Recomendaciones de compra
    - Promociones y ofertas

    Diferencias con el agente técnico:
    - Tono más entusiasta (pero honesto)
    - Enfoque en valor y beneficios
    - Guía en el proceso de compra
    - Conocimiento de pricing y opciones

    Args:
        state: Estado con la consulta de ventas

    Returns:
        Diccionario con la respuesta de ventas
    """
    print("\n" + "="*70)
    print("💰 AGENTE DE VENTAS: Procesando consulta...")
    print("="*70)

    query = state["query"]

    # System prompt específico para agente de ventas
    system_prompt = """Eres un experto en ventas y productos de la empresa.

Tu especialidad:
- Conocimiento profundo de todos los productos y planes
- Información actualizada de precios y promociones
- Habilidad para recomendar el producto perfecto para cada necesidad
- Proceso de compra y opciones de pago

Tu estilo de respuesta:
1. Muestra entusiasmo genuino (pero no exagerado)
2. Enfócate en el valor y beneficios para el cliente
3. Proporciona comparaciones cuando sea útil
4. Menciona promociones o descuentos aplicables
5. Facilita el siguiente paso (cómo comprar)

Siempre sé honesto, útil y orientado al cliente. No presiones, asesora."""

    # Construir mensajes
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=query)
    ]

    # Invocar el LLM con el contexto de ventas
    response = llm.invoke(messages)
    response_content = response.content

    print(f"Respuesta: {response_content[:150]}...")

    return {"response": response_content}


def support_agent(state: RouterState) -> dict:
    """
    Agente especializado en consultas de soporte.

    Este agente es experto en:
    - Políticas de devolución y garantías
    - Procesos de reembolso
    - Cambios y ajustes de pedidos
    - Resolución de problemas post-compra

    Características especiales:
    - Máxima empatía (el cliente puede estar frustrado)
    - Conocimiento de políticas y procedimientos
    - Habilidad para resolver situaciones delicadas
    - Enfoque en la satisfacción del cliente

    Args:
        state: Estado con la consulta de soporte

    Returns:
        Diccionario con la respuesta de soporte
    """
    print("\n" + "="*70)
    print("🤝 AGENTE DE SOPORTE: Procesando consulta...")
    print("="*70)

    query = state["query"]

    # System prompt específico para agente de soporte
    system_prompt = """Eres un especialista en soporte al cliente y políticas de la empresa.

Tu especialidad:
- Políticas de devolución, garantías y reembolsos
- Procesos de cambio y ajuste de pedidos
- Resolución de problemas post-compra
- Situaciones delicadas que requieren empatía

Tu estilo de respuesta:
1. Muestra empatía profunda con la situación del cliente
2. Explica las políticas relevantes de manera clara
3. Detalla el proceso paso a paso
4. Proporciona plazos y expectativas realistas
5. Ofrece opciones cuando sea posible

Siempre prioriza la satisfacción del cliente dentro de las políticas.
Sé empático, claro y proactivo en ofrecer soluciones."""

    # Construir mensajes
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=query)
    ]

    # Invocar el LLM con el contexto de soporte
    response = llm.invoke(messages)
    response_content = response.content

    print(f"Respuesta: {response_content[:150]}...")

    return {"response": response_content}


# =============================================================================
# CONSTRUCCIÓN DEL GRAFO
# =============================================================================

def build_graph():
    """
    Construye el grafo del sistema de routing.

    Este grafo implementa el pattern routing:
    1. Todas las consultas pasan por el clasificador
    2. El clasificador determina la categoría
    3. route_query() decide el agente apropiado
    4. El agente especializado procesa la consulta
    5. El sistema retorna la respuesta

    Características del grafo:
    - Un solo entry point (classifier)
    - Múltiples nodos especializados (agents)
    - Conditional edges para routing dinámico
    - Todos los agentes terminan en END

    Arquitectura:
                    ┌──────────────┐
        START  ──>  │ Classifier   │
                    └──────┬───────┘
                           │
                    [route_query()]
                           │
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
    │  Technical  │ │   Sales     │ │   Support   │
    │   Agent     │ │   Agent     │ │   Agent     │
    └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
           │               │               │
           └───────────────┼───────────────┘
                           ▼
                          END

    Returns:
        Grafo compilado listo para ejecutar
    """
    # Crear el grafo con el tipo de estado
    workflow = StateGraph(RouterState)

    # Agregar nodos
    # El clasificador es el único nodo que todos ejecutan
    workflow.add_node("classifier", classifier_node)

    # Agregar los tres agentes especializados
    workflow.add_node("technical_agent", technical_agent)
    workflow.add_node("sales_agent", sales_agent)
    workflow.add_node("support_agent", support_agent)

    # Establecer el clasificador como punto de entrada
    # Todas las consultas comienzan aquí
    workflow.set_entry_point("classifier")

    # Agregar conditional edges desde el clasificador
    # route_query() retorna el nombre del nodo a ejecutar
    workflow.add_conditional_edges(
        "classifier",          # Desde este nodo
        route_query,          # Función que decide el siguiente nodo
        {
            # Mapeo de valor retornado → nodo destino
            # Estos valores deben coincidir con lo que retorna route_query()
            "technical_agent": "technical_agent",
            "sales_agent": "sales_agent",
            "support_agent": "support_agent"
        }
    )

    # Conectar todos los agentes a END
    # Una vez que un agente responde, el flujo termina
    workflow.add_edge("technical_agent", END)
    workflow.add_edge("sales_agent", END)
    workflow.add_edge("support_agent", END)

    # Compilar y retornar el grafo
    return workflow.compile()


# =============================================================================
# EJECUCIÓN DEL SISTEMA
# =============================================================================

def main():
    """
    Función principal que demuestra el sistema de routing
    con diferentes tipos de consultas.

    Este demo muestra:
    1. Consultas de diferentes categorías
    2. Cómo el clasificador determina la categoría
    3. Cómo cada agente responde con su expertise
    4. El flujo completo del sistema
    """
    print("\n" + "="*70)
    print("🚀 SISTEMA DE ROUTING MULTI-AGENTE")
    print("="*70)

    # Construir el grafo
    app = build_graph()

    # Consultas de prueba que cubren los tres tipos
    # Estas consultas están diseñadas para ser claramente
    # clasificables en cada categoría
    test_queries = [
        # Consultas técnicas - Keywords: error, no funciona, configurar
        "Mi aplicación no inicia, me da error 404 al intentar acceder",
        "¿Cómo configuro la autenticación de dos factores en mi cuenta?",

        # Consultas de ventas - Keywords: costo, precio, comprar, planes
        "¿Cuánto cuesta el plan empresarial y qué incluye?",
        "Quiero comprar 10 licencias para mi equipo, ¿hay descuento por volumen?",

        # Consultas de soporte - Keywords: devolver, garantía, reembolso
        "Necesito devolver un producto que compré hace 2 semanas",
        "¿Cuál es su política de garantía? Mi producto dejó de funcionar",
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*70}")
        print(f"📝 CONSULTA {i}/{len(test_queries)}")
        print('='*70)

        # Crear estado inicial
        # Solo necesitamos proporcionar la query
        # Los demás campos se llenarán durante la ejecución
        initial_state = {
            "query": query,
            "category": "",
            "response": ""
        }

        # Ejecutar el sistema de routing
        # El grafo:
        # 1. Clasificará la consulta
        # 2. Dirigirá al agente apropiado
        # 3. El agente generará la respuesta
        final_state = app.invoke(initial_state)

        # Mostrar resultados
        print(f"\n✅ RESULTADO:")
        print(f"Consulta: {final_state['query']}")
        print(f"Categoría: {final_state['category'].upper()}")
        print(f"\nRespuesta del agente {final_state['category']}:")
        print(f"{final_state['response']}")

        # Pausa entre consultas para mejor lectura
        if i < len(test_queries):
            input("\n[Presiona Enter para continuar...]")

    print("\n" + "="*70)
    print("🎉 ¡Ejercicio completado!")
    print("="*70)
    print("\n💡 Observaciones:")
    print("   • Cada consulta fue dirigida al agente especializado correcto")
    print("   • Cada agente respondió con expertise en su dominio")
    print("   • El sistema es escalable: fácil agregar más agentes")
    print("   • El routing es transparente y debuggeable")


if __name__ == "__main__":
    main()
