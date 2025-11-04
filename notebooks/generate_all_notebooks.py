"""
Script para generar TODOS los notebooks del instructor (Módulos 2, 3, 4).

Este script crea los 12 notebooks restantes con estructura completa.
"""

import json
import os

def create_notebook_template(title, module, exercise_num, time, objectives, cells_content):
    """Crea un notebook con estructura estándar"""

    notebook = {
        "cells": [
            # Cell 1: Header
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"# {title}\n\n",
                    f"**{module}**  \n",
                    f"**Tiempo estimado**: {time}  \n",
                    f"**Ejercicio**: {exercise_num}\n\n",
                    "---\n\n",
                    "## 🎯 Objetivos de Aprendizaje\n\n"
                ] + [f"{i+1}. ✅ {obj}\n" for i, obj in enumerate(objectives)]
            },
            # Cell 2: Setup
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# ╔════════════════════════════════════════════════════════════╗\n",
                    "# ║  📋 SETUP Y VERIFICACIÓN                                  ║\n",
                    "# ╚════════════════════════════════════════════════════════════╝\n\n",
                    "%pip install -q langgraph langchain-openai python-dotenv\n\n",
                    "import os, sys\n",
                    "from dotenv import load_dotenv\n",
                    "sys.path.append(os.path.abspath('../..'))\n",
                    "load_dotenv()\n\n",
                    "print('='*50)\n",
                    "print('   SETUP VERIFICATION')\n",
                    "print('='*50)\n",
                    "print(f\"✅ Python {sys.version.split()[0]}\")\n",
                    "print(f\"{'✅' if os.getenv('OPENAI_API_KEY') else '❌'} OpenAI API Key\")\n",
                    "print(f\"\\n🎬 Ready!\\n\")"
                ]
            }
        ] + cells_content + [
            # Final cell
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "---\n\n",
                    "## ✅ CHECKPOINT FINAL\n\n",
                    "- [ ] Código ejecuta sin errores\n",
                    "- [ ] Conceptos clave entendidos\n",
                    "- [ ] Listos para continuar\n\n",
                    "### 💬 PREGUNTA:\n",
                    "> \"¿Alguna duda antes de continuar?\"\n"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "version": "3.11.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    return notebook

# ═══════════════════════════════════════════════════════════════════
# DEFINICIÓN DE TODOS LOS NOTEBOOKS
# ═══════════════════════════════════════════════════════════════════

notebooks_to_create = [
    # ────────────────────────────────────────────────────────────────
    # MÓDULO 2: PATRONES MULTI-AGENTE
    # ────────────────────────────────────────────────────────────────
    {
        "path": "modulo_2/01_instructor_patrones_overview.ipynb",
        "title": "🔀 Patrones Multi-Agente - Overview",
        "module": "Módulo 2: Patrones Multi-Agente",
        "exercise": "Overview",
        "time": "15 minutos",
        "objectives": [
            "Entender los 3 patterns fundamentales",
            "Routing (especialización)",
            "Parallelization (velocidad)",
            "Orchestrator (coordinación)"
        ],
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": "## 💬 SCRIPT\n\n> \"Módulo 2: Sistemas multi-agente.\n> En producción, un solo agente no es suficiente.\n> Hoy: 3 patterns que se usan REALMENTE en empresas.\""},
            {"cell_type": "markdown", "metadata": {}, "source": "## 📊 Los 3 Patterns\n\n### 1. ROUTING (Especialización)\n```\nQuery → Classifier → Specialist\n```\n\n### 2. PARALLELIZATION (Velocidad)\n```\nInput → [Agent A, Agent B, Agent C] → Aggregator\n```\n\n### 3. ORCHESTRATOR (Coordinación)\n```\nOrchestrator → Worker 1 → Worker 2 → Synthesis\n```"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# Demo rápida de cada pattern\n\nfrom langgraph.graph import StateGraph, START, END\nfrom typing import TypedDict\n\nprint('🔀 Vamos a ver cada uno en acción...')\nprint('\\n1. ROUTING: Especialistas por dominio')\nprint('2. PARALLELIZATION: Múltiples perspectivas')\nprint('3. ORCHESTRATOR: Coordinación inteligente')"}
        ]
    },
    {
        "path": "modulo_2/02_instructor_ejercicio_2_1_routing.ipynb",
        "title": "🎯 Ejercicio 2.1: Sistema de Routing",
        "module": "Módulo 2: Patrones Multi-Agente",
        "exercise": "2.1",
        "time": "15 minutos",
        "objectives": [
            "Implementar classifier con LLM",
            "Crear agentes especializados",
            "Usar conditional_edges para routing",
            "Manejar múltiples rutas"
        ],
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": "## 💬 SCRIPT\n\n> \"Ejercicio 2.1: Sistema de customer support con especialistas.\n> El classifier decide: ¿technical, billing, o general?\""},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "from typing import TypedDict\nfrom langchain_openai import ChatOpenAI\nfrom langgraph.graph import StateGraph, START, END\n\nclass SupportState(TypedDict):\n    query: str\n    intent: str\n    response: str\n\nllm = ChatOpenAI(model='gpt-4o-mini')\nprint('✅ Setup completo')"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# Classifier - LA CLAVE del routing\n\ndef classify_intent(state):\n    prompt = f'''Clasifica esta consulta de soporte:\n    \n    Query: {state[\"query\"]}\n    \n    Categorías:\n    - technical: problemas de API, código, errores\n    - billing: pagos, facturas, suscripciones\n    - general: otras preguntas\n    \n    Responde SOLO: technical, billing, o general'''\n    \n    response = llm.invoke(prompt)\n    intent = response.content.strip().lower()\n    print(f'🎯 Clasificado como: {intent}')\n    return {'intent': intent}\n\nprint('✅ Classifier definido')"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# Agentes especializados\n\ndef technical_agent(state):\n    print('🔧 Agente técnico manejando...')\n    response = llm.invoke(f'Responde como experto técnico: {state[\"query\"]}')\n    return {'response': response.content}\n\ndef billing_agent(state):\n    print('💰 Agente de billing manejando...')\n    response = llm.invoke(f'Responde como experto en facturación: {state[\"query\"]}')\n    return {'response': response.content}\n\ndef general_agent(state):\n    print('💬 Agente general manejando...')\n    response = llm.invoke(f'Responde de forma general: {state[\"query\"]}')\n    return {'response': response.content}\n\nprint('✅ Agentes especializados definidos')"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# Construir grafo con routing\n\ngraph = StateGraph(SupportState)\n\n# Agregar nodos\ngraph.add_node('classifier', classify_intent)\ngraph.add_node('technical', technical_agent)\ngraph.add_node('billing', billing_agent)\ngraph.add_node('general', general_agent)\n\n# Routing desde classifier\ngraph.add_edge(START, 'classifier')\ngraph.add_conditional_edges(\n    'classifier',\n    lambda s: s['intent'],  # ← Decisión basada en intent\n    {\n        'technical': 'technical',\n        'billing': 'billing',\n        'general': 'general'\n    }\n)\n\n# Todos terminan en END\ngraph.add_edge('technical', END)\ngraph.add_edge('billing', END)\ngraph.add_edge('general', END)\n\napp = graph.compile()\nprint('✅ Sistema de routing compilado')"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# 🎬 DEMO: Diferentes tipos de consultas\n\ntest_queries = [\n    'Mi API da error 500',\n    'Quiero cancelar mi suscripción',\n    '¿Qué es LangGraph?'\n]\n\nfor query in test_queries:\n    print('='*60)\n    print(f'Query: {query}')\n    result = app.invoke({'query': query})\n    print(f'Intent: {result[\"intent\"]}')\n    print(f'Response: {result[\"response\"][:100]}...')\n    print()"}
        ]
    },
    {
        "path": "modulo_2/03_instructor_ejercicio_2_2_parallel.ipynb",
        "title": "⚡ Ejercicio 2.2: Paralelización",
        "module": "Módulo 2: Patrones Multi-Agente",
        "exercise": "2.2",
        "time": "12 minutos",
        "objectives": [
            "Usar Send() API para fan-out",
            "Ejecutar agentes en paralelo",
            "Agregar resultados de múltiples agentes",
            "Medir mejoras de performance"
        ],
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": "## 💬 SCRIPT\n\n> \"Ejercicio 2.2: Análisis paralelo.\n> 3 analistas trabajan AL MISMO TIEMPO.\n> Esto es MUCHO más rápido que secuencial.\""},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "from typing import TypedDict\nfrom langchain_openai import ChatOpenAI\nfrom langgraph.graph import StateGraph, START, END\nfrom langgraph.constants import Send\n\nclass AnalysisState(TypedDict):\n    document: str\n    sentiment: str\n    entities: list\n    summary: str\n    final_report: str\n\nllm = ChatOpenAI(model='gpt-4o-mini')\nprint('✅ Setup')"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# Analistas paralelos\n\ndef sentiment_analyst(state):\n    print('🎭 Analizando sentimiento...')\n    result = llm.invoke(f'Sentimiento (Positivo/Negativo/Neutral): {state[\"document\"][:200]}')\n    return {'sentiment': result.content}\n\ndef entity_analyst(state):\n    print('👤 Extrayendo entidades...')\n    result = llm.invoke(f'Extrae personas y organizaciones de: {state[\"document\"][:200]}')\n    return {'entities': result.content.split(',')}\n\ndef summary_analyst(state):\n    print('📝 Generando resumen...')\n    result = llm.invoke(f'Resume en una oración: {state[\"document\"][:200]}')\n    return {'summary': result.content}\n\nprint('✅ Analistas definidos')"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# Fan-out paralelo\n\ndef fan_out(state):\n    '''Dispara los 3 analistas EN PARALELO'''\n    return [\n        Send('sentiment', state),\n        Send('entities', state),\n        Send('summary', state)\n    ]\n\ndef aggregate(state):\n    '''Combina todos los análisis'''\n    report = f'''REPORTE FINAL:\n    Sentimiento: {state.get(\"sentiment\", \"N/A\")}\n    Entidades: {state.get(\"entities\", [])}\n    Resumen: {state.get(\"summary\", \"N/A\")}\n    '''\n    return {'final_report': report}\n\nprint('✅ Fan-out y aggregator definidos')"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# Construir grafo paralelo\n\ngraph = StateGraph(AnalysisState)\n\ngraph.add_node('sentiment', sentiment_analyst)\ngraph.add_node('entities', entity_analyst)\ngraph.add_node('summary', summary_analyst)\ngraph.add_node('aggregate', aggregate)\n\n# Fan-out desde START\ngraph.add_conditional_edges(START, fan_out)\n\n# Fan-in a aggregate\ngraph.add_edge('sentiment', 'aggregate')\ngraph.add_edge('entities', 'aggregate')\ngraph.add_edge('summary', 'aggregate')\ngraph.add_edge('aggregate', END)\n\napp = graph.compile()\nprint('✅ Grafo paralelo compilado')"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# 🎬 DEMO: Performance paralelo\n\nimport time\n\ndoc = 'LangGraph de LangChain es excelente para construir agentes. Permite workflows complejos.'\n\nprint('='*60)\nprint('🚀 EJECUCIÓN PARALELA')\nprint('='*60)\n\nstart = time.time()\nresult = app.invoke({'document': doc})\nelapsed = time.time() - start\n\nprint(f'\\n⏱️ Tiempo: {elapsed:.2f}s')\nprint(f'\\n{result[\"final_report\"]}')\nprint('\\n💡 Los 3 análisis se ejecutaron AL MISMO TIEMPO')"}
        ]
    },
    {
        "path": "modulo_2/04_instructor_ejercicio_2_3_orchestrator.ipynb",
        "title": "🎼 Ejercicio 2.3: Orchestrator-Workers",
        "module": "Módulo 2: Patrones Multi-Agente",
        "exercise": "2.3",
        "time": "10 minutos",
        "objectives": [
            "Implementar orchestrator que planifica",
            "Crear workers especializados",
            "Routing dinámico basado en decisiones",
            "Permitir re-planificación"
        ],
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": "## 💬 SCRIPT\n\n> \"Ejercicio 2.3: Orchestrator-Workers.\n> El orchestrator es el 'cerebro' - decide qué workers necesita.\n> Los workers son las 'manos' - ejecutan tareas específicas.\""},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "from typing import TypedDict, List\nfrom langchain_openai import ChatOpenAI\nfrom langgraph.graph import StateGraph, START, END\n\nclass OrchestratorState(TypedDict):\n    query: str\n    plan: str\n    worker_results: List[str]\n    final_answer: str\n\nllm = ChatOpenAI(model='gpt-4o-mini')\nprint('✅ Setup')"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# Orchestrator - decide qué hacer\n\ndef orchestrator(state):\n    '''Decide qué worker necesitamos'''\n    query = state['query']\n    results = state.get('worker_results', [])\n    \n    # ¿Ya tenemos suficiente info?\n    if len(results) >= 2:\n        return {'plan': 'synthesize'}\n    \n    # Decidir qué worker usar\n    prompt = f'''Query: {query}\n    Results so far: {results}\n    \n    ¿Qué worker necesitamos?\n    - search_worker: buscar información\n    - analyze_worker: analizar datos\n    - done: suficiente info\n    \n    Responde SOLO: search_worker, analyze_worker, o done'''\n    \n    decision = llm.invoke(prompt).content.strip().lower()\n    print(f'🎼 Orchestrator decide: {decision}')\n    return {'plan': decision}\n\nprint('✅ Orchestrator definido')"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# Workers\n\ndef search_worker(state):\n    print('🔍 Search worker ejecutando...')\n    result = f'Búsqueda completada para: {state[\"query\"][:50]}'\n    return {'worker_results': [result]}\n\ndef analyze_worker(state):\n    print('📊 Analyze worker ejecutando...')\n    result = f'Análisis completado de: {state[\"query\"][:50]}'\n    return {'worker_results': [result]}\n\ndef synthesize(state):\n    print('🔨 Sintetizando resultados...')\n    answer = f'Respuesta basada en: {\", \".join(state[\"worker_results\"])}'\n    return {'final_answer': answer}\n\nprint('✅ Workers definidos')"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# Routing dinámico\n\ndef route_decision(state):\n    plan = state['plan']\n    if plan == 'search_worker':\n        return 'search'\n    elif plan == 'analyze_worker':\n        return 'analyze'\n    elif plan == 'synthesize' or plan == 'done':\n        return 'synthesize'\n    return 'end'\n\nprint('✅ Router definido')"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# Construir grafo\n\ngraph = StateGraph(OrchestratorState)\n\ngraph.add_node('orchestrator', orchestrator)\ngraph.add_node('search', search_worker)\ngraph.add_node('analyze', analyze_worker)\ngraph.add_node('synthesize', synthesize)\n\n# Orchestrator decide\ngraph.add_edge(START, 'orchestrator')\ngraph.add_conditional_edges(\n    'orchestrator',\n    route_decision,\n    {\n        'search': 'search',\n        'analyze': 'analyze',\n        'synthesize': 'synthesize',\n        'end': END\n    }\n)\n\n# Workers vuelven al orchestrator\ngraph.add_edge('search', 'orchestrator')\ngraph.add_edge('analyze', 'orchestrator')\ngraph.add_edge('synthesize', END)\n\napp = graph.compile()\nprint('✅ Sistema orchestrator-workers compilado')"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# 🎬 DEMO\n\nquery = 'Investiga tendencias de LangGraph en 2024'\n\nprint('='*60)\nprint('🎼 ORCHESTRATOR-WORKERS')\nprint('='*60)\nprint(f'Query: {query}\\n')\n\nresult = app.invoke({'query': query, 'worker_results': []})\n\nprint(f'\\nResultados de workers: {result[\"worker_results\"]}')\nprint(f'\\nRespuesta final: {result.get(\"final_answer\", \"En proceso\")}')"}
        ]
    },

    # ────────────────────────────────────────────────────────────────
    # MÓDULO 3: AGENTES AUTÓNOMOS
    # ────────────────────────────────────────────────────────────────
    {
        "path": "modulo_3/01_instructor_autonomia_overview.ipynb",
        "title": "🤖 Agentes Autónomos - Overview",
        "module": "Módulo 3: Agentes Autónomos",
        "exercise": "Overview",
        "time": "15 minutos",
        "objectives": [
            "Entender verdadera autonomía",
            "Plan-Execute-Evaluate pattern",
            "Handoffs dinámicos",
            "Memoria compartida"
        ],
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": "## 💬 SCRIPT\n\n> \"Módulo 3: Agentes verdaderamente autónomos.\n> No solo ejecutan - PLANIFICAN, SE COORDINAN, y APRENDEN.\""},
            {"cell_type": "markdown", "metadata": {}, "source": "## 🎯 Los 3 Conceptos\n\n### 1. PLAN-EXECUTE\n```\nPlanner → Executor → Evaluator → Re-plan?\n```\n\n### 2. HANDOFFS\n```\nAgent A → (decide transferir) → Agent B\n```\n\n### 3. MEMORIA\n```\nAgent lee/escribe → Memoria Compartida\n```"}
        ]
    },
    {
        "path": "modulo_3/02_instructor_ejercicio_3_1_plan_execute.ipynb",
        "title": "📋 Ejercicio 3.1: Plan-Execute-Evaluate",
        "module": "Módulo 3: Agentes Autónomos",
        "exercise": "3.1",
        "time": "17 minutos",
        "objectives": [
            "Implementar planner que crea plan completo",
            "Executor que ejecuta paso a paso",
            "Evaluator que verifica progreso",
            "Loop de ejecución con límites"
        ],
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": "## 💬 SCRIPT\n\n> \"Plan-Execute: El agente PLANIFICA primero, EJECUTA después.\n> Como un chef que lee toda la receta antes de cocinar.\""},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "from typing import TypedDict, List\nfrom langchain_openai import ChatOpenAI\nfrom langgraph.graph import StateGraph, START, END\n\nclass PlanExecuteState(TypedDict):\n    query: str\n    plan: List[str]\n    current_step: int\n    results: List[str]\n    evaluation: str\n\nllm = ChatOpenAI(model='gpt-4o-mini')\nprint('✅ Setup')"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# Planner\n\ndef planner(state):\n    '''Crea plan completo'''\n    query = state['query']\n    \n    prompt = f'''Crea un plan de 3 pasos para: {query}\n    \n    Formato:\n    1. [paso 1]\n    2. [paso 2]\n    3. [paso 3]'''\n    \n    plan_text = llm.invoke(prompt).content\n    steps = [line.strip() for line in plan_text.split('\\n') if line.strip() and line[0].isdigit()]\n    \n    print(f'📋 Plan creado con {len(steps)} pasos')\n    for step in steps:\n        print(f'  {step}')\n    \n    return {'plan': steps, 'current_step': 0, 'results': []}\n\nprint('✅ Planner definido')"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# Executor\n\ndef executor(state):\n    '''Ejecuta paso actual'''\n    plan = state['plan']\n    current = state['current_step']\n    \n    if current >= len(plan):\n        return state\n    \n    step = plan[current]\n    print(f'⚙️ Ejecutando paso {current+1}: {step[:50]}...')\n    \n    # Simular ejecución\n    result = f'Resultado del paso {current+1}'\n    \n    return {\n        'results': state['results'] + [result],\n        'current_step': current + 1\n    }\n\nprint('✅ Executor definido')"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# Decisión de continuar\n\ndef should_continue(state):\n    current = state['current_step']\n    total = len(state['plan'])\n    \n    # Límite de seguridad\n    if current > 10:\n        return 'end'\n    \n    if current >= total:\n        return 'evaluate'\n    return 'execute'\n\nprint('✅ Router definido')"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# Evaluator\n\ndef evaluator(state):\n    '''Evalúa si el plan funcionó'''\n    print('✅ Evaluando resultados...')\n    eval = f'Plan completado. {len(state[\"results\"])} pasos ejecutados.'\n    return {'evaluation': eval}\n\nprint('✅ Evaluator definido')"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# Construir grafo\n\ngraph = StateGraph(PlanExecuteState)\n\ngraph.add_node('planner', planner)\ngraph.add_node('executor', executor)\ngraph.add_node('evaluator', evaluator)\n\ngraph.add_edge(START, 'planner')\ngraph.add_edge('planner', 'executor')\ngraph.add_conditional_edges(\n    'executor',\n    should_continue,\n    {\n        'execute': 'executor',  # Loop\n        'evaluate': 'evaluator',\n        'end': END\n    }\n)\ngraph.add_edge('evaluator', END)\n\napp = graph.compile()\nprint('✅ Plan-Execute compilado')"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# 🎬 DEMO\n\nquery = 'Investiga las tendencias de IA en 2024 y crea un reporte'\n\nprint('='*60)\nprint('📋 PLAN-EXECUTE-EVALUATE')\nprint('='*60)\nprint(f'Query: {query}\\n')\n\nresult = app.invoke({'query': query})\n\nprint(f'\\nPlan: {result[\"plan\"]}')\nprint(f'\\nResultados: {result[\"results\"]}')\nprint(f'\\nEvaluación: {result[\"evaluation\"]}')"}
        ]
    },
    {
        "path": "modulo_3/03_instructor_ejercicio_3_2_handoffs.ipynb",
        "title": "🤝 Ejercicio 3.2: Handoffs Dinámicos",
        "module": "Módulo 3: Agentes Autónomos",
        "exercise": "3.2",
        "time": "12 minutos",
        "objectives": [
            "Crear tools de transferencia",
            "Agentes que deciden cuándo transferir",
            "Routing basado en tool_calls",
            "Ciclos de handoff"
        ],
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": "## 💬 SCRIPT\n\n> \"Handoffs: Los agentes se PASAN el control.\n> Como un hospital: recepción → especialista → otro especialista.\""},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "from typing import Annotated\nfrom langchain_core.messages import HumanMessage\nfrom langchain_core.tools import tool\nfrom langchain_openai import ChatOpenAI\nfrom langgraph.graph import StateGraph, START, END\nimport operator\n\nclass HandoffState(TypedDict):\n    messages: Annotated[list, operator.add]\n    next_agent: str\n\nllm = ChatOpenAI(model='gpt-4o-mini', temperature=0)\nprint('✅ Setup')"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# Tools de transferencia\n\n@tool\ndef transfer_to_technical(reason: str) -> str:\n    '''Transfiere al agente técnico. Usa cuando hay problemas técnicos.'''\n    return f'TRANSFER:technical:{reason}'\n\n@tool\ndef transfer_to_billing(reason: str) -> str:\n    '''Transfiere al agente de billing. Usa para temas de facturación.'''\n    return f'TRANSFER:billing:{reason}'\n\nprint('✅ Transfer tools definidas')"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# Agentes con handoff\n\nsupport_tools = [transfer_to_technical, transfer_to_billing]\nsupport_llm = llm.bind_tools(support_tools)\n\ndef support_agent(state):\n    print('📞 Support agent...')\n    response = support_llm.invoke(state['messages'])\n    \n    # ¿Decidió transferir?\n    if response.tool_calls:\n        call = response.tool_calls[0]\n        if 'transfer_to' in call['name']:\n            dest = call['name'].split('_')[-1]\n            print(f'  → Transfiriendo a {dest}')\n            return {'messages': [response], 'next_agent': dest}\n    \n    return {'messages': [response], 'next_agent': 'end'}\n\ndef technical_agent(state):\n    print('🔧 Technical agent resolviendo...')\n    response = llm.invoke(state['messages'] + [HumanMessage('(Agente técnico) Resuelvo el problema.')])\n    return {'messages': [response], 'next_agent': 'support'}\n\ndef billing_agent(state):\n    print('💰 Billing agent resolviendo...')\n    response = llm.invoke(state['messages'] + [HumanMessage('(Agente billing) Resuelvo el problema.')])\n    return {'messages': [response], 'next_agent': 'support'}\n\nprint('✅ Agentes con handoff definidos')"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# Routing de handoffs\n\ndef route_handoff(state):\n    next_agent = state.get('next_agent', 'end')\n    if next_agent == 'technical':\n        return 'technical'\n    elif next_agent == 'billing':\n        return 'billing'\n    elif next_agent == 'support':\n        return 'support'\n    return 'end'\n\nprint('✅ Router definido')"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# Construir grafo\n\ngraph = StateGraph(HandoffState)\n\ngraph.add_node('support', support_agent)\ngraph.add_node('technical', technical_agent)\ngraph.add_node('billing', billing_agent)\n\ngraph.add_edge(START, 'support')\ngraph.add_conditional_edges(\n    'support',\n    route_handoff,\n    {\n        'technical': 'technical',\n        'billing': 'billing',\n        'support': 'support',\n        'end': END\n    }\n)\ngraph.add_edge('technical', 'support')\ngraph.add_edge('billing', 'support')\n\napp = graph.compile()\nprint('✅ Sistema de handoffs compilado')"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# 🎬 DEMO\n\nquery = 'Mi API da error 500 y mi factura está incorrecta'\n\nprint('='*60)\nprint('🤝 HANDOFFS DINÁMICOS')\nprint('='*60)\nprint(f'Query: {query}\\n')\n\nresult = app.invoke({'messages': [HumanMessage(query)], 'next_agent': ''})\n\nprint(f'\\nMensajes intercambiados: {len(result[\"messages\"])}')\nprint(f'Último mensaje: {result[\"messages\"][-1].content[:100]}...')"}
        ]
    },
    {
        "path": "modulo_3/04_instructor_ejercicio_3_3_memoria.ipynb",
        "title": "🧠 Ejercicio 3.3: Memoria Compartida",
        "module": "Módulo 3: Agentes Autónomos",
        "exercise": "3.3",
        "time": "10 minutos",
        "objectives": [
            "Usar operator.add para acumular",
            "Compartir hechos entre agentes",
            "Contexto persistente",
            "Multi-turno conversations"
        ],
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": "## 💬 SCRIPT\n\n> \"Memoria compartida: Los agentes RECUERDAN.\n> No empiezan de cero cada vez.\""},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "from typing import Annotated\nimport operator\nfrom langchain_core.messages import HumanMessage, SystemMessage\nfrom langchain_openai import ChatOpenAI\nfrom langgraph.graph import StateGraph, START, END\n\nclass MemoryState(TypedDict):\n    messages: Annotated[list, operator.add]\n    facts: Annotated[list, operator.add]  # ← Acumula\n\nllm = ChatOpenAI(model='gpt-4o-mini')\nprint('✅ Setup')"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# Agente con memoria\n\ndef agent_with_memory(state):\n    '''Agente que usa y actualiza memoria'''\n    messages = state['messages']\n    facts = state.get('facts', [])\n    \n    # Construir contexto con memoria\n    context = SystemMessage(content=f\"Hechos conocidos: {', '.join(facts)}\")\n    full_messages = [context] + messages\n    \n    print(f'🧠 Memoria actual: {facts}')\n    \n    response = llm.invoke(full_messages)\n    \n    # Extraer nuevos hechos (simplificado)\n    new_facts = []\n    content_lower = response.content.lower()\n    if 'nombre' in content_lower and 'es' in content_lower:\n        # Extrae hechos simples\n        new_facts.append(f\"Nombre mencionado en conversación\")\n    \n    return {\n        'messages': [response],\n        'facts': new_facts  # Se AGREGAN a los existentes\n    }\n\nprint('✅ Agente con memoria definido')"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# Construir grafo simple\n\ngraph = StateGraph(MemoryState)\ngraph.add_node('agent', agent_with_memory)\ngraph.add_edge(START, 'agent')\ngraph.add_edge('agent', END)\n\napp = graph.compile()\nprint('✅ Sistema con memoria compilado')"},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# 🎬 DEMO: Conversación multi-turno\n\nconversacion = [\n    'Me llamo Juan',\n    '¿Cuál es mi nombre?',\n    'Vivo en México',\n    '¿Dónde vivo?'\n]\n\nstate = {'messages': [], 'facts': []}\n\nprint('='*60)\nprint('🧠 MEMORIA COMPARTIDA')\nprint('='*60)\n\nfor turno in conversacion:\n    print(f'\\nUsuario: {turno}')\n    state['messages'] = [HumanMessage(turno)]\n    result = app.invoke(state)\n    \n    # Actualizar state con resultados acumulados\n    state['facts'] = result['facts']\n    \n    print(f'Agente: {result[\"messages\"][-1].content}')\n    print(f'Memoria: {result[\"facts\"]}')"}
        ]
    },

    # ────────────────────────────────────────────────────────────────
    # MÓDULO 4: APLICACIONES DE NEGOCIO
    # ────────────────────────────────────────────────────────────────
    {
        "path": "modulo_4/01_instructor_produccion_overview.ipynb",
        "title": "🏭 Producción - Consideraciones Clave",
        "module": "Módulo 4: Aplicaciones de Negocio",
        "exercise": "Overview",
        "time": "15 minutos",
        "objectives": [
            "Checklist de producción",
            "Retry logic y error handling",
            "Logging y métricas",
            "Costos y optimización"
        ],
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": "## 💬 SCRIPT\n\n> \"Módulo 4: De prototipo a PRODUCCIÓN.\n> Todo lo que necesitas para sistemas REALES.\""},
            {"cell_type": "markdown", "metadata": {}, "source": "## ✅ Checklist de Producción\n\n### 1. Funcionalidad\n- Tests >80%\n- Error handling\n- Validación de inputs\n\n### 2. Performance\n- Latencia < requisitos\n- Timeouts configurados\n- Retry logic\n\n### 3. Observabilidad\n- Logging estructurado\n- Métricas (latencia, costos)\n- LangSmith tracing\n\n### 4. Costos\n- Presupuesto definido\n- Monitoring por llamada\n- Modelos optimizados"}
        ]
    },
    {
        "path": "modulo_4/02_instructor_ejercicio_4_1_customer_support.ipynb",
        "title": "🎧 Ejercicio 4.1: Customer Support Completo",
        "module": "Módulo 4: Aplicaciones de Negocio",
        "exercise": "4.1",
        "time": "20 minutos",
        "objectives": [
            "Sistema completo de customer support",
            "Confidence scoring",
            "Escalación a humano",
            "Logging y métricas"
        ],
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": "## 💬 SCRIPT\n\n> \"Sistema REAL de customer support.\n> Con confidence, escalación, y logging completo.\""},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# Ver ejercicio completo\n!cat ../../ejercicios/modulo_4/ejercicio_4_1_atencion_cliente/README.md | head -50"}
        ]
    },
    {
        "path": "modulo_4/03_instructor_ejercicio_4_2_document_analysis.ipynb",
        "title": "📄 Ejercicio 4.2: Análisis de Documentos",
        "module": "Módulo 4: Aplicaciones de Negocio",
        "exercise": "4.2",
        "time": "20 minutos",
        "objectives": [
            "Pipeline multi-etapa",
            "Análisis paralelo",
            "Agregación de resultados",
            "Validación de calidad"
        ],
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": "## 💬 SCRIPT\n\n> \"Pipeline de análisis de documentos.\n> Preproceso → Análisis paralelo → Agregación → Validación.\""},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# Ver ejercicio\n!cat ../../ejercicios/modulo_4/ejercicio_4_2_analisis_datos/README.md | head -50"}
        ]
    },
    {
        "path": "modulo_4/04_instructor_ejercicio_4_3_research.ipynb",
        "title": "🔬 Ejercicio 4.3: Asistente de Investigación",
        "module": "Módulo 4: Aplicaciones de Negocio",
        "exercise": "4.3",
        "time": "15 minutos",
        "objectives": [
            "Sistema de investigación completo",
            "Plan-Execute aplicado",
            "Búsquedas paralelas",
            "Síntesis de información"
        ],
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": "## 💬 SCRIPT\n\n> \"Asistente de investigación empresarial.\n> Combina TODOS los patterns que vimos.\""},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": "# Ver ejercicio\n!cat ../../ejercicios/modulo_4/ejercicio_4_3_investigacion/README.md | head -50"},
            {"cell_type": "markdown", "metadata": {}, "source": "## 💡 TIP\n\n> \"Este ejercicio es complejo - úsenlo como referencia.\n> Combina Plan-Execute + Parallelization + Memoria.\n> Es un buen ejemplo de sistema REAL.\""}
        ]
    }
]

# ═══════════════════════════════════════════════════════════════════
# CREAR TODOS LOS NOTEBOOKS
# ═══════════════════════════════════════════════════════════════════

print("🚀 Generando notebooks de módulos 2, 3 y 4...\n")

for nb_config in notebooks_to_create:
    notebook = create_notebook_template(
        title=nb_config["title"],
        module=nb_config["module"],
        exercise_num=nb_config["exercise"],
        time=nb_config["time"],
        objectives=nb_config["objectives"],
        cells_content=nb_config["cells"]
    )

    filepath = os.path.join(".", nb_config["path"])
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)

    print(f"✅ {nb_config['path']}")

print(f"\n🎉 ¡Completado! Se crearon {len(notebooks_to_create)} notebooks.")
print("\nEstructura completa:")
print("  📁 modulo_2: 4 notebooks")
print("  📁 modulo_3: 4 notebooks")
print("  📁 modulo_4: 4 notebooks")
print("\nTotal: 12 notebooks nuevos + 3 existentes = 15 notebooks completos ✨")
