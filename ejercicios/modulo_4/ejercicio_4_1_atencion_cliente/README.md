# Ejercicio 4.1: Sistema de Atención al Cliente

## 🎯 Objetivo

Construir un **sistema completo de atención al cliente** que integra múltiples patterns de LangGraph para resolver consultas de manera inteligente, escalable y profesional.

Este ejercicio es un caso de uso real simplificado que combina:
- ✅ Routing inteligente
- ✅ Agentes especializados
- ✅ Memoria de conversación
- ✅ Búsqueda en base de conocimiento
- ✅ Escalamiento a humanos cuando es necesario

## 📚 Contexto del Problema

### Escenario de Negocio

Eres parte del equipo de IA de **TechStore**, una empresa de e-commerce de tecnología. La empresa recibe cientos de consultas diarias por:
- Preguntas sobre productos
- Soporte técnico
- Estado de pedidos
- Devoluciones y garantías
- Facturación

El equipo de soporte humano está saturado. Tu misión es construir un sistema de agentes que:
1. Atienda el 70-80% de consultas automáticamente
2. Escale a humanos solo cuando sea necesario
3. Proporcione respuestas precisas usando la base de conocimiento
4. Mantenga contexto de conversación
5. Sea monitoreable y medible

### Arquitectura del Sistema

```
                    ┌─────────────────┐
                    │  USUARIO        │
                    └────────┬────────┘
                             │
                             ↓
                    ┌─────────────────┐
                    │  INTAKE AGENT   │ ← Clasifica la consulta
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ↓              ↓              ↓
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
    │  PRODUCT    │ │  SUPPORT    │ │  ORDER      │
    │  AGENT      │ │  AGENT      │ │  AGENT      │
    └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
           │               │               │
           └───────────────┼───────────────┘
                           ↓
                  ┌─────────────────┐
                  │  SYNTHESIZER    │ ← Genera respuesta final
                  └────────┬────────┘
                           │
                    ┌──────┴──────┐
                    ↓             ↓
            ┌──────────┐   ┌──────────┐
            │ RESPOND  │   │ ESCALATE │
            │ TO USER  │   │ TO HUMAN │
            └──────────┘   └──────────┘

         ┌──────────────────────────────┐
         │   KNOWLEDGE BASE             │
         │  - FAQs                      │
         │  - Product Catalog           │
         │  - Technical Docs            │
         │  - Policies                  │
         └──────────────────────────────┘
```

## 🏗️ Componentes del Sistema

### 1. Estado Global

```python
class CustomerSupportState(TypedDict):
    """Estado compartido del sistema de atención al cliente."""
    # Input del usuario
    user_query: str
    user_id: str
    conversation_history: List[BaseMessage]

    # Clasificación
    category: str  # "product", "support", "order"
    urgency: str   # "low", "medium", "high"

    # Análisis de agentes
    product_analysis: str
    support_analysis: str
    order_analysis: str

    # Base de conocimiento
    kb_results: List[Dict]  # Resultados de búsqueda en KB

    # Respuesta
    final_response: str
    confidence_score: float
    should_escalate: bool
    escalation_reason: str
```

### 2. Knowledge Base

Base de conocimiento simulada con FAQs, productos y políticas:

```python
knowledge_base = {
    "products": [
        {
            "id": "LAPTOP001",
            "name": "Laptop Pro X15",
            "price": 1299.99,
            "specs": "Intel i7, 16GB RAM, 512GB SSD",
            "warranty": "2 years"
        },
        # ... más productos
    ],
    "faqs": [
        {
            "question": "¿Cuál es la política de devoluciones?",
            "answer": "30 días sin preguntas...",
            "category": "policy"
        },
        # ... más FAQs
    ],
    "technical_docs": [
        {
            "product": "LAPTOP001",
            "issue": "No enciende",
            "solution": "1. Verificar carga... 2. Reset BIOS..."
        },
        # ... más docs técnicas
    ]
}
```

### 3. Agentes Especializados

#### Intake Agent
- Clasifica la consulta en categorías
- Determina nivel de urgencia
- Busca en knowledge base
- Deriva al agente especializado apropiado

#### Product Agent
- Responde preguntas sobre productos
- Compara especificaciones
- Proporciona recomendaciones
- Accede al catálogo

#### Support Agent
- Resuelve problemas técnicos
- Sigue troubleshooting guides
- Busca en documentación técnica
- Puede solicitar información adicional

#### Order Agent
- Consulta estado de pedidos
- Maneja tracking
- Procesa devoluciones
- Accede a sistema de órdenes

