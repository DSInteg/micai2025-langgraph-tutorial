"""
Ejercicio 3.2: Red Colaborativa con Handoffs - SOLUCIÓN COMPLETA

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

    Este estado es fundamental para la colaboración:
    - Cada agente puede ver qué hicieron los anteriores
    - Los reportes se acumulan para síntesis final
    - El historial muestra el flujo de handoffs
    """
    query: str                        # Consulta original del usuario
    current_agent: str                # Agente que tiene el control actualmente
    conversation_history: List[Dict]  # Historial completo de acciones
    specialist_reports: Dict[str, str]  # Reportes por cada especialista
    handoff_reason: str               # Razón del último handoff
    final_response: str               # Respuesta final sintetizada


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# =============================================================================
# AGENTE DE TRIAGE
# =============================================================================

def triage_agent(state: CollaborativeState) -> dict:
    """
    Agente de triage que analiza la consulta y deriva al especialista apropiado.

    Este es el punto de entrada del sistema. Su decisión determina
    qué especialista atenderá primero la consulta.

    La clasificación debe ser precisa porque afecta todo el flujo.
    """
    print("\n" + "="*70)
    print("🎯 TRIAGE AGENT: Analizando consulta...")
    print("="*70)

    query = state["query"]

    # Usar LLM para clasificar la consulta
    prompt = f"""Analiza esta consulta de soporte técnico y clasifica en UNA categoría:

Consulta: {query}

Categorías:
- CODE: Problemas de código, bugs, errores de programación, lógica de software
- NETWORK: Problemas de conectividad, DNS, firewall, puertos, latencia
- SECURITY: Vulnerabilidades, permisos, autenticación, cifrado, certificados

Responde SOLO con: CODE, NETWORK, o SECURITY

Clasificación:"""

    response = llm.invoke(prompt)
    category = response.content.strip().upper()

    # Validar y mapear a nombre de agente
    category_map = {
        "CODE": "code_agent",
        "NETWORK": "network_agent",
        "SECURITY": "security_agent"
    }

    if category not in category_map:
        # Fallback: clasificar por keywords
        query_lower = query.lower()
        if any(kw in query_lower for kw in ["código", "code", "bug", "función", "error"]):
            category = "CODE"
        elif any(kw in query_lower for kw in ["red", "network", "puerto", "firewall", "dns"]):
            category = "NETWORK"
        else:
            category = "SECURITY"

    agent_name = category_map[category]

    print(f"   → Consulta clasificada como: {category}")
    print(f"   → Derivando a: {agent_name}")

    # Actualizar historial
    history = state.get("conversation_history", [])
    history.append({
        "agent": "triage_agent",
        "action": "classify",
        "category": category,
        "handoff_to": agent_name,
        "reason": f"Consulta clasificada como {category}"
    })

    return {
        "current_agent": agent_name,
        "conversation_history": history
    }


# =============================================================================
# AGENTES ESPECIALISTAS
# =============================================================================

