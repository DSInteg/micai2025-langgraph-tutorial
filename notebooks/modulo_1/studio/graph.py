"""
Sistema de Clasificación de Tickets de Soporte
==============================================

Grafo simple que demuestra los conceptos fundamentales de LangGraph:
- State (Estado compartido)
- Nodes (Nodos de procesamiento)
- Edges (Conexiones normales)
- Conditional Edges (Routing dinámico)

Este grafo se puede abrir en LangGraph Studio para visualización interactiva.
"""

from typing_extensions import TypedDict
from typing import Literal
from langgraph.graph import StateGraph, START, END


# =============================================================================
# PASO 1: Definir el State
# =============================================================================

class TicketState(TypedDict):
    """Estado que representa un ticket de soporte a través del flujo."""

    ticket_id: str        # ID único del ticket
    mensaje: str          # Mensaje original del usuario
    prioridad: str        # "urgente" o "normal"
    estado: str           # "recibido", "clasificado", "procesado"
    asignado_a: str       # Equipo o persona asignada


# =============================================================================
# PASO 2: Crear los Nodes (Nodos)
# =============================================================================

def recibir_ticket(state: TicketState) -> dict:
    """
    Nodo 1: Recibe el ticket y lo prepara para clasificación.

    Args:
        state: Estado actual del ticket

    Returns:
        Dict con campos actualizados del state
    """
    print(f"\n📨 NODO 1: Recibiendo ticket {state['ticket_id']}")
    print(f"   Mensaje: '{state['mensaje']}'")

    # Actualizar el estado a "clasificado"
    return {
        "estado": "clasificado"
    }


def procesar_urgente(state: TicketState) -> dict:
    """
    Nodo 2: Procesa tickets urgentes con alta prioridad.

    Args:
        state: Estado actual del ticket

    Returns:
        Dict con campos actualizados
    """
    print(f"\n🚨 NODO 2: Procesando ticket URGENTE {state['ticket_id']}")
    print(f"   ⚡ Escalando al equipo de ingeniería...")

    return {
        "estado": "procesado",
        "asignado_a": "Equipo de Ingeniería",
        "prioridad": "urgente"
    }


def procesar_normal(state: TicketState) -> dict:
    """
    Nodo 3: Procesa tickets con prioridad normal.

    Args:
        state: Estado actual del ticket

    Returns:
        Dict con campos actualizados
    """
    print(f"\n📋 NODO 3: Procesando ticket NORMAL {state['ticket_id']}")
    print(f"   📌 Agregando a cola de soporte estándar...")

    return {
        "estado": "procesado",
        "asignado_a": "Equipo de Soporte L1",
        "prioridad": "normal"
    }


# =============================================================================
# PASO 3: Crear el Conditional Edge (Routing Dinámico)
# =============================================================================

def clasificar_prioridad(state: TicketState) -> Literal["procesar_urgente", "procesar_normal"]:
    """
    Conditional Edge: Decide si el ticket es urgente o normal.

    Esta función analiza el mensaje del ticket y clasifica su prioridad
    basándose en palabras clave que indican urgencia.

    Args:
        state: Estado actual del ticket

    Returns:
        Nombre del nodo siguiente ("procesar_urgente" o "procesar_normal")
    """
    mensaje_lower = state['mensaje'].lower()

    # Palabras clave que indican urgencia
    palabras_urgentes = [
        "caído", "down", "crítico", "urgente",
        "producción", "error fatal", "no funciona",
        "seguridad", "hackeo", "pérdida de datos"
    ]

    # Verificar si el mensaje contiene palabras urgentes
    es_urgente = any(palabra in mensaje_lower for palabra in palabras_urgentes)

    if es_urgente:
        print(f"\n⚠️  ROUTING: Ticket clasificado como URGENTE")
        print(f"   Razón: Contiene palabras clave de urgencia")
        return "procesar_urgente"
    else:
        print(f"\n✅ ROUTING: Ticket clasificado como NORMAL")
        print(f"   Razón: No contiene indicadores de urgencia")
        return "procesar_normal"