#### Synthesizer Agent
- Integra análisis de agentes
- Genera respuesta coherente
- Decide si escalar a humano
- Calcula confidence score

## 📝 Tareas

### Paso 1: Implementar Knowledge Base Search

```python
def search_knowledge_base(query: str, category: str, kb: Dict) -> List[Dict]:
    """
    Busca información relevante en la base de conocimiento.

    TODO:
    1. Determinar qué secciones buscar según categoría
    2. Buscar por keywords (versión simple)
    3. Rankear resultados por relevancia
    4. Retornar top-k resultados
    """
    pass
```

### Paso 2: Implementar Intake Agent

```python
def intake_agent(state: CustomerSupportState) -> dict:
    """
    Agente inicial que clasifica y busca información.

    TODO:
    1. Analizar la consulta del usuario
    2. Clasificar en: product, support, order
    3. Determinar urgencia: low, medium, high
    4. Buscar en knowledge base
    5. Derivar al agente apropiado
    """
    pass
```

### Paso 3: Implementar Agentes Especializados

```python
def product_agent(state: CustomerSupportState) -> dict:
    """
    Agente especializado en productos.

    TODO:
    1. Analizar consulta desde perspectiva de productos
    2. Usar knowledge base results
    3. Acceder al catálogo si es necesario
    4. Generar análisis de productos
    """
    pass

def support_agent(state: CustomerSupportState) -> dict:
    """
    Agente especializado en soporte técnico.

    TODO:
    1. Analizar problema técnico
    2. Buscar soluciones en docs técnicas
    3. Seguir troubleshooting si aplica
    4. Generar análisis de soporte
    """
    pass

def order_agent(state: CustomerSupportState) -> dict:
    """
    Agente especializado en órdenes.

    TODO:
    1. Analizar consulta sobre pedido
    2. Buscar información de orden (simulado)
    3. Generar análisis de orden
    """
    pass
```

### Paso 4: Implementar Synthesizer

```python
def synthesizer_agent(state: CustomerSupportState) -> dict:
    """
    Sintetiza respuesta final y decide escalamiento.

    TODO:
    1. Recopilar todos los análisis de agentes
    2. Integrar knowledge base results
    3. Generar respuesta coherente y profesional
    4. Calcular confidence score (0-1)
    5. Decidir si escalar a humano (confidence < 0.7)
    """
    pass
```

### Paso 5: Implementar Routing

```python
def route_to_specialist(state: CustomerSupportState) -> Literal["product", "support", "order"]:
    """Rutea según categoría determinada por intake."""
    pass

def route_after_synthesis(state: CustomerSupportState) -> Literal["respond", "escalate"]:
    """Decide si responder o escalar según confidence."""
    pass
```

### Paso 6: Construir el Grafo

```python
def build_graph():
    """
    TODO:
    1. Agregar todos los nodos
    2. Entry: intake
    3. Conditional edge: intake → [product, support, order]
    4. Edges: specialists → synthesizer
    5. Conditional edge: synthesizer → [respond, escalate]
    """
    pass
```

## 🎓 Conceptos Clave

### 1. Integración de Patterns

Este ejercicio combina múltiples patterns:

**Routing (Módulo 2.1):**
```python
# Intake clasifica y rutea a especialista
intake → [product_agent, support_agent, order_agent]
```

**Especialización (Módulo 3.2):**
```python
# Cada agente tiene su dominio de expertise
product_agent: Catálogo, specs, recomendaciones
support_agent: Troubleshooting, docs técnicas
order_agent: Tracking, devoluciones
```

**Síntesis (Módulo 2.3):**
```python
# Synthesizer integra análisis
[product, support, order] → synthesizer → respuesta final
```

**Decision Making:**
```python
# Decidir si escalar basado en confidence
if confidence < 0.7:
    escalate_to_human()
else:
    respond_to_user()
```

### 2. Confidence Score

El confidence score indica qué tan seguro está el sistema:

```python
def calculate_confidence(state: CustomerSupportState) -> float:
    """
    Calcula confidence basado en:
    - ¿Se encontraron resultados en KB? (+0.3)
    - ¿El análisis es específico? (+0.3)
    - ¿No hay ambigüedad? (+0.2)
    - ¿No requiere acceso a sistemas externos? (+0.2)
    """
    confidence = 0.0

    # KB results found
    if state["kb_results"]:
        confidence += 0.3

    # Specific analysis
    analysis = state.get("product_analysis") or state.get("support_analysis") or state.get("order_analysis")
    if analysis and len(analysis) > 100:
        confidence += 0.3

    # No ambiguity keywords
    ambiguous_keywords = ["no estoy seguro", "podría ser", "tal vez"]
    if not any(kw in analysis.lower() for kw in ambiguous_keywords):
        confidence += 0.2

    # Self-contained (no external access needed)
    if "necesito acceder" not in analysis.lower():
        confidence += 0.2

    return min(confidence, 1.0)
```

