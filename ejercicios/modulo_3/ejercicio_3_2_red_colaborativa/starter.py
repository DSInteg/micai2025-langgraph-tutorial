"""
Ejercicio 3.2: Red Colaborativa con Handoffs - STARTER

Implementa una red de agentes especializados que colaboran mediante handoffs.
"""

from typing import TypedDict, Literal, List, Dict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()

# =============================================================================
# ESTADO COMPARTIDO
# =============================================================================

class CollaborativeState(TypedDict):
    """
    Estado compartido entre todos los agentes colaborativos.

    Este estado permite que cada agente vea:
    - Qué se ha hecho antes (conversation_history)
    - Qué encontraron otros agentes (specialist_reports)
    - Quién tiene el control ahora (current_agent)
    """
    # TODO: Define los campos del estado
    # - query: str (consulta original del usuario)
    # - current_agent: str (agente que tiene el control actualmente)
    # - conversation_history: List[Dict] (historial de todas las acciones)
    # - specialist_reports: Dict[str, str] (reportes por especialista)
    # - handoff_reason: str (razón del último handoff)
    # - final_response: str (respuesta final sintetizada)
    pass


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# =============================================================================
# AGENTE DE TRIAGE
# =============================================================================

def triage_agent(state: CollaborativeState) -> dict:
    """
    Agente de triage que analiza la consulta y deriva al especialista apropiado.

    Este agente es el punto de entrada del sistema.
    Su trabajo es entender la naturaleza del problema y decidir
    qué especialista debe atenderlo primero.

    Categorías de especialistas:
    - code: Problemas de código, bugs, errores de programación
    - network: Problemas de conectividad, DNS, firewall, puertos
    - security: Vulnerabilidades, permisos, autenticación, cifrado

    Args:
        state: Estado actual con la consulta del usuario

    Returns:
        dict con current_agent actualizado y entrada en conversation_history
    """
    print("\n" + "="*70)
    print("🎯 TRIAGE AGENT: Analizando consulta...")
    print("="*70)

    query = state["query"]

    # TODO: Implementa la clasificación usando el LLM
    # 1. Crear prompt que pida clasificar en CODE, NETWORK, o SECURITY
    # 2. Invocar el LLM
    # 3. Extraer la categoría de la respuesta
    # 4. Mapear la categoría a nombre de agente: code_agent, network_agent, security_agent
    # 5. Actualizar conversation_history con la decisión

    # HINT: El prompt debe ser claro sobre las tres categorías
    # HINT: Usa .strip().upper() para normalizar la respuesta del LLM

    prompt = ""  # TODO: Crear prompt de clasificación

    # TODO: Invocar LLM y procesar respuesta

    print(f"   → Consulta clasificada como: [CATEGORY]")
    print(f"   → Derivando a: [AGENT_NAME]")

    # TODO: Retornar estado actualizado
    return {}


# =============================================================================
# AGENTES ESPECIALISTAS
# =============================================================================

def code_agent(state: CollaborativeState) -> dict:
    """
    Agente especialista en problemas de código.

    Este agente analiza problemas relacionados con:
    - Bugs y errores de programación
    - Lógica de código
    - Frameworks y bibliotecas
    - Optimización de código

    Puede decidir hacer handoff si:
    - Detecta que el problema también tiene componente de red
    - Detecta que hay implicaciones de seguridad
    """
    print("\n💻 CODE AGENT: Analizando desde perspectiva de código...")

    query = state["query"]
    history = state.get("conversation_history", [])
    reports = state.get("specialist_reports", {})

    # TODO: Implementa el análisis de código
    # 1. Crear prompt que pida analizar la consulta desde perspectiva de código
    # 2. Incluir contexto del historial y reportes previos
    # 3. Generar reporte detallado
    # 4. Decidir si puede resolver completamente o necesita handoff
    # 5. Actualizar specialist_reports con tu reporte
    # 6. Actualizar current_agent con el próximo agente (o "final")
    # 7. Actualizar conversation_history

    # HINT: El análisis debe ser específico sobre aspectos de código
    # HINT: Decidir handoff preguntando: "¿Hay aspectos de red/seguridad que necesitan expertise?"

    # TODO: Implementar

    print(f"   ✓ Reporte generado")
    print(f"   → Próximo agente: [NEXT_AGENT]")

    return {}