def code_agent(state: CollaborativeState) -> dict:
    """
    Agente especialista en problemas de código.

    Responsabilidades:
    - Analizar bugs y errores de programación
    - Revisar lógica de código
    - Identificar problemas de frameworks/bibliotecas

    Decisión de handoff:
    - Si detecta componente de red -> handoff a network_agent
    - Si detecta implicaciones de seguridad -> handoff a security_agent
    - Si puede resolver completamente -> ir a final
    """
    print("\n💻 CODE AGENT: Analizando desde perspectiva de código...")

    query = state["query"]
    history = state.get("conversation_history", [])
    reports = state.get("specialist_reports", {})

    # Contexto de reportes previos
    context = ""
    if reports:
        context = "\n\nReportes de otros especialistas:\n"
        for agent, report in reports.items():
            context += f"\n[{agent}]:\n{report}\n"

    # Análisis desde perspectiva de código
    analysis_prompt = f"""Eres un especialista en análisis de código y debugging.

Consulta del usuario:
{query}

{context}

Analiza la consulta desde la perspectiva de CÓDIGO:
1. Identifica posibles bugs o errores de programación
2. Analiza aspectos de frameworks, bibliotecas, sintaxis
3. Considera problemas de lógica de negocio
4. Proporciona diagnóstico técnico detallado

Genera un reporte técnico específico sobre aspectos de CÓDIGO.

REPORTE DE CÓDIGO:"""

    response = llm.invoke(analysis_prompt)
    code_report = response.content

    print(f"   ✓ Reporte de código generado ({len(code_report)} caracteres)")

    # Decidir siguiente paso
    decision_prompt = f"""Eres un especialista en código que ha analizado una consulta.

Consulta original: {query}

Tu reporte de código: {code_report}

Otros reportes disponibles: {list(reports.keys())}

Decide el siguiente paso:
- FINAL: Si la consulta está completamente resuelta desde todas las perspectivas necesarias
- NETWORK: Si necesitas ayuda de un especialista en redes (conectividad, puertos, DNS, etc.)
- SECURITY: Si necesitas ayuda de un especialista en seguridad (vulnerabilidades, autenticación, etc.)

Responde SOLO con: FINAL, NETWORK, o SECURITY

Decisión:"""

    decision_response = llm.invoke(decision_prompt)
    decision = decision_response.content.strip().upper()

    # Validar decisión
    if decision not in ["FINAL", "NETWORK", "SECURITY"]:
        # Si ya tenemos reportes de otros, probablemente podemos terminar
        decision = "FINAL" if len(reports) >= 1 else "NETWORK"

    # Mapear decisión a nombre de agente
    decision_map = {
        "FINAL": "final",
        "NETWORK": "network_agent",
        "SECURITY": "security_agent"
    }
    next_agent = decision_map[decision]

    print(f"   → Decisión: {decision}")
    print(f"   → Próximo agente: {next_agent}")

    # Actualizar estado
    reports_updated = reports.copy()
    reports_updated["code_agent"] = code_report

    history.append({
        "agent": "code_agent",
        "action": "analysis",
        "handoff_to": next_agent,
        "reason": f"Reporte de código completado. {'Listo para síntesis final' if decision == 'FINAL' else f'Necesita expertise en {decision}'}"
    })

    return {
        "current_agent": next_agent,
        "specialist_reports": reports_updated,
        "conversation_history": history,
        "handoff_reason": f"Code agent -> {next_agent}: {decision}"
    }


def network_agent(state: CollaborativeState) -> dict:
    """
    Agente especialista en problemas de red.

    Responsabilidades:
    - Analizar conectividad y protocolos
    - Diagnosticar problemas de puertos y firewall
    - Revisar configuración de DNS
    - Identificar latencia y performance de red
    """
    print("\n🔧 NETWORK AGENT: Analizando desde perspectiva de red...")

    query = state["query"]
    history = state.get("conversation_history", [])
    reports = state.get("specialist_reports", {})

    # Contexto de reportes previos
    context = ""
    if reports:
        context = "\n\nReportes de otros especialistas:\n"
        for agent, report in reports.items():
            context += f"\n[{agent}]:\n{report}\n"

    # Análisis desde perspectiva de red
    analysis_prompt = f"""Eres un especialista en redes y conectividad.

Consulta del usuario:
{query}

{context}

Analiza la consulta desde la perspectiva de REDES:
1. Identifica problemas de conectividad
2. Analiza puertos, firewalls, DNS
3. Considera protocolos de red (TCP/IP, HTTP, etc.)
4. Evalúa latencia y performance
5. Proporciona diagnóstico de red detallado

Genera un reporte técnico específico sobre aspectos de RED.

REPORTE DE RED:"""

    response = llm.invoke(analysis_prompt)
    network_report = response.content

    print(f"   ✓ Reporte de red generado ({len(network_report)} caracteres)")

    # Decidir siguiente paso
    decision_prompt = f"""Eres un especialista en redes que ha analizado una consulta.

Consulta original: {query}

Tu reporte de red: {network_report}

Otros reportes disponibles: {list(reports.keys())}

Decide el siguiente paso:
- FINAL: Si la consulta está completamente resuelta desde todas las perspectivas necesarias
- CODE: Si necesitas ayuda de un especialista en código (bugs, lógica, frameworks)
- SECURITY: Si necesitas ayuda de un especialista en seguridad (vulnerabilidades, autenticación)

Responde SOLO con: FINAL, CODE, o SECURITY

Decisión:"""

    decision_response = llm.invoke(decision_prompt)
    decision = decision_response.content.strip().upper()

    if decision not in ["FINAL", "CODE", "SECURITY"]:
        decision = "FINAL" if len(reports) >= 1 else "SECURITY"

    decision_map = {
        "FINAL": "final",
        "CODE": "code_agent",
        "SECURITY": "security_agent"
    }
    next_agent = decision_map[decision]

    print(f"   → Decisión: {decision}")
    print(f"   → Próximo agente: {next_agent}")

    reports_updated = reports.copy()
    reports_updated["network_agent"] = network_report

    history.append({
        "agent": "network_agent",
        "action": "analysis",
        "handoff_to": next_agent,
        "reason": f"Reporte de red completado. {'Listo para síntesis final' if decision == 'FINAL' else f'Necesita expertise en {decision}'}"
    })

    return {
        "current_agent": next_agent,
        "specialist_reports": reports_updated,
        "conversation_history": history,
        "handoff_reason": f"Network agent -> {next_agent}: {decision}"
    }


