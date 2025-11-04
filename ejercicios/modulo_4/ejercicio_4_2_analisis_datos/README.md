# Ejercicio 4.2: Pipeline de Análisis de Documentos

## 🎯 Objetivo

Construir un **pipeline de análisis de documentos multi-etapa** que procesa documentos de negocio (contratos, reportes, propuestas) extrayendo información estructurada, insights y generando resúmenes ejecutivos.

Este ejercicio demuestra:
- ✅ Pipeline de procesamiento secuencial
- ✅ Paralelización de análisis independientes
- ✅ Agregación de resultados
- ✅ Validación y quality assurance
- ✅ Generación de outputs estructurados

## 📚 Contexto del Problema

### Escenario de Negocio

Trabajas en **LegalTech Solutions**, una empresa que analiza contratos y documentos legales para otras empresas. Actualmente, el proceso manual toma 2-4 horas por documento.

Tu misión es construir un pipeline automatizado que:
1. Extrae información clave (partes, fechas, montos, obligaciones)
2. Analiza riesgos y oportunidades
3. Identifica cláusulas críticas
4. Genera resumen ejecutivo estructurado
5. Valida la calidad del análisis

**Requisitos:**
- Procesar documentos de 5-20 páginas
- Tiempo objetivo: < 3 minutos por documento
- Accuracy: > 90% en extracción de datos clave
- Output estructurado en JSON y resumen ejecutivo en texto

### Arquitectura del Pipeline

```
┌──────────────────┐
│  DOCUMENTO       │
│  (Texto/PDF)     │
└────────┬─────────┘
         │
         ↓
┌────────────────────────────────────────────┐
│  ETAPA 1: PREPROCESSING                    │
│  - Limpiar texto                           │
│  - Detectar secciones                      │
│  - Metadata extraction                     │
└────────┬───────────────────────────────────┘
         │
         ↓
┌────────────────────────────────────────────┐
│  ETAPA 2: ANÁLISIS PARALELOS               │
│                                            │
│  ┌─────────────┐  ┌─────────────┐        │
│  │  Financial  │  │    Risk     │        │
│  │  Analysis   │  │  Analysis   │        │
│  └──────┬──────┘  └──────┬──────┘        │
│         │                │                │
│  ┌─────────────┐  ┌─────────────┐        │
│  │   Legal     │  │ Obligation  │        │
│  │  Analysis   │  │  Analysis   │        │
│  └──────┬──────┘  └──────┬──────┘        │
└─────────┼─────────────────┼───────────────┘
          │                 │
          └────────┬────────┘
                   ↓
       ┌───────────────────────┐
       │  ETAPA 3: AGGREGATION │
       │  - Combinar análisis  │
       │  - Detectar conflictos│
       │  - Priorizar insights │
       └───────────┬───────────┘
                   │
                   ↓
       ┌───────────────────────┐
       │  ETAPA 4: VALIDATION  │
       │  - Verificar          │
       │    completitud        │
       │  - Quality checks     │
       │  - Confidence scoring │
       └───────────┬───────────┘
                   │
            ┌──────┴──────┐
            ↓             ↓
    ┌──────────┐   ┌──────────┐
    │  APPROVE │   │  REVIEW  │
    │  OUTPUT  │   │  MANUAL  │
    └──────────┘   └──────────┘
```

## 🏗️ Componentes del Sistema

### 1. Estado del Pipeline

```python
class DocumentAnalysisState(TypedDict):
    """Estado del pipeline de análisis de documentos."""
    # Input
    document_text: str
    document_type: str  # "contract", "proposal", "report"

    # Preprocessing
    cleaned_text: str
    sections: Dict[str, str]
    metadata: Dict

    # Análisis paralelos
    financial_analysis: Dict
    risk_analysis: Dict
    legal_analysis: Dict
    obligations_analysis: Dict

    # Agregación
    combined_insights: List[Dict]
    executive_summary: str

    # Validación
    validation_results: Dict
    confidence_score: float
    requires_human_review: bool
    review_reasons: List[str]

    # Output final
    structured_output: Dict
```

### 2. Etapas del Pipeline

#### Etapa 1: Preprocessing

Limpia y estructura el documento:
- Remove ruido (headers, footers repetitivos)
- Detectar secciones principales
- Extraer metadata básica (fechas, partes, referencias)

#### Etapa 2: Análisis Paralelos

Cuatro agentes analizan en paralelo:

**Financial Analyst:**
- Montos monetarios
- Plazos de pago
- Penalizaciones
- Garantías financieras