def network_agent(state: CollaborativeState) -> dict:
    """
    Agente especialista en problemas de red.

    Este agente analiza problemas relacionados con:
    - Conectividad
    - DNS y resolución de nombres
    - Firewalls y puertos
    - Protocolos de red
    - Latencia y performance de red
    """
    print("\n🔧 NETWORK AGENT: Analizando desde perspectiva de red...")

    query = state["query"]
    history = state.get("conversation_history", [])
    reports = state.get("specialist_reports", {})

    # TODO: Implementa el análisis de red
    # Similar a code_agent pero enfocado en networking

    # HINT: Considera aspectos como: conectividad, puertos, DNS, firewalls
    # HINT: Puede hacer handoff a security_agent si detecta problemas de seguridad

    # TODO: Implementar

    print(f"   ✓ Reporte generado")
    print(f"   → Próximo agente: [NEXT_AGENT]")

    return {}


def security_agent(state: CollaborativeState) -> dict:
    """
    Agente especialista en seguridad.

    Este agente analiza problemas relacionados con:
    - Vulnerabilidades
    - Autenticación y autorización
    - Cifrado y protección de datos
    - Permisos y control de acceso
    - Certificados y PKI
    """
    print("\n🔒 SECURITY AGENT: Analizando desde perspectiva de seguridad...")

    query = state["query"]
    history = state.get("conversation_history", [])
    reports = state.get("specialist_reports", {})

    # TODO: Implementa el análisis de seguridad
    # Similar a code_agent pero enfocado en security

    # HINT: Considera aspectos como: vulnerabilidades, autenticación, permisos, cifrado
    # HINT: Puede hacer handoff a code_agent si necesita analizar código específico

    # TODO: Implementar

    print(f"   ✓ Reporte generado")
    print(f"   → Próximo agente: [NEXT_AGENT]")

    return {}


# =============================================================================
# AGENTE FINAL
# =============================================================================

def final_agent(state: CollaborativeState) -> dict:
    """
    Agente final que sintetiza todos los reportes en una respuesta coherente.

    Este agente integra:
    - Todos los specialist_reports
    - El conversation_history completo
    - La consulta original

    Y genera una respuesta final que:
    - Sea coherente y bien estructurada
    - Integre todas las perspectivas
    - Proporcione soluciones accionables
    - No pierda información crítica de ningún especialista
    """
    print("\n" + "="*70)
    print("✅ FINAL AGENT: Sintetizando respuesta final...")
    print("="*70)

    query = state["query"]
    reports = state.get("specialist_reports", {})
    history = state.get("conversation_history", [])

    # TODO: Implementa la síntesis final
    # 1. Recopilar todos los reportes de especialistas
    # 2. Crear prompt que pida integrar todas las perspectivas
    # 3. Generar respuesta final unificada
    # 4. Actualizar final_response

    # HINT: El prompt debe enfatizar integración, no concatenación
    # HINT: La respuesta debe ser ejecutiva y accionable

    # TODO: Implementar

    print(f"   ✓ Respuesta final generada ({len('final_response')} caracteres)")

    return {}


# =============================================================================
# FUNCIONES DE ROUTING
# =============================================================================

def route_from_triage(state: CollaborativeState) -> Literal["code", "network", "security"]:
    """
    Determina a qué especialista derivar desde el triage.

    Lee current_agent del estado y mapea a nombre de nodo.
    """
    # TODO: Implementar routing
    # Mapear current_agent a nombre de nodo:
    # - "code_agent" -> "code"
    # - "network_agent" -> "network"
    # - "security_agent" -> "security"

    current = state["current_agent"]

    # TODO: Implementar mapeo

    print(f"   → Routing desde triage a: [TARGET]")

    return "code"  # TODO: Retornar el nodo correcto