def security_agent(state: CollaborativeState) -> dict:
    """
    Agente especialista en seguridad.

    Responsabilidades:
    - Identificar vulnerabilidades
    - Analizar autenticación y autorización
    - Revisar cifrado y protección de datos
    - Evaluar permisos y control de acceso
    """
    print("\n🔒 SECURITY AGENT: Analizando desde perspectiva de seguridad...")

    query = state["query"]
    history = state.get("conversation_history", [])
    reports = state.get("specialist_reports", {})

    context = ""
    if reports:
        context = "\n\nReportes de otros especialistas:\n"
        for agent, report in reports.items():
            context += f"\n[{agent}]:\n{report}\n"

    analysis_prompt = f"""Eres un especialista en seguridad informática.

Consulta del usuario:
{query}

{context}

Analiza la consulta desde la perspectiva de SEGURIDAD:
1. Identifica vulnerabilidades potenciales
2. Analiza autenticación y autorización
3. Evalúa cifrado y protección de datos
4. Revisa permisos y control de acceso
5. Considera certificados y PKI si aplica
6. Proporciona análisis de seguridad detallado

Genera un reporte técnico específico sobre aspectos de SEGURIDAD.

REPORTE DE SEGURIDAD:"""

    response = llm.invoke(analysis_prompt)
    security_report = response.content

    print(f"   ✓ Reporte de seguridad generado ({len(security_report)} caracteres)")

    # Decidir siguiente paso
    decision_prompt = f"""Eres un especialista en seguridad que ha analizado una consulta.

Consulta original: {query}

Tu reporte de seguridad: {security_report}

Otros reportes disponibles: {list(reports.keys())}

Decide el siguiente paso:
- FINAL: Si la consulta está completamente resuelta desde todas las perspectivas necesarias
- CODE: Si necesitas ayuda de un especialista en código (revisar implementación específica)
- NETWORK: Si necesitas ayuda de un especialista en redes (configuración de firewall, puertos)

Responde SOLO con: FINAL, CODE, o NETWORK

Decisión:"""

    decision_response = llm.invoke(decision_prompt)
    decision = decision_response.content.strip().upper()

    if decision not in ["FINAL", "CODE", "NETWORK"]:
        decision = "FINAL" if len(reports) >= 1 else "CODE"

    decision_map = {
        "FINAL": "final",
        "CODE": "code_agent",
        "NETWORK": "network_agent"
    }
    next_agent = decision_map[decision]

    print(f"   → Decisión: {decision}")
    print(f"   → Próximo agente: {next_agent}")

    reports_updated = reports.copy()
    reports_updated["security_agent"] = security_report

    history.append({
        "agent": "security_agent",
        "action": "analysis",
        "handoff_to": next_agent,
        "reason": f"Reporte de seguridad completado. {'Listo para síntesis final' if decision == 'FINAL' else f'Necesita expertise en {decision}'}"
    })

    return {
        "current_agent": next_agent,
        "specialist_reports": reports_updated,
        "conversation_history": history,
        "handoff_reason": f"Security agent -> {next_agent}: {decision}"
    }