### 3. Escalamiento a Humanos

Criterios para escalar:
- ✅ Confidence score < 0.7
- ✅ Usuario solicita explícitamente hablar con humano
- ✅ Problema requiere acceso a sistemas externos
- ✅ Situación de alta urgencia y complejidad
- ✅ Múltiples intentos fallidos

### 4. Respuesta Profesional

Las respuestas deben ser:
- **Claras**: Lenguaje simple y directo
- **Específicas**: Incluir detalles relevantes
- **Accionables**: Pasos concretos a seguir
- **Empáticas**: Reconocer la situación del usuario
- **Profesionales**: Tono cortés y formal

```python
# ✅ BIEN: Respuesta profesional
"""
Estimado cliente,

He revisado su consulta sobre la Laptop Pro X15.

ESPECIFICACIONES:
- Procesador: Intel i7 11th Gen
- RAM: 16GB DDR4
- Almacenamiento: 512GB SSD NVMe
- Garantía: 2 años

RESPUESTA A SU PREGUNTA:
Sí, esta laptop es excelente para programación y diseño gráfico gracias a sus 16GB de RAM y procesador i7.

¿Puedo ayudarle con algo más?

Saludos,
Sistema de Atención TechStore
"""

# ❌ MAL: Respuesta vaga
"""
Sí, es buena para eso.
"""
```

## 🧪 Testing

Los tests verifican:
1. ✅ Intake clasifica correctamente
2. ✅ Routing deriva al agente apropiado
3. ✅ Knowledge base search funciona
4. ✅ Agentes especializados generan análisis
5. ✅ Synthesizer integra múltiples fuentes
6. ✅ Confidence score se calcula correctamente
7. ✅ Escalamiento ocurre cuando es necesario
8. ✅ End-to-end con diferentes tipos de consultas

## 💡 Pistas

### Pista 1: Clasificación en Intake

```python
classification_prompt = f"""Eres un agente de clasificación de consultas de atención al cliente.

CONSULTA: {query}

Clasifica la consulta en UNA de estas categorías:
- PRODUCT: Preguntas sobre productos, especificaciones, comparaciones, recomendaciones
- SUPPORT: Problemas técnicos, troubleshooting, cómo usar productos
- ORDER: Estado de pedidos, tracking, devoluciones, facturación

También determina URGENCIA:
- LOW: Pregunta informativa, no urgente
- MEDIUM: Problema que necesita resolución pronto
- HIGH: Problema crítico, cliente bloqueado o frustrado

Responde en formato:
CATEGORY: [PRODUCT/SUPPORT/ORDER]
URGENCY: [LOW/MEDIUM/HIGH]

CLASIFICACIÓN:"""
```

### Pista 2: Búsqueda en Knowledge Base

```python
def search_knowledge_base(query: str, category: str, kb: Dict) -> List[Dict]:
    results = []
    query_lower = query.lower()
    query_words = set(query_lower.split())

    if category == "product":
        for product in kb["products"]:
            # Buscar en nombre y specs
            product_text = f"{product['name']} {product['specs']}".lower()
            if any(word in product_text for word in query_words):
                results.append({
                    "type": "product",
                    "data": product
                })

    elif category == "support":
        for doc in kb["technical_docs"]:
            # Buscar en issue y solution
            doc_text = f"{doc['issue']} {doc['solution']}".lower()
            overlap = len([w for w in query_words if w in doc_text])
            if overlap > 0:
                results.append({
                    "type": "technical_doc",
                    "data": doc,
                    "relevance": overlap
                })

    # Siempre buscar en FAQs
    for faq in kb["faqs"]:
        faq_text = f"{faq['question']} {faq['answer']}".lower()
        overlap = len([w for w in query_words if w in faq_text])
        if overlap > 1:
            results.append({
                "type": "faq",
                "data": faq,
                "relevance": overlap
            })

    # Ordenar por relevancia
    results.sort(key=lambda x: x.get("relevance", 0), reverse=True)

    return results[:5]
```

### Pista 3: Synthesizer con Confidence