def route_from_specialist(state: CollaborativeState) -> Literal["code", "network", "security", "final"]:
    """
    Determina el siguiente agente desde un especialista.

    Los especialistas pueden hacer handoff a:
    - Otro especialista (si necesitan ayuda)
    - Final agent (si pueden terminar)
    """
    # TODO: Implementar routing
    # Leer current_agent y mapear a nodo destino
    # - Si current_agent es "final" -> "final"
    # - Si es otro especialista -> mapear a su nodo

    current = state["current_agent"]

    # TODO: Implementar mapeo

    print(f"   → Routing desde especialista a: [TARGET]")

    return "final"  # TODO: Retornar el nodo correcto


# =============================================================================
# CONSTRUCCIÓN DEL GRAFO
# =============================================================================

def build_graph():
    """
    Construye el grafo de red colaborativa con handoffs.

    Arquitectura:
    - Entry: triage_agent
    - Conditional edge: triage -> [code, network, security]
    - Conditional edges: cada especialista -> [otro especialista o final]
    - Edge: final -> END

    Los handoffs se implementan mediante conditional edges que permiten
    a cada agente decidir dinámicamente el próximo paso.
    """
    workflow = StateGraph(CollaborativeState)

    # TODO: Agregar nodos
    # - triage_agent
    # - code_agent (nodo "code")
    # - network_agent (nodo "network")
    # - security_agent (nodo "security")
    # - final_agent (nodo "final")

    # TODO: Set entry point a "triage"

    # TODO: Conditional edge desde triage a especialistas
    # workflow.add_conditional_edges(
    #     "triage",
    #     route_from_triage,
    #     {...}
    # )

    # TODO: Conditional edges desde cada especialista
    # Cada especialista puede ir a otro especialista o a final
    # workflow.add_conditional_edges(
    #     "code",
    #     route_from_specialist,
    #     {...}
    # )
    # (Repetir para "network" y "security")

    # TODO: Edge de final a END

    return workflow.compile()


# =============================================================================
# EJECUCIÓN Y DEMO
# =============================================================================

def main():
    print("\n" + "="*70)
    print("🤝 RED COLABORATIVA CON HANDOFFS")
    print("="*70)

    queries = [
        "Mi aplicación web no puede conectarse a la base de datos. El código usa SQLAlchemy y parece que hay un problema de autenticación, pero el firewall también podría estar bloqueando el puerto 5432.",
        "Tengo un bug en mi función de login que permite a usuarios acceder sin credenciales correctas.",
        "El servidor no responde en el puerto 443, creo que hay un problema con el certificado SSL."
    ]

    app = build_graph()

    for i, query in enumerate(queries, 1):
        print(f"\n{'='*70}")
        print(f"📋 CONSULTA {i}:")
        print(f"{'='*70}")
        print(f"{query}")

        initial_state = {
            "query": query,
            "current_agent": "",
            "conversation_history": [],
            "specialist_reports": {},
            "handoff_reason": "",
            "final_response": ""
        }

        # TODO: Invocar el grafo
        # final_state = app.invoke(initial_state, {"recursion_limit": 20})

        # TODO: Mostrar resultado
        # print("\n" + "="*70)
        # print("📊 RESPUESTA FINAL")
        # print("="*70)
        # print(final_state["final_response"])

        # TODO: Mostrar estadísticas
        # print(f"\n📈 Flujo de colaboración:")
        # for entry in final_state["conversation_history"]:
        #     print(f"   {entry['agent']} → {entry.get('handoff_to', 'FIN')}")

        if i < len(queries):
            input("\n[Presiona Enter para continuar...]")


if __name__ == "__main__":
    main()