**Risk Analyst:**
- Riesgos legales
- Riesgos operacionales
- Riesgos financieros
- Nivel de exposición

**Legal Analyst:**
- Cláusulas críticas
- Jurisdicción
- Resolución de disputas
- Cumplimiento regulatorio

**Obligations Analyst:**
- Obligaciones de cada parte
- Entregables y deadlines
- Condiciones y dependencias
- Consecuencias de incumplimiento

#### Etapa 3: Aggregation

Combina todos los análisis:
- Integra insights de todos los analistas
- Detecta conflictos o inconsistencias
- Prioriza hallazgos por importancia
- Genera resumen ejecutivo

#### Etapa 4: Validation

Verifica calidad del análisis:
- Completitud: ¿Se analizaron todas las secciones?
- Consistencia: ¿Hay contradicciones?
- Confidence: ¿Qué tan seguro está el sistema?
- Decide si requiere revisión humana

## 📝 Tareas

### Paso 1: Implementar Preprocessing

```python
def preprocess_node(state: DocumentAnalysisState) -> dict:
    """
    Preprocesa el documento para análisis.

    TODO:
    1. Limpiar texto (remover ruido)
    2. Detectar secciones principales
    3. Extraer metadata básica (fechas, partes, montos)
    4. Retornar cleaned_text, sections, metadata
    """
    pass
```

### Paso 2: Implementar Analistas Paralelos

```python
def financial_analyst(state: DocumentAnalysisState) -> dict:
    """
    Analiza aspectos financieros del documento.

    TODO:
    1. Extraer montos, plazos, penalizaciones
    2. Analizar términos de pago
    3. Identificar riesgos financieros
    4. Retornar financial_analysis estructurado
    """
    pass

def risk_analyst(state: DocumentAnalysisState) -> dict:
    """Analiza riesgos del documento."""
    pass

def legal_analyst(state: DocumentAnalysisState) -> dict:
    """Analiza aspectos legales del documento."""
    pass

def obligations_analyst(state: DocumentAnalysisState) -> dict:
    """Analiza obligaciones de las partes."""
    pass
```

### Paso 3: Implementar Aggregation

```python
def aggregator_node(state: DocumentAnalysisState) -> dict:
    """
    Agrega todos los análisis en insights unificados.

    TODO:
    1. Recopilar todos los análisis paralelos
    2. Integrar hallazgos
    3. Detectar conflictos o inconsistencias
    4. Priorizar insights por criticidad
    5. Generar executive summary
    """
    pass
```

### Paso 4: Implementar Validation

```python
def validator_node(state: DocumentAnalysisState) -> dict:
    """
    Valida calidad del análisis y decide si requiere revisión.

    TODO:
    1. Verificar completitud de análisis
    2. Calcular confidence score
    3. Detectar flags de calidad
    4. Decidir si requiere revisión humana
    5. Documentar razones de revisión
    """
    pass
```

### Paso 5: Construir el Grafo

```python
def build_graph():
    """
    TODO:
    1. Agregar nodos para cada etapa
    2. Secuencial: preprocess → analysts
    3. Paralelo: Los 4 analysts ejecutan simultáneamente
    4. Secuencial: aggregator → validator
    5. Condicional: validator → [approve, review]
    """
    pass
```

## 🎓 Conceptos Clave

### 1. Pipeline Pattern

Este ejercicio implementa el **Pipeline Pattern** clásico:

```
Input → Transform → Analyze → Aggregate → Validate → Output
```

Cada etapa:
- Recibe estado
- Procesa
- Agrega resultados al estado
- Pasa al siguiente

### 2. Paralelización

Los 4 analistas ejecutan **en paralelo**:

```python
# LangGraph permite paralelización automática
workflow.add_edge("preprocess", "financial")
workflow.add_edge("preprocess", "risk")
workflow.add_edge("preprocess", "legal")
workflow.add_edge("preprocess", "obligations")

# Todos convergen a aggregator
workflow.add_edge("financial", "aggregator")
workflow.add_edge("risk", "aggregator")
workflow.add_edge("legal", "aggregator")
workflow.add_edge("obligations", "aggregator")
```

LangGraph ejecuta los 4 analistas concurrentemente, acelerando el proceso.

### 3. Reducers para Agregación

Cuando múltiples nodos actualizan el mismo campo, usa reducers:

```python
from operator import add

class DocumentAnalysisState(TypedDict):
    combined_insights: Annotated[List[Dict], add]  # Reducer: concatena listas
```

### 4. Structured Output

