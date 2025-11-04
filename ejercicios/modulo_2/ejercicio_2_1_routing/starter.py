"""
Ejercicio 2.1: Sistema de Routing con Agentes Especializados

Este módulo implementa un sistema de routing que:
- Clasifica consultas de usuarios en categorías
- Dirige cada consulta al agente especializado apropiado
- Coordina múltiples agentes especializados

Conceptos clave:
- Pattern Routing
- Clasificación con LLM
- Agentes especializados
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
# PASO 1: DEFINICIÓN DEL ESTADO
# =============================================================================

class RouterState(TypedDict):
    """
    Estado del sistema de routing.

    El flujo del estado es:
    1. Usuario proporciona query
    2. Clasificador determina category
    3. Agente especializado genera response

    Campos:
        query: Consulta original del usuario
        category: Categoría asignada ("technical", "sales", "support")
        response: Respuesta del agente especializado
    """
    query: str
    category: str
    response: str


# =============================================================================
# PASO 2: CONFIGURACIÓN DEL LLM
# =============================================================================

# Configurar el modelo de lenguaje
# Usamos temperature=0 para clasificación más consistente
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0  # Determinista para clasificación
)


# =============================================================================
# PASO 3: NODO CLASIFICADOR
# =============================================================================

def classifier_node(state: RouterState) -> dict:
    """
    Nodo que clasifica la consulta del usuario en una categoría.

    Este es el "router" del sistema. Su trabajo es:
    1. Analizar la consulta del usuario
    2. Determinar si es técnica, de ventas, o de soporte
    3. Retornar la categoría apropiada

    La calidad de este nodo es crucial: si clasifica mal,
    la consulta irá al agente incorrecto.

    Args:
        state: Estado con la consulta del usuario

    Returns:
        Diccionario con la categoría asignada

    Ejemplo:
        query: "Mi app no inicia" → category: "technical"
        query: "¿Cuánto cuesta?" → category: "sales"
        query: "Quiero devolver un producto" → category: "support"
    """
    print("\n" + "="*70)
    print("🔍 CLASIFICADOR: Analizando consulta...")
    print("="*70)

    query = state["query"]
    print(f"Consulta: {query}")

    # TODO: Implementar clasificación de la consulta
    #
    # Pasos:
    # 1. Crear un prompt que explique las categorías al LLM
    # 2. Pedir al LLM que clasifique la consulta
    # 3. Parsear la respuesta para obtener la categoría
    # 4. Retornar la categoría (debe ser: "technical", "sales", o "support")
    #
    # Categorías:
    # - "technical": Problemas técnicos, errores, bugs, configuración
    # - "sales": Precios, productos, comparaciones, quiero comprar
    # - "support": Devoluciones, garantías, políticas, reembolsos
    #
    # Pista: Usa un prompt que pida una respuesta de UNA SOLA PALABRA

    # Ejemplo de estructura del prompt:
    # prompt = f"""Clasifica la siguiente consulta en UNA categoría.
    #
    # Categorías posibles:
    # - technical: [descripción]
    # - sales: [descripción]
    # - support: [descripción]
    #
    # Consulta: {query}
    #
    # Responde SOLO con: technical, sales, o support"""

    # Tu código aquí:
    category = "technical"  # TODO: Reemplazar con clasificación real

    print(f"✓ Categoría detectada: {category}")
    return {"category": category}


# =============================================================================
# PASO 4: FUNCIÓN DE ROUTING
# =============================================================================

def route_query(state: RouterState) -> Literal["technical_agent", "sales_agent", "support_agent"]:
    """
    Función que decide a qué agente especializado enviar la consulta.

    Esta función se ejecuta después del clasificador y determina
    el flujo del grafo usando conditional edges.

    Args:
        state: Estado con la categoría ya asignada

    Returns:
        Nombre del nodo del agente especializado

    Nota: El valor retornado debe coincidir exactamente con el nombre
    del nodo en el grafo.
    """
    # TODO: Implementar routing basado en la categoría
    #
    # Pasos:
    # 1. Obtener la categoría del estado
    # 2. Mapear la categoría al nombre del nodo correspondiente
    # 3. Retornar el nombre del nodo
    #
    # Mapeo:
    # - "technical" → "technical_agent"
    # - "sales" → "sales_agent"
    # - "support" → "support_agent"
    #
    # Pista: Usa un diccionario para mapear categorías a nodos

    category = state["category"]

    # Tu código aquí:
    # Crear mapeo de categoría → nodo
    # Retornar el nodo apropiado

    print(f"→ Dirigiendo a: [nodo correspondiente]")
    return "technical_agent"  # TODO: Implementar lógica real


# =============================================================================
# PASO 5: AGENTES ESPECIALIZADOS
# =============================================================================

def technical_agent(state: RouterState) -> dict:
    """
    Agente especializado en consultas técnicas.

    Este agente es experto en:
    - Diagnosticar problemas técnicos
    - Resolver errores y bugs
    - Explicar configuración y setup
    - Proporcionar soluciones paso a paso

    Args:
        state: Estado con la consulta técnica

    Returns:
        Diccionario con la respuesta técnica
    """
    print("\n" + "="*70)
    print("🔧 AGENTE TÉCNICO: Procesando consulta...")
    print("="*70)

    query = state["query"]

    # TODO: Implementar el agente técnico
    #
    # Pasos:
    # 1. Crear un system prompt que defina el rol del agente técnico
    # 2. Invocar el LLM con el system prompt y la consulta
    # 3. Retornar la respuesta
    #
    # El system prompt debe:
    # - Definir claramente el rol (experto técnico)
    # - Especificar el estilo de respuesta (paso a paso, claro)
    # - Guiar el tipo de información a proporcionar
    #
    # Pista: Usa SystemMessage para el prompt del sistema
    #        y HumanMessage para la consulta del usuario

    # Ejemplo de estructura:
    # system_prompt = """Eres un experto técnico de soporte...
    # [Define el rol y estilo]"""
    #
    # messages = [
    #     SystemMessage(content=system_prompt),
    #     HumanMessage(content=query)
    # ]
    #
    # response = llm.invoke(messages)

    # Tu código aquí:
    response_content = "TODO: Implementar agente técnico"

    print(f"Respuesta: {response_content[:100]}...")
    return {"response": response_content}


