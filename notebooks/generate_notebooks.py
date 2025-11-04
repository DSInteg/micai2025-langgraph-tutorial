"""
Script para generar todos los notebooks del instructor.

Este script crea los 12 notebooks restantes con estructura completa.
"""

import json
import os

# Template base para notebooks
def create_notebook_template(title, module, exercise_num, time, objectives, cells_content):
    """Crea un notebook con estructura estándar"""

    notebook = {
        "cells": [
            # Cell 1: Header
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"# {title}\n",
                    "\n",
                    f"**{module}**  \n",
                    f"**Tiempo estimado**: {time}  \n",
                    f"**Ejercicio**: {exercise_num}\n",
                    "\n",
                    "---\n",
                    "\n",
                    "## 🎯 Objetivos de Aprendizaje\n",
                    "\n"
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
                    "# ║  📋 CELL 1: SETUP Y VERIFICACIÓN                          ║\n",
                    "# ║  ⏱️ Tiempo: 30 segundos                                    ║\n",
                    "# ╚════════════════════════════════════════════════════════════╝\n",
                    "\n",
                    "%pip install -q langgraph langchain-openai python-dotenv\n",
                    "\n",
                    "import os\n",
                    "import sys\n",
                    "from dotenv import load_dotenv\n",
                    "\n",
                    "sys.path.append(os.path.abspath('../..'))\n",
                    "load_dotenv()\n",
                    "\n",
                    "print(\"╔════════════════════════════════════════╗\")\n",
                    "print(\"║   SETUP VERIFICATION                   ║\")\n",
                    "print(\"╚════════════════════════════════════════╝\")\n",
                    "print(f\"✅ Python {sys.version.split()[0]}\")\n",
                    "print(f\"{'✅' if os.getenv('OPENAI_API_KEY') else '❌'} OpenAI API Key\")\n",
                    "print(f\"\\n🎬 Ready!\\n\")"
                ]
            }
        ] + cells_content + [
            # Final cell: Summary
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "---\n",
                    "\n",
                    "## ✅ CHECKPOINT FINAL\n",
                    "\n",
                    "### Verificar:\n",
                    "- [ ] El código ejecuta sin errores\n",
                    "- [ ] Todos entienden los conceptos clave\n",
                    "- [ ] Listos para el siguiente notebook\n",
                    "\n",
                    "### 💬 PREGUNTA FINAL:\n",
                    "> \"¿Alguna pregunta antes de continuar?\"\n",
                    "\n",
                    "---\n"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.11.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    return notebook


# Definir todos los notebooks a crear
notebooks_to_create = [
    # Módulo 1
    {
        "path": "modulo_1/02_instructor_ejercicio_1_1.ipynb",
        "title": "📝 Ejercicio 1.1: Workflow Simple",
        "module": "Módulo 1: Fundamentos",
        "exercise": "1.1",
        "time": "12 minutos",
        "objectives": [
            "Crear un StateGraph básico",
            "Definir nodos como funciones Python",
            "Conectar nodos con edges fijos",
            "Compilar y ejecutar un workflow"
        ],
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": "## 💬 SCRIPT DE INTRODUCCIÓN\n\n> \"Ejercicio 1.1: Van a construir su primer workflow.\n> \n> Un pipeline de procesamiento de documentos con 3 pasos fijos.\n> Abran el archivo starter.py y síganme.\""
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": "# Ver el código del ejercicio\n!cat ../../ejercicios/modulo_1/ejercicio_1_1_workflow_simple/README.md"
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": "# IMPLEMENTACIÓN PASO A PASO\n\nfrom typing import TypedDict\nfrom langgraph.graph import StateGraph, START, END\nfrom langchain_openai import ChatOpenAI\n\n# Paso 1: Estado\nclass DocumentState(TypedDict):\n    document: str\n    cleaned_text: str\n    sentiment: str\n    summary: str\n\nprint(\"✅ Estado definido\")"
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": "# Paso 2: Nodos\n\nllm = ChatOpenAI(model='gpt-4o-mini')\n\ndef clean_text_node(state):\n    text = state['document'].strip().lower()\n    print(f\"🧹 Limpiando: {text[:50]}...\")\n    return {'cleaned_text': text}\n\ndef analyze_sentiment_node(state):\n    response = llm.invoke(f\"Sentiment (Positivo/Negativo/Neutral): {state['cleaned_text'][:200]}\")\n    sentiment = response.content.strip()\n    print(f\"🎭 Sentimiento: {sentiment}\")\n    return {'sentiment': sentiment}\n\ndef summarize_node(state):\n    response = llm.invoke(f\"Resume en una oración: {state['cleaned_text'][:200]}\")\n    summary = response.content.strip()\n    print(f\"📝 Resumen: {summary}\")\n    return {'summary': summary}\n\nprint(\"✅ Nodos definidos\")"
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": "# Paso 3: Construir Grafo\n\nworkflow = StateGraph(DocumentState)\n\nworkflow.add_node('clean', clean_text_node)\nworkflow.add_node('analyze', analyze_sentiment_node)\nworkflow.add_node('summarize', summarize_node)\n\nworkflow.add_edge(START, 'clean')\nworkflow.add_edge('clean', 'analyze')\nworkflow.add_edge('analyze', 'summarize')\nworkflow.add_edge('summarize', END)\n\napp = workflow.compile()\n\nprint(\"✅ Workflow compilado\")"
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": "# 🎬 DEMO: Ejecutar\n\ntest_doc = 'LangGraph es increíble para construir workflows!'\n\nprint('='*60)\nprint('🎬 EJECUTANDO WORKFLOW')\nprint('='*60)\nprint(f'Input: {test_doc}\\n')\n\nresult = app.invoke({'document': test_doc})\n\nprint('\\n📊 RESULTADO:')\nfor key, value in result.items():\n    print(f'  {key}: {value}')\nprint('='*60)"
            }
        ]
    },
    {
        "path": "modulo_1/03_instructor_ejercicio_1_2.ipynb",
        "title": "🤖 Ejercicio 1.2: Agente Básico",
        "module": "Módulo 1: Fundamentos",
        "exercise": "1.2",
        "time": "12 minutos",
        "objectives": [
            "Crear herramientas con @tool",
            "Usar bind_tools para dar herramientas al LLM",
            "Implementar conditional_edges",
            "Manejar tool_calls y ToolNode"
        ],
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": "## 💬 SCRIPT\n\n> \"Ahora el desafío: un agente que DECIDE qué herramientas usar.\n> La clave: conditional_edges en vez de edges fijos.\""
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": "from typing import Annotated\nfrom langchain_core.messages import HumanMessage\nfrom langchain_core.tools import tool\nfrom langgraph.prebuilt import ToolNode\nimport operator\n\nclass AgentState(TypedDict):\n    messages: Annotated[list, operator.add]\n\n# Herramientas\n@tool\ndef search_web(query: str) -> str:\n    '''Busca en internet. Usa para info actual.'''\n    return f'Resultados: {query}'\n\n@tool\ndef calculator(expression: str) -> str:\n    '''Calcula. Usa para matemáticas.'''\n    return f'Resultado: {eval(expression)}'\n\nprint('✅ Herramientas definidas')"
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": "# Agente con herramientas\n\nfrom langchain_openai import ChatOpenAI\nfrom langgraph.graph import StateGraph, START, END\n\ntools = [search_web, calculator]\nllm = ChatOpenAI(model='gpt-4o-mini', temperature=0)\nllm_with_tools = llm.bind_tools(tools)\n\ndef agent_node(state):\n    response = llm_with_tools.invoke(state['messages'])\n    return {'messages': [response]}\n\ndef should_continue(state):\n    last = state['messages'][-1]\n    if hasattr(last, 'tool_calls') and last.tool_calls:\n        return 'tools'\n    return 'end'\n\n# Grafo\ngraph = StateGraph(AgentState)\ngraph.add_node('agent', agent_node)\ngraph.add_node('tools', ToolNode(tools))\n\ngraph.add_edge(START, 'agent')\ngraph.add_conditional_edges('agent', should_continue, {'tools': 'tools', 'end': END})\ngraph.add_edge('tools', 'agent')\n\napp = graph.compile()\nprint('✅ Agente compilado')"
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": "# 🎬 DEMO: Diferentes inputs\n\ntests = [\n    '¿Cuánto es 25 * 4?',\n    '¿Qué es LangGraph?',\n    'Hola'\n]\n\nfor test in tests:\n    print(f'\\nInput: {test}')\n    result = app.invoke({'messages': [HumanMessage(content=test)]})\n    \n    for msg in result['messages']:\n        if hasattr(msg, 'tool_calls') and msg.tool_calls:\n            print(f\"  🔧 Usó: {msg.tool_calls[0]['name']}\")\n    \n    print(f\"  💬 Respuesta: {result['messages'][-1].content}\")"
            }
        ]
    }
]

# Crear cada notebook
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

    print(f"✅ Created: {nb_config['path']}")

print(f"\n🎉 Created {len(notebooks_to_create)} notebooks!")
print("\nNext: Run this script from the notebooks/ directory:")
print("  cd notebooks/")
print("  python generate_notebooks.py")