Los análisis deben ser estructurados para facilitar procesamiento:

```python
financial_analysis = {
    "total_amount": 150000.00,
    "currency": "USD",
    "payment_terms": {
        "milestone_1": {"amount": 50000, "deadline": "2024-03-01"},
        "milestone_2": {"amount": 50000, "deadline": "2024-06-01"},
        "milestone_3": {"amount": 50000, "deadline": "2024-09-01"}
    },
    "penalties": {
        "late_payment": "1.5% mensual",
        "early_termination": "20% del monto total"
    },
    "financial_risks": [
        "Alto monto sin garantías",
        "Penalizaciones bajas podrían incentivar incumplimiento"
    ]
}
```

### 5. Validation Strategy

Múltiples niveles de validación:

```python
def calculate_confidence(state):
    confidence = 1.0

    # Penalizar si falta análisis
    if not state.get("financial_analysis"):
        confidence -= 0.3

    # Penalizar si hay inconsistencias
    if detect_contradictions(state):
        confidence -= 0.2

    # Penalizar si hay secciones sin analizar
    analyzed_sections = count_analyzed_sections(state)
    total_sections = len(state["sections"])
    if analyzed_sections < total_sections * 0.8:
        confidence -= 0.2

    return max(confidence, 0.0)
```

## 🧪 Testing

Los tests verifican:
1. ✅ Preprocessing extrae metadata correctamente
2. ✅ Cada analista genera análisis estructurado
3. ✅ Paralelización funciona (todos ejecutan)
4. ✅ Aggregator integra todos los análisis
5. ✅ Validator calcula confidence correctamente
6. ✅ Decisión de revisión humana es apropiada
7. ✅ End-to-end con diferentes tipos de documentos

## 💡 Pistas

### Pista 1: Detección de Secciones

```python
def detect_sections(text: str) -> Dict[str, str]:
    """
    Detecta secciones principales del documento.
    """
    sections = {}

    # Patrones comunes de secciones
    section_headers = [
        "PARTIES", "PARTES",
        "SCOPE", "ALCANCE",
        "PAYMENT", "PAGO",
        "TERM", "PLAZO",
        "OBLIGATIONS", "OBLIGACIONES",
        "LIABILITY", "RESPONSABILIDAD",
        "TERMINATION", "TERMINACIÓN"
    ]

    lines = text.split('\n')
    current_section = "PREAMBLE"
    current_content = []

    for line in lines:
        line_upper = line.strip().upper()

        # Verificar si es un header de sección
        is_header = False
        for header in section_headers:
            if header in line_upper and len(line.strip()) < 50:
                # Nueva sección encontrada
                if current_content:
                    sections[current_section] = '\n'.join(current_content)
                current_section = header
                current_content = []
                is_header = True
                break

        if not is_header:
            current_content.append(line)

    # Agregar última sección
    if current_content:
        sections[current_section] = '\n'.join(current_content)

    return sections
```

### Pista 2: Extracción de Metadata

```python
import re
from datetime import datetime

def extract_metadata(text: str) -> Dict:
    """
    Extrae metadata básica del documento.
    """
    metadata = {}

    # Extraer fechas
    date_patterns = [
        r'\d{1,2}/\d{1,2}/\d{4}',
        r'\d{4}-\d{2}-\d{2}',
        r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}'
    ]

    dates = []
    for pattern in date_patterns:
        found = re.findall(pattern, text, re.IGNORECASE)
        dates.extend(found)

    metadata["dates_found"] = dates[:5]  # Top 5

    # Extraer montos
    money_pattern = r'\$\s*[\d,]+(?:\.\d{2})?'
    amounts = re.findall(money_pattern, text)
    metadata["amounts_found"] = amounts[:10]  # Top 10

    # Detectar partes (buscar "between X and Y")
    party_pattern = r'between\s+([^and]+)\s+and\s+([^,\.]+)'
    parties = re.findall(party_pattern, text, re.IGNORECASE)
    if parties:
        metadata["parties"] = list(parties[0])

    return metadata
```

### Pista 3: Análisis Paralelo con Prompts