# =============================================================================
# AGENTE FINAL
# =============================================================================

def final_agent(state: CollaborativeState) -> dict:
    """
    Agente final que sintetiza todos los reportes en una respuesta coherente.

    Este agente es crucial porque debe:
    - Integrar múltiples perspectivas técnicas
    - Crear una narrativa coherente
    - Proporcionar soluciones accionables
    - No perder información crítica de ningún especialista

    La síntesis es diferente a concatenación: debe crear
    una respuesta unificada que se lea como un todo.
    """
    print("\n" + "="*70)
    print("✅ FINAL AGENT: Sintetizando respuesta final...")
    print("="*70)

    query = state["query"]
    reports = state.get("specialist_reports", {})
    history = state.get("conversation_history", [])

    # Preparar contexto de todos los reportes
    all_reports = ""
    for agent_name, report in reports.items():
        all_reports += f"\n═══ {agent_name.upper().replace('_', ' ')} ═══\n{report}\n"

    # Preparar flujo de colaboración
    flow = " → ".join([
        entry.get("agent", "unknown")
        for entry in history
    ])

    synthesis_prompt = f"""Eres un consultor técnico senior que debe crear una respuesta ejecutiva integrando
múltiples análisis especializados.

CONSULTA ORIGINAL DEL USUARIO:
{query}

FLUJO DE COLABORACIÓN:
{flow}

ANÁLISIS DE ESPECIALISTAS:
{all_reports}

Crea una RESPUESTA FINAL INTEGRADA que:

1. RESUMEN EJECUTIVO (2-3 frases)
   - Diagnostica el problema de manera integral
   - Menciona todas las dimensiones identificadas

2. ANÁLISIS DETALLADO
   - Integra los hallazgos de todos los especialistas
   - Identifica interdependencias entre aspectos (código ↔ red ↔ seguridad)
   - Explica cómo cada dimensión contribuye al problema

3. SOLUCIONES RECOMENDADAS
   - Proporciona pasos accionables
   - Prioriza las acciones según impacto
   - Considera todas las dimensiones

4. CONCLUSIÓN
   - Valoración general del problema
   - Próximos pasos sugeridos

La respuesta debe ser coherente, profesional y ejecutiva.
NO menciones el proceso interno de análisis ni los nombres de los agentes.
Habla directamente del problema y las soluciones.

RESPUESTA INTEGRADA:"""

    response = llm.invoke(synthesis_prompt)
    final_response = response.content

    print(f"   ✓ Respuesta final generada ({len(final_response)} caracteres)")
    print(f"   ✓ Integró {len(reports)} reportes de especialistas")

    return {"final_response": final_response}


# =============================================================================
# FUNCIONES DE ROUTING
# =============================================================================

def route_from_triage(state: CollaborativeState) -> Literal["code", "network", "security"]:
    """
    Determina a qué especialista derivar desde el triage.

    Lee current_agent del estado (que ya fue determinado por triage_agent)
    y mapea al nombre del nodo correspondiente.
    """
    current = state["current_agent"]

    # Mapear nombre de agente a nombre de nodo
    agent_to_node = {
        "code_agent": "code",
        "network_agent": "network",
        "security_agent": "security"
    }

    next_node = agent_to_node.get(current, "code")

    print(f"   → Routing desde triage a nodo: {next_node}")

    return next_node