```python
synthesis_prompt = f"""Eres un agente que genera respuestas finales de atención al cliente.

CONSULTA ORIGINAL: {query}

ANÁLISIS DE AGENTE ESPECIALISTA:
{specialist_analysis}

INFORMACIÓN DE BASE DE CONOCIMIENTO:
{kb_info}

HISTORIAL DE CONVERSACIÓN:
{conversation_history}

Genera una RESPUESTA PROFESIONAL que:
1. Sea clara y específica
2. Use información del análisis y KB
3. Proporcione pasos accionables si aplica
4. Sea empática y profesional
5. Ofrezca ayuda adicional

Si NO tienes suficiente información para responder con confianza,
incluye al final: [REQUIERE_ESCALAMIENTO]

RESPUESTA:"""
```

## 🎯 Resultado Esperado

### Ejemplo 1: Consulta de Producto

**Input:**
```
Usuario: "¿La Laptop Pro X15 es buena para diseño gráfico?"
```

**Output:**
```
═══════════════════════════════════════════════════════════
🎯 INTAKE AGENT
═══════════════════════════════════════════════════════════
Categoría: PRODUCT
Urgencia: LOW
KB Results: 2 resultados encontrados

═══════════════════════════════════════════════════════════
💻 PRODUCT AGENT
═══════════════════════════════════════════════════════════
Análisis generado (342 caracteres)

═══════════════════════════════════════════════════════════
✅ SYNTHESIZER
═══════════════════════════════════════════════════════════
Confidence Score: 0.85
Decision: RESPOND

═══════════════════════════════════════════════════════════
📨 RESPUESTA FINAL
═══════════════════════════════════════════════════════════
Estimado cliente,

He revisado las especificaciones de la Laptop Pro X15 para diseño gráfico.

ESPECIFICACIONES RELEVANTES:
- Procesador: Intel i7 11th Gen (excelente para rendering)
- RAM: 16GB DDR4 (suficiente para Adobe Suite)
- Gráficos: Intel Iris Xe (bueno para diseño 2D, limitado en 3D)
- Pantalla: 15.6" Full HD IPS (buena precisión de color)

RECOMENDACIÓN:
✅ Excelente para: Photoshop, Illustrator, diseño web, edición de fotos
⚠️  Limitaciones: Modelado 3D intensivo (recomendaría GPU dedicada)

Para diseño gráfico 2D profesional, esta laptop cumple perfectamente.
Si trabaja con 3D (Blender, 3DS Max), considere nuestro modelo Pro X15 Gaming
con GPU dedicada RTX 3060.

¿Le gustaría más información sobre algún aspecto específico?

Saludos,
Sistema de Atención TechStore
```

### Ejemplo 2: Consulta Compleja (Escalamiento)

**Input:**
```
Usuario: "Mi laptop no enciende y ya probé todo. Necesito que me la cambien YA."
```

**Output:**
```
═══════════════════════════════════════════════════════════
🎯 INTAKE AGENT
═══════════════════════════════════════════════════════════
Categoría: SUPPORT
Urgencia: HIGH

═══════════════════════════════════════════════════════════
🔧 SUPPORT AGENT
═══════════════════════════════════════════════════════════
Análisis generado (178 caracteres)

═══════════════════════════════════════════════════════════
✅ SYNTHESIZER
═══════════════════════════════════════════════════════════
Confidence Score: 0.45
Decision: ESCALATE

═══════════════════════════════════════════════════════════
🚨 ESCALADO A AGENTE HUMANO
═══════════════════════════════════════════════════════════
Razón: Situación de alta urgencia requiere validación de garantía
       y acceso a sistema de RMA. Confidence score bajo (0.45).

INFORMACIÓN RECOPILADA PARA AGENTE HUMANO:
- Categoría: Soporte técnico
- Urgencia: Alta
- Problema: Laptop no enciende
- Usuario ya intentó troubleshooting básico
- Solicita cambio/reemplazo

Tiempo estimado de respuesta de agente humano: 5-10 minutos
```

## 📖 Referencias

- [Customer Service Automation](https://langchain-ai.github.io/langgraph/tutorials/)
- [Multi-Agent Collaboration](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/)
- [Production Best Practices](https://langchain-ai.github.io/langgraph/how-tos/production/)

---

**Tiempo estimado**: 60 minutos

**Dificultad**: ⭐⭐⭐⭐⭐ (Avanzado - Integración completa de múltiples patterns)

Este ejercicio demuestra cómo construir un sistema real de producción que combina todos los conceptos del tutorial.