```python
def financial_analyst(state):
    text = state["cleaned_text"]
    sections = state["sections"]

    # Preparar contexto relevante
    relevant_text = ""
    for section_name in ["PAYMENT", "PAGO", "PRICE", "PRECIO"]:
        if section_name in sections:
            relevant_text += f"\n\n{section_name}:\n{sections[section_name]}"

    # Si no hay secciones específicas, usar todo
    if not relevant_text:
        relevant_text = text[:3000]  # Primeros 3000 chars

    prompt = f"""Eres un analista financiero experto en contratos.

TEXTO DEL CONTRATO:
{relevant_text}

Analiza los aspectos financieros y extrae:

1. MONTOS TOTALES
   - Valor total del contrato
   - Moneda

2. TÉRMINOS DE PAGO
   - Calendario de pagos
   - Hitos y condiciones

3. PENALIZACIONES
   - Por retraso en pago
   - Por terminación anticipada
   - Por incumplimiento

4. GARANTÍAS FINANCIERAS
   - Depósitos
   - Fianzas
   - Seguros requeridos

5. RIESGOS FINANCIEROS IDENTIFICADOS

Genera un análisis estructurado en JSON.

ANÁLISIS FINANCIERO:"""

    response = llm.invoke(prompt)

    # Parsear respuesta (idealmente JSON)
    # Para este ejercicio, guardamos texto
    return {"financial_analysis": {"raw": response.content}}
```

## 🎯 Resultado Esperado

### Input: Contrato de Servicios

```
SERVICE AGREEMENT

This agreement ("Agreement") is entered into on March 1, 2024,
between TechCorp Inc. ("Client") and DevSolutions LLC ("Provider").

SCOPE OF WORK:
Provider will develop a custom web application according to specifications
in Exhibit A.

PAYMENT TERMS:
Total contract value: $150,000 USD
- Milestone 1 (Requirements): $50,000 due March 31, 2024
- Milestone 2 (Development): $50,000 due June 30, 2024
- Milestone 3 (Delivery): $50,000 due September 30, 2024

Late payment penalty: 1.5% monthly interest

TERM:
This agreement is effective from March 1, 2024 to December 31, 2024.

TERMINATION:
Either party may terminate with 30 days notice.
Early termination penalty: 20% of remaining contract value.

LIABILITY:
Provider's liability is limited to the total contract value.
Client must provide adequate project information.

...
```

### Output: Análisis Estructurado

```json
{
  "document_type": "contract",
  "confidence_score": 0.92,
  "requires_human_review": false,

  "financial_summary": {
    "total_value": 150000.00,
    "currency": "USD",
    "payment_schedule": [
      {"milestone": 1, "amount": 50000, "date": "2024-03-31", "description": "Requirements"},
      {"milestone": 2, "amount": 50000, "date": "2024-06-30", "description": "Development"},
      {"milestone": 3, "amount": 50000, "date": "2024-09-30", "description": "Delivery"}
    ],
    "penalties": {
      "late_payment": "1.5% monthly",
      "early_termination": "20% of remaining value"
    }
  },

  "risk_assessment": {
    "overall_risk": "MEDIUM",
    "key_risks": [
      {
        "category": "financial",
        "severity": "medium",
        "description": "No upfront deposit or guarantee mentioned"
      },
      {
        "category": "legal",
        "severity": "low",
        "description": "Liability cap is standard"
      },
      {
        "category": "operational",
        "severity": "medium",
        "description": "Success depends on client providing adequate information"
      }
    ]
  },

  "key_obligations": {
    "provider": [
      "Develop web application per Exhibit A",
      "Deliver by September 30, 2024"
    ],
    "client": [
      "Pay milestones on schedule",
      "Provide adequate project information"
    ]
  },

  "critical_clauses": [
    {
      "section": "TERMINATION",
      "importance": "HIGH",
      "summary": "30-day notice required. 20% penalty for early termination."
    },
    {
      "section": "LIABILITY",
      "importance": "HIGH",
      "summary": "Provider liability capped at contract value"
    }
  ],

  "executive_summary": "This is a standard fixed-price software development agreement valued at $150,000 with milestone-based payments. Risk level is MEDIUM primarily due to lack of upfront guarantees and dependency on client cooperation. Payment schedule is reasonable but late payment penalties are relatively low. Recommend negotiating upfront deposit of at least 30% to reduce financial risk."
}
```

## 📖 Referencias

- [LangGraph Parallelization](https://langchain-ai.github.io/langgraph/how-tos/map-reduce/)
- [Document Analysis with LLMs](https://python.langchain.com/docs/use_cases/question_answering/)
- [Structured Outputs](https://python.langchain.com/docs/modules/model_io/output_parsers/)

---

**Tiempo estimado**: 60-75 minutos

**Dificultad**: ⭐⭐⭐⭐⭐ (Avanzado - Pipeline complejo con paralelización)

Este ejercicio es representativo de aplicaciones reales de document intelligence en empresas.
