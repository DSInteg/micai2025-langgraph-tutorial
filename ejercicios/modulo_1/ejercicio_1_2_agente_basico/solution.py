"""
Ejercicio 1.2: Agente Básico Autónomo con Herramientas - SOLUCIÓN COMPLETA

Este módulo implementa un agente que puede:
- Razonar sobre qué herramientas necesita
- Ejecutar herramientas dinámicamente
- Decidir cuándo ha completado su tarea

Conceptos implementados:
- ReAct pattern (Reasoning + Acting)
- Tool calling y tool binding
- Conditional edges
- Ciclos en grafos
- ToolNode para ejecución de herramientas
"""

from typing import Annotated, Sequence, Literal
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

# Cargar variables de entorno
load_dotenv()

# =============================================================================
# DEFINICIÓN DEL ESTADO DEL AGENTE
# =============================================================================

class AgentState(dict):
    """
    Estado del agente con historial de mensajes.

    A diferencia del Ejercicio 1.1 donde usábamos campos específicos (article,
    summary, etc.), los agentes usan una secuencia de mensajes porque:

    1. Permite al LLM ver todo el contexto de la conversación
    2. Incluye diferentes tipos de mensajes:
       - HumanMessage: Mensajes del usuario
       - AIMessage: Respuestas del agente
       - SystemMessage: Instrucciones del sistema
       - ToolMessage: Resultados de herramientas

    El decorator Annotated con add_messages es un "reducer" especial:
    - Automáticamente agrega nuevos mensajes al final
    - No duplica mensajes con el mismo ID
    - Mantiene el orden cronológico
    - Permite al estado evolucionar a través del grafo

    Ejemplo de flujo de mensajes:
    [HumanMessage("¿cuánto es 2+2?")]
    → [HumanMessage("¿cuánto es 2+2?"), AIMessage(tool_calls=[calculator])]
    → [..., ToolMessage("4")]
    → [..., AIMessage("El resultado es 4")]
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]


# =============================================================================
# DEFINICIÓN DE HERRAMIENTAS
# =============================================================================

@tool
def calculator(expression: str) -> str:
    """
    Calcula expresiones matemáticas simples.

    El decorator @tool convierte una función Python en una herramienta que:
    1. El LLM puede descubrir y entender
    2. Tiene un esquema JSON automático basado en los type hints
    3. Incluye la docstring como descripción para el LLM

    Esta herramienta puede evaluar:
    - Operaciones básicas: +, -, *, /
    - Porcentajes: "15% of 250"
    - Potencias: 2**3
    - Paréntesis para precedencia

    Args:
        expression: Expresión matemática como string (ej: "2 + 2", "15% of 250")

    Returns:
        Resultado del cálculo como string

    Ejemplos:
        calculator("2 + 2") → "4"
        calculator("15% of 250") → "37.5"
        calculator("(10 + 5) * 2") → "30"
    """
    try:
        # Manejar porcentajes: "X% of Y" → (X/100) * Y
        if "%" in expression and "of" in expression:
            parts = expression.replace("%", "").split("of")
            if len(parts) == 2:
                percent = float(parts[0].strip())
                number = float(parts[1].strip())
                result = (percent / 100) * number
                return str(result)

        # Evaluar expresión matemática
        # NOTA: En producción, usar una librería más segura que eval()
        # como simpleeval o crear un parser propio
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error al calcular: {str(e)}"


@tool
def search_knowledge(query: str) -> str:
    """
    Busca información en una base de conocimiento simulada.

    Esta es una simulación simple de una base de datos.
    En un sistema real, esto podría:
    - Consultar una base de datos SQL
    - Buscar en documentos con RAG (Retrieval-Augmented Generation)
    - Llamar a una API externa
    - Consultar un vector store

    Args:
        query: Consulta de búsqueda (ej: "precio producto X")

    Returns:
        Información encontrada o mensaje de no encontrado

    Ejemplos:
        search_knowledge("precio producto X") → "El precio del producto X es $120"
        search_knowledge("horario tienda") → "La tienda abre de 9:00 a 18:00"
    """
    # Base de conocimiento simulada (en producción sería una DB real)
    knowledge_base = {
        "producto x": "El precio del producto X es $120",
        "producto y": "El precio del producto Y es $85",
        "producto z": "El precio del producto Z es $200",
        "horario": "La tienda abre de 9:00 a 18:00, de lunes a sábado",
        "envío": "El envío es gratuito para compras superiores a $100",
        "garantía": "Todos los productos tienen garantía de 1 año",
        "devoluciones": "Aceptamos devoluciones dentro de los 30 días",
    }

    # Buscar en la base de conocimiento (búsqueda simple por substring)
    query_lower = query.lower()
    for key, value in knowledge_base.items():
        if key in query_lower:
            return value

    return f"No se encontró información sobre: {query}"


# Lista de herramientas disponibles para el agente
tools = [calculator, search_knowledge]

# =============================================================================
# CONFIGURACIÓN DEL LLM CON HERRAMIENTAS
# =============================================================================

# Inicializar el modelo
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,  # Temperatura 0 para razonamiento más determinístico
)

# Vincular herramientas al LLM
# bind_tools() es un método especial que:
# 1. Convierte las herramientas a formato de OpenAI function calling
# 2. Las incluye en cada llamada al LLM
# 3. Permite al LLM decidir cuándo y cómo llamarlas
llm_with_tools = llm.bind_tools(tools)

# System prompt que guía el comportamiento del agente
SYSTEM_PROMPT = """Eres un asistente útil que puede realizar cálculos y buscar información.