def sales_agent(state: RouterState) -> dict:
    """
    Agente especializado en consultas de ventas.

    Este agente es experto en:
    - Información de productos y precios
    - Comparaciones de productos
    - Recomendaciones de compra
    - Promociones y ofertas

    Args:
        state: Estado con la consulta de ventas

    Returns:
        Diccionario con la respuesta de ventas
    """
    print("\n" + "="*70)
    print("💰 AGENTE DE VENTAS: Procesando consulta...")
    print("="*70)

    query = state["query"]

    # TODO: Implementar el agente de ventas
    #
    # Similar al agente técnico, pero con un prompt diferente
    # enfocado en ventas y productos.
    #
    # El system prompt debe:
    # - Definir el rol como experto en ventas
    # - Ser entusiasta pero honesto
    # - Conocer productos, precios y promociones
    # - Ayudar al cliente a tomar la mejor decisión

    # Tu código aquí:
    response_content = "TODO: Implementar agente de ventas"

    print(f"Respuesta: {response_content[:100]}...")
    return {"response": response_content}


def support_agent(state: RouterState) -> dict:
    """
    Agente especializado en consultas de soporte.

    Este agente es experto en:
    - Políticas de devolución y garantías
    - Procesos de reembolso
    - Cambios y ajustes de pedidos
    - Resolución de problemas post-compra

    Args:
        state: Estado con la consulta de soporte

    Returns:
        Diccionario con la respuesta de soporte
    """
    print("\n" + "="*70)
    print("🤝 AGENTE DE SOPORTE: Procesando consulta...")
    print("="*70)

    query = state["query"]

    # TODO: Implementar el agente de soporte
    #
    # Similar a los anteriores, pero enfocado en soporte
    # y políticas de la empresa.
    #
    # El system prompt debe:
    # - Ser empático y servicial
    # - Conocer políticas de devolución, garantías, etc.
    # - Explicar procesos claramente
    # - Resolver situaciones post-compra

    # Tu código aquí:
    response_content = "TODO: Implementar agente de soporte"

    print(f"Respuesta: {response_content[:100]}...")
    return {"response": response_content}


# =============================================================================
# PASO 6: CONSTRUCCIÓN DEL GRAFO
# =============================================================================

def build_graph():
    """
    Construye el grafo del sistema de routing.

    Arquitectura del grafo:

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
    # Crear el grafo
    workflow = StateGraph(RouterState)

    # TODO: Construir el grafo
    #
    # Pasos:
    # 1. Agregar nodo "classifier" que ejecuta classifier_node
    # 2. Agregar nodo "technical_agent" que ejecuta technical_agent
    # 3. Agregar nodo "sales_agent" que ejecuta sales_agent
    # 4. Agregar nodo "support_agent" que ejecuta support_agent
    # 5. Establecer "classifier" como entry point
    # 6. Agregar conditional edges desde "classifier" usando route_query
    # 7. Conectar cada agente a END
    #
    # Pista: Para conditional edges, usa esta sintaxis:
    # workflow.add_conditional_edges(
    #     "nodo_origen",
    #     funcion_de_decision,
    #     {
    #         "valor_retornado_1": "nodo_destino_1",
    #         "valor_retornado_2": "nodo_destino_2",
    #         ...
    #     }
    # )

    # Tu código aquí:
    # workflow.add_node(...)
    # workflow.set_entry_point(...)
    # workflow.add_conditional_edges(...)
    # workflow.add_edge(...)

    # Compilar el grafo
    return workflow.compile()


# =============================================================================
# PASO 7: EJECUCIÓN DEL SISTEMA
# =============================================================================

def main():
    """
    Función principal que demuestra el sistema de routing
    con diferentes tipos de consultas.
    """
    print("\n" + "="*70)
    print("🚀 SISTEMA DE ROUTING MULTI-AGENTE")
    print("="*70)

    # Construir el grafo
    app = build_graph()

    # Consultas de prueba que cubren los tres tipos
    test_queries = [
        # Consultas técnicas
        "Mi aplicación no inicia, me da error 404",
        "¿Cómo configuro la autenticación de dos factores?",

        # Consultas de ventas
        "¿Cuánto cuesta el plan empresarial?",
        "Quiero comprar 10 licencias, ¿hay descuento?",

        # Consultas de soporte
        "Necesito devolver un producto que compré hace 2 semanas",
        "¿Cuál es su política de garantía?",
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*70}")
        print(f"📝 CONSULTA {i}/{len(test_queries)}")
        print('='*70)

        # Crear estado inicial
        initial_state = {
            "query": query,
            "category": "",
            "response": ""
        }

        # Ejecutar el sistema de routing
        final_state = app.invoke(initial_state)

        # Mostrar resultados
        print(f"\n✅ RESULTADO:")
        print(f"Consulta: {final_state['query']}")
        print(f"Categoría: {final_state['category']}")
        print(f"\nRespuesta del agente:")
        print(f"{final_state['response']}")

        # Pausa entre consultas
        if i < len(test_queries):
            input("\n[Presiona Enter para continuar...]")

    print("\n" + "="*70)
    print("🎉 ¡Ejercicio completado!")
    print("="*70)


if __name__ == "__main__":
    main()
