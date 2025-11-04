# Ejercicio 4.3: Asistente de Investigación Empresarial

## 🎯 Objetivo

Construir un **asistente de investigación** que combina búsqueda, análisis y síntesis para generar reportes empresariales de alta calidad.

Este ejercicio integra:
- ✅ Plan-Execute pattern
- ✅ Búsqueda y análisis paralelos
- ✅ Memoria para evitar trabajo duplicado
- ✅ Síntesis multi-fuente
- ✅ Validación de calidad

## 📚 Contexto

### Escenario

Eres parte de un equipo de consultoría estratégica. Los analistas necesitan investigar temas de negocio rápidamente (competencia, mercados, tecnologías).

**Problema actual:**
- Investigación manual toma 4-8 horas
- Resultados inconsistentes
- Duplicación de trabajo
- Difícil mantener calidad

**Tu solución:**
Sistema automatizado que:
1. Planifica investigación
2. Busca información en paralelo
3. Analiza con múltiples perspectivas
4. Sintetiza en reporte ejecutivo
5. Usa memoria para eficiencia

### Arquitectura

```
OBJETIVO DE INVESTIGACIÓN
         ↓
    ┌─────────┐
    │ PLANNER │ ← Crea plan de investigación
    └────┬────┘
         ↓
┌────────────────────────────┐
│  BÚSQUEDA PARALELA         │
│  ┌──────┐  ┌──────┐       │
│  │ Web  │  │ Docs │       │
│  └──┬───┘  └──┬───┘       │
└─────┼─────────┼────────────┘
      │         │
      └────┬────┘
           ↓
    ┌──────────────┐
    │  ANALYZER    │ ← Analiza información
    └──────┬───────┘
           ↓
    ┌──────────────┐
    │ SYNTHESIZER  │ ← Genera reporte
    └──────┬───────┘
           ↓
    ┌──────────────┐
    │  VALIDATOR   │ ← Verifica calidad
    └──────────────┘
```

## 📝 Tareas

### Paso 1: Planner
```python
def planner_node(state):
    """
    TODO: Crear plan de investigación
    - Identificar sub-temas
    - Definir fuentes
    - Priorizar áreas
    """
```

### Paso 2: Researchers (Paralelo)
```python
def web_researcher(state):
    """TODO: Simular búsqueda web"""

def document_researcher(state):
    """TODO: Buscar en documentos"""
```

### Paso 3: Analyzer
```python
def analyzer_node(state):
    """TODO: Analizar hallazgos"""
```

### Paso 4: Synthesizer
```python
def synthesizer_node(state):
    """TODO: Generar reporte"""
```

### Paso 5: Validator
```python
def validator_node(state):
    """TODO: Validar calidad"""
```

## 🎓 Conceptos Clave

**Pattern Híbrido:**
- Plan-Execute para estructura
- Paralelización para eficiencia
- Memoria para no duplicar

**Salida Estructurada:**
```json
{
  "topic": "AI in Healthcare",
  "executive_summary": "...",
  "key_findings": [...],
  "recommendations": [...],
  "sources": [...],
  "confidence": 0.85
}
```

## 💡 Resultado Esperado

```
🎯 OBJETIVO: Investigar adopción de IA en salud

📋 PLANNER: Creando plan...
   ✓ 3 sub-temas identificados

🔍 RESEARCH (Paralelo):
   • Web Researcher: 5 fuentes
   • Document Researcher: 3 documentos

📊 ANALYZER: Analizando hallazgos...
   ✓ 8 insights clave

📝 SYNTHESIZER: Generando reporte...
   ✓ Reporte de 1,200 palabras

✅ VALIDATOR: Verificando...
   → Confidence: 0.87
   → Status: APPROVED
```

---

**Tiempo estimado**: 45-60 minutos
**Dificultad**: ⭐⭐⭐⭐⭐