# =============================================================================
# PASO 4: Construir el Grafo
# =============================================================================

def create_graph():
    """
    Construye y compila el grafo de clasificación de tickets.

    Arquitectura:
        START
          ↓
        recibir_ticket
          ↓
        clasificar_prioridad (Conditional Edge)
          ↓               ↓
        urgente        normal
          ↓               ↓
        END            END

    Returns:
        CompiledGraph: Grafo compilado listo para ejecutar
    """
    # 1. Crear el builder
    builder = StateGraph(TicketState)
    print("✅ StateGraph creado")

    # 2. Agregar los nodos
    builder.add_node("recibir_ticket", recibir_ticket)
    builder.add_node("procesar_urgente", procesar_urgente)
    builder.add_node("procesar_normal", procesar_normal)
    print("✅ Nodos agregados")

    # 3. Conectar con edges
    # START → recibir_ticket (edge normal, siempre va ahí)
    builder.add_edge(START, "recibir_ticket")

    # recibir_ticket → clasificar_prioridad → [urgente O normal] (conditional edge)
    builder.add_conditional_edges(
        "recibir_ticket",           # Desde este nodo
        clasificar_prioridad        # Usar esta función para decidir
    )

    # procesar_urgente → END (edge normal)
    builder.add_edge("procesar_urgente", END)

    # procesar_normal → END (edge normal)
    builder.add_edge("procesar_normal", END)

    print("✅ Edges conectados")

    # 4. Compilar el grafo
    graph = builder.compile()
    print("🎉 Grafo compilado exitosamente\n")

    return graph


# =============================================================================
# Crear el grafo (para LangGraph Studio)
# =============================================================================

# Esta variable es la que LangGraph Studio buscará
graph = create_graph()


# =============================================================================
# PASO 5: Función de prueba (opcional, para ejecutar localmente)
# =============================================================================

def main():
    """
    Función principal para probar el grafo localmente.

    Ejecuta varios casos de prueba con diferentes tipos de tickets.
    """
    print("="*70)
    print("🎬 Sistema de Clasificación de Tickets de Soporte")
    print("="*70)

    # Casos de prueba
    test_cases = [
        {
            "ticket_id": "TICKET-001",
            "mensaje": "El servidor de producción está caído",
            "prioridad": "",
            "estado": "nuevo",
            "asignado_a": ""
        },
        {
            "ticket_id": "TICKET-002",
            "mensaje": "¿Cómo cambio mi contraseña?",
            "prioridad": "",
            "estado": "nuevo",
            "asignado_a": ""
        },
        {
            "ticket_id": "TICKET-003",
            "mensaje": "Error crítico en el sistema de pagos",
            "prioridad": "",
            "estado": "nuevo",
            "asignado_a": ""
        },
        {
            "ticket_id": "TICKET-004",
            "mensaje": "Necesito actualizar mi perfil",
            "prioridad": "",
            "estado": "nuevo",
            "asignado_a": ""
        },
        {
            "ticket_id": "TICKET-005",
            "mensaje": "Posible hackeo detectado en la base de datos",
            "prioridad": "",
            "estado": "nuevo",
            "asignado_a": ""
        }
    ]

    # Ejecutar cada caso
    for i, ticket in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"TEST {i}/{len(test_cases)}")
        print(f"{'='*70}")
        print(f"\n📥 INPUT:")
        print(f"   ID: {ticket['ticket_id']}")
        print(f"   Mensaje: '{ticket['mensaje']}'")

        # Ejecutar el grafo
        resultado = graph.invoke(ticket)

        print(f"\n📤 OUTPUT FINAL:")
        print(f"   ID: {resultado['ticket_id']}")
        print(f"   Estado: {resultado['estado']}")
        print(f"   Prioridad: {resultado['prioridad']}")
        print(f"   Asignado a: {resultado['asignado_a']}")
        print(f"\n{'='*70}\n")

    print("\n✅ Todos los tests completados")


if __name__ == "__main__":
    # Solo ejecutar main() si se corre directamente (no en Studio)
    main()