Tienes acceso a las siguientes herramientas:
- calculator: Para realizar cálculos matemáticos
- search_knowledge: Para buscar información en la base de conocimiento

Cuando recibas una pregunta:
1. Piensa qué información necesitas
2. Usa las herramientas apropiadas
3. Una vez que tengas toda la información, proporciona una respuesta clara

Siempre explica tu razonamiento brevemente."""


# =============================================================================
# DEFINICIÓN DE NODOS
# =============================================================================

def agent_node(state: AgentState) -> dict:
    """
    Nodo del agente: razona y decide qué hacer.

    Este es el "cerebro" del agente. En cada llamada:
    1. Recibe todo el historial de mensajes (contexto completo)
    2. El LLM analiza el contexto y decide:
       - Opción A: Llamar una o más herramientas (tool_calls)
       - Opción B: Responder directamente al usuario
    3. Retorna un AIMessage con su decisión

    El LLM ve:
    - El system prompt con instrucciones
    - Todos los mensajes previos (contexto)
    - Las herramientas disponibles (via bind_tools)
    - Los resultados de herramientas previas (ToolMessages)

    Args:
        state: Estado con historial de mensajes

    Returns:
        Diccionario con el nuevo mensaje del agente
    """
    print("\n🤖 Agente pensando...")

    # 1. Obtener mensajes del estado
    messages = state["messages"]

    # 2. Agregar system prompt si es el primer mensaje del usuario
    # Solo lo agregamos una vez al inicio
    if len(messages) == 1:
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(messages)

    # 3. Invocar el LLM con herramientas vinculadas
    # El LLM decidirá si necesita usar herramientas o responder
    response = llm_with_tools.invoke(messages)

    # 4. Logging para debugging (opcional pero útil)
    if hasattr(response, "tool_calls") and response.tool_calls:
        print(f"   → El agente quiere usar {len(response.tool_calls)} herramienta(s)")
        for tc in response.tool_calls:
            print(f"      • {tc['name']}({tc['args']})")
    else:
        print("   → El agente tiene una respuesta final")

    # 5. Retornar el mensaje de respuesta
    # add_messages automáticamente lo agregará al historial
    return {"messages": [response]}


def should_continue(state: AgentState) -> Literal["continue", "end"]:
    """
    Función de routing: decide si el agente debe continuar o terminar.

    Esta es una función crucial en el pattern ReAct. Determina:
    - Si el agente quiere usar herramientas → continuar el ciclo
    - Si el agente ya tiene la respuesta → terminar

    El flujo es:
    - agent genera AIMessage con tool_calls → "continue" → ejecutar tools
    - tools generan ToolMessages → automático volver a agent
    - agent genera AIMessage sin tool_calls → "end" → terminar

    Args:
        state: Estado actual

    Returns:
        "continue" si hay herramientas por ejecutar, "end" si debe terminar
    """
    # Obtener el último mensaje (que siempre es del agente)
    last_message = state["messages"][-1]

    # Verificar si el mensaje tiene tool_calls
    # Los modelos que soportan function calling agregan este atributo
    # cuando deciden usar herramientas
    if hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0:
        print("   🔄 Hay herramientas por ejecutar, continuando...")
        return "continue"
    else:
        print("   ✅ No hay más herramientas, terminando...")
        return "end"


# =============================================================================
# CONSTRUCCIÓN DEL GRAFO
# =============================================================================

def build_graph():
    """
    Construye el grafo del agente con ciclo de razonamiento.

    Este grafo implementa el pattern ReAct:

    ┌─────────────────────────────────────┐
    │         START                        │
    └───────────────┬─────────────────────┘
                    ↓
    ┌───────────────────────────────────────┐
    │  agent_node                           │
    │  - Recibe contexto                    │
    │  - LLM decide qué hacer               │
    │  - Retorna AIMessage                  │
    └───────────────┬───────────────────────┘
                    ↓
            [should_continue?]
                ↙         ↘
          "continue"      "end"
             ↓              ↓
    ┌────────────────┐    END
    │  tool_node     │
    │  - Ejecuta     │
    │    herramientas│
    │  - Retorna     │
    │    ToolMessages│
    └────────┬───────┘
             ↓
          (volver a agent) ←─┐
                             │
                           CICLO

    Características importantes:
    1. Es un CICLO: agent → tools → agent → ...
    2. No sabemos cuántas iteraciones tomará
    3. El agente decide cuándo terminar
    4. Cada herramienta ejecutada agrega contexto

    Returns:
        Grafo compilado listo para ejecutar
    """
    # 1. Crear el grafo con el tipo de estado
    workflow = StateGraph(AgentState)

    # 2. Crear el nodo de herramientas usando ToolNode
    # ToolNode es una clase proporcionada por LangGraph que:
    # - Extrae tool_calls del último AIMessage
    # - Busca las herramientas correspondientes
    # - Las ejecuta con los argumentos especificados
    # - Retorna ToolMessages con los resultados
    # Esto nos ahorra implementar la lógica manualmente
    tool_node = ToolNode(tools=tools)

    # 3. Agregar nodos al grafo
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)

    # 4. Establecer el punto de entrada
    # El grafo siempre comienza con el agente
    workflow.set_entry_point("agent")

    # 5. Agregar conditional edge desde el agente
    # Después de que el agente razona, should_continue decide:
    # - "continue" → ejecutar herramientas
    # - "end" → terminar (el agente ya respondió)
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            "end": END
        }
    )

    # 6. Agregar edge desde tools de vuelta a agent
    # ¡ESTO CREA EL CICLO!
    # Después de ejecutar herramientas, siempre volvemos al agente
    # para que analice los resultados y decida qué hacer
    workflow.add_edge("tools", "agent")

    # 7. Compilar el grafo
    return workflow.compile()


# =============================================================================
# EJECUCIÓN DEL AGENTE
# =============================================================================

def main():
    """
    Función principal que ejecuta el agente con diferentes consultas.

    Demuestra varios casos de uso:
    1. Consulta simple (una herramienta)
    2. Consulta de búsqueda (otra herramienta)
    3. Consulta compleja (múltiples herramientas)
    4. Otra consulta de búsqueda

    Esto muestra la flexibilidad del agente para adaptarse
    a diferentes tipos de tareas sin reprogramación.
    """
    print("\n" + "="*70)
    print("🚀 AGENTE AUTÓNOMO CON HERRAMIENTAS")
    print("="*70)

    # Construir el grafo
    app = build_graph()

    # Ejemplos de consultas que requieren diferentes herramientas
    queries = [
        "¿Cuánto es 15% de 250?",
        "¿Cuál es el precio del producto X?",
        "Calcula el 20% de 450 y súmale el precio del producto Y",
        "¿Cuál es el horario de la tienda?",
    ]

    for i, query in enumerate(queries, 1):
        print(f"\n{'='*70}")
        print(f"📝 CONSULTA {i}: {query}")
        print('='*70)

        # Crear estado inicial con la consulta del usuario
        initial_state = {
            "messages": [HumanMessage(content=query)]
        }

        # Ejecutar el agente
        # El método invoke() ejecutará el grafo completo:
        # - Puede hacer múltiples iteraciones del ciclo agent → tools
        # - Continúa hasta que el agente decida terminar
        # - Retorna el estado final con todos los mensajes
        final_state = app.invoke(initial_state)

        # Mostrar la respuesta final (último mensaje)
        final_message = final_state["messages"][-1]
        print(f"\n✅ RESPUESTA FINAL:")
        print(f"{final_message.content}")
        print()

        # Información de debugging útil
        num_steps = len(final_state["messages"])
        print(f"📊 Estadísticas:")
        print(f"   • Total de mensajes: {num_steps}")
        print(f"   • Iteraciones aproximadas: {(num_steps - 1) // 2}")

        # Pequeña separación entre consultas
        if i < len(queries):
            input("\nPresiona Enter para continuar con la siguiente consulta...")

    print("\n" + "="*70)
    print("🎉 ¡Ejercicio completado! Has creado tu primer agente autónomo.")
    print("="*70)
    print("\n💡 Conceptos clave aprendidos:")
    print("   • ReAct pattern (Reasoning + Acting)")
    print("   • Tool calling y binding")
    print("   • Conditional edges para decisiones dinámicas")
    print("   • Ciclos en grafos de LangGraph")
    print("   • Diferencia entre workflows y agentes")


if __name__ == "__main__":
    main()