def route_from_specialist(state: CollaborativeState) -> Literal["code", "network", "security", "final"]:
    """
    Determina el siguiente agente desde un especialista.

    Los especialistas pueden hacer handoff a:
    - Otro especialista (si necesitan ayuda de otra área)
    - Final agent (si ya tienen suficiente para responder)

    Esta función implementa el mecanismo de handoffs dinámicos.
    """
    current = state["current_agent"]

    # Si el agente decidió ir a final, ir allá
    if current == "final":
        print(f"   → Routing a nodo: final")
        return "final"

    # Mapear nombre de agente a nombre de nodo
    agent_to_node = {
        "code_agent": "code",
        "network_agent": "network",
        "security_agent": "security",
        "final": "final"
    }

    next_node = agent_to_node.get(current, "final")

    print(f"   → Routing desde especialista a nodo: {next_node}")

    return next_node


# =============================================================================
# CONSTRUCCIÓN DEL GRAFO
# =============================================================================

def build_graph():
    """
    Construye el grafo de red colaborativa con handoffs.

    Arquitectura de handoffs:

    1. Entry: triage
    2. Triage decide primer especialista
    3. Cada especialista puede hacer handoff a otro o a final
    4. Final sintetiza y termina

    Los handoffs se implementan mediante conditional edges que
    permiten flujo dinámico basado en decisiones de cada agente.

    Este pattern es más flexible que routing fijo porque:
    - Los agentes deciden en runtime
    - Pueden colaborar en secuencias no predefinidas
    - El flujo se adapta a la complejidad real del problema
    """
    workflow = StateGraph(CollaborativeState)

    # Agregar todos los nodos
    workflow.add_node("triage", triage_agent)
    workflow.add_node("code", code_agent)
    workflow.add_node("network", network_agent)
    workflow.add_node("security", security_agent)
    workflow.add_node("final", final_agent)

    # Entry point: triage clasifica la consulta
    workflow.set_entry_point("triage")

    # Conditional edge: triage → [code, network, security]
    # El triage decide qué especialista debe atender primero
    workflow.add_conditional_edges(
        "triage",
        route_from_triage,
        {
            "code": "code",
            "network": "network",
            "security": "security"
        }
    )

    # Conditional edges: especialistas → [otros especialistas, final]
    # Cada especialista puede hacer handoff dinámicamente

    # Code agent puede ir a: network, security, o final
    workflow.add_conditional_edges(
        "code",
        route_from_specialist,
        {
            "code": "code",
            "network": "network",
            "security": "security",
            "final": "final"
        }
    )

    # Network agent puede ir a: code, security, o final
    workflow.add_conditional_edges(
        "network",
        route_from_specialist,
        {
            "code": "code",
            "network": "network",
            "security": "security",
            "final": "final"
        }
    )

    # Security agent puede ir a: code, network, o final
    workflow.add_conditional_edges(
        "security",
        route_from_specialist,
        {
            "code": "code",
            "network": "network",
            "security": "security",
            "final": "final"
        }
    )

    # Final siempre termina
    workflow.add_edge("final", END)

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

        # Ejecutar con límite de recursión para evitar loops
        final_state = app.invoke(initial_state, {"recursion_limit": 20})

        print("\n" + "="*70)
        print("📊 RESPUESTA FINAL")
        print("="*70)
        print(final_state["final_response"])

        print(f"\n📈 Flujo de colaboración:")
        for entry in final_state["conversation_history"]:
            agent = entry.get("agent", "unknown")
            handoff = entry.get("handoff_to", "END")
            reason = entry.get("reason", "")
            print(f"   • {agent} → {handoff}")
            if reason:
                print(f"     Razón: {reason}")

        print(f"\n📋 Especialistas que participaron:")
        for agent_name in final_state["specialist_reports"].keys():
            print(f"   • {agent_name}")

        if i < len(queries):
            input("\n[Presiona Enter para continuar...]")

    print("\n" + "="*70)
    print("🎉 ¡Ejercicio completado!")
    print("="*70)
    print("\n💡 Observaciones sobre el pattern de Handoffs:")
    print("   • Los agentes colaboran dinámicamente sin flujo predefinido")
    print("   • Cada agente decide si necesita ayuda de otro especialista")
    print("   • El contexto se comparte mediante specialist_reports")
    print("   • Los handoffs permiten resolver problemas multi-dimensionales")
    print("   • Este pattern es ideal cuando la complejidad emerge durante el análisis")


if __name__ == "__main__":
    main()
