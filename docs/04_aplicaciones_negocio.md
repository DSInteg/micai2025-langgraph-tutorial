# Módulo 4: Aplicaciones de Negocio

## 📖 Índice

1. [Introducción](#introducción)
2. [Del Prototipo a Producción](#producción)
3. [Casos de Uso Empresariales](#casos-de-uso)
4. [Arquitecturas de Sistemas Reales](#arquitecturas)
5. [Monitoreo y Observabilidad](#monitoreo)
6. [Optimización de Costos](#costos)
7. [Mejores Prácticas](#mejores-prácticas)

---

## 🎯 Introducción {#introducción}

En este módulo aplicamos todo lo aprendido a **casos de uso reales de negocio**. Los ejercicios están basados en sistemas que se usan en producción.

### Diferencia: Ejercicios vs Aplicaciones Reales

| Aspecto | Ejercicios (M1-M3) | Aplicaciones (M4) |
|---------|-------------------|-------------------|
| **Propósito** | Aprender patterns | Resolver problemas reales |
| **Complejidad** | Un pattern a la vez | Múltiples patterns integrados |
| **Datos** | Simulados | Realistas |
| **Errores** | Controlados | Todos los edge cases |
| **Escalabilidad** | No crítica | Crítica |
| **Monitoreo** | Opcional | Esencial |

---

## 🚀 Del Prototipo a Producción {#producción}

### Checklist de Producción

#### 1. Funcionalidad ✅
- [ ] Todos los flujos principales funcionan
- [ ] Casos de error manejados
- [ ] Validaciones de entrada
- [ ] Tests comprehensivos (>80% cobertura)

#### 2. Rendimiento ⚡
- [ ] Latencia < requisitos (ej: p95 < 3s)
- [ ] Throughput adecuado
- [ ] Concurrencia sin degradación
- [ ] Timeout configurados

#### 3. Confiabilidad 🔒
- [ ] Retry con backoff exponencial
- [ ] Circuit breakers
- [ ] Fallbacks para LLM failures
- [ ] Idempotencia en operaciones críticas

#### 4. Observabilidad 👁️
- [ ] Logging estructurado
- [ ] Métricas (latencia, errores, costos)
- [ ] Tracing distribuido
- [ ] Alertas configuradas

#### 5. Seguridad 🛡️
- [ ] API keys en secrets manager
- [ ] Input sanitization
- [ ] Rate limiting
- [ ] Audit logs

#### 6. Costos 💰
- [ ] Presupuesto definido
- [ ] Monitoring de costos por llamada
- [ ] Caching donde aplique
- [ ] Modelos optimizados (gpt-4o-mini donde sea suficiente)

---

## 💼 Casos de Uso Empresariales {#casos-de-uso}

### 1. Atención al Cliente (Ejercicio 4.1)

**Problema de Negocio:**
- Volumen de consultas: 500-1,000/día
- Costo por agente humano: $15/hora
- Tiempo promedio por consulta: 10 min
- Costo mensual: $50,000

**Solución con Agentes:**
- Automatiza 70% de consultas
- Tiempo de respuesta: < 30 segundos
- Costo por consulta: $0.05 (LLM)
- Ahorro mensual: $30,000

**ROI:**
- Inversión inicial: $20,000 (desarrollo)
- Payback: < 1 mes
- ROI año 1: 1,500%

**Métricas Clave:**
```python
metrics = {
    "automation_rate": 0.72,  # 72% automated
    "escalation_rate": 0.28,  # 28% to humans
    "avg_confidence": 0.81,
    "csat_score": 4.3,  # /5
    "cost_per_query": 0.05  # USD
}
```

### 2. Análisis de Documentos (Ejercicio 4.2)

**Problema de Negocio:**
- Análisis manual: 2-4 horas/documento
- Analista senior: $80/hora
- Costo por documento: $160-320
- 50 documentos/mes = $8,000-16,000

**Solución con Agentes:**
- Análisis automatizado: 3 minutos
- 90% accuracy en extracción
- Costo por documento: $2-5
- Ahorro mensual: $7,500-15,000

**Aplicaciones:**
- Legal: Contratos, acuerdos
- Finanzas: Análisis de propuestas
- Compliance: Revisión de políticas
- RFPs: Evaluación de proveedores

### 3. Investigación Empresarial (Ejercicio 4.3)

**Problema de Negocio:**
- Investigación manual: 4-8 horas
- Consultor: $150/hora
- Costo por investigación: $600-1,200
- Calidad inconsistente

**Solución con Agentes:**
- Investigación automatizada: 10-15 minutos
- Costo: $5-10
- Calidad estandarizada
- Ahorro: 95% en tiempo y costo

**Aplicaciones:**
- Market research
- Competitive intelligence
- Technology assessment
- Due diligence preliminar

---

## 🏗️ Arquitecturas de Sistemas Reales {#arquitecturas}

### Arquitectura de Microservicios

```
┌─────────────────────────────────────────────────┐
│  FRONTEND (Web/Mobile)                          │
└────────────────┬────────────────────────────────┘
                 │ REST/GraphQL
                 ↓
┌─────────────────────────────────────────────────┐
│  API GATEWAY                                    │
│  - Auth                                         │
│  - Rate Limiting                                │
│  - Request Routing                              │
└────────────────┬────────────────────────────────┘
                 │
        ┌────────┼────────┐
        ↓        ↓        ↓
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Service  │ │ Service  │ │ Service  │
│ A        │ │ B        │ │ C        │
│(Customer)│ │(Document)│ │(Research)│
└────┬─────┘ └────┬─────┘ └────┬─────┘
     │            │            │
     └────────────┼────────────┘
                  │
        ┌─────────┼──────────┐
        ↓         ↓          ↓
┌──────────┐ ┌────────┐ ┌──────────┐
│ LangGraph│ │ Vector │ │ Cache    │
│ Runtime  │ │ DB     │ │ (Redis)  │
└──────────┘ └────────┘ └──────────┘
     │
     ↓
┌──────────┐
│ LLM APIs │
│ (OpenAI) │
└──────────┘
```

### Ejemplo de Configuración

```python
# config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    # LLM
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.3
    openai_max_tokens: int = 2000

    # Redis Cache
    redis_url: str
    cache_ttl: int = 3600  # 1 hour

    # Vector DB
    pinecone_api_key: str
    pinecone_environment: str
    pinecone_index: str

    # Monitoring
    langsmith_api_key: str
    langsmith_project: str

    # Rate Limits
    max_requests_per_minute: int = 60
    max_concurrent_requests: int = 10

    # Timeouts
    llm_timeout: int = 30
    pipeline_timeout: int = 120

    class Config:
        env_file = ".env"

settings = Settings()
```

---

## 👁️ Monitoreo y Observabilidad {#monitoreo}

### Métricas Clave

#### 1. Métricas de Sistema

```python
from prometheus_client import Counter, Histogram, Gauge

# Requests
request_counter = Counter(
    'agent_requests_total',
    'Total agent requests',
    ['agent_type', 'status']
)

# Latencia
request_duration = Histogram(
    'agent_request_duration_seconds',
    'Request duration',
    ['agent_type']
)

# Costos
cost_gauge = Gauge(
    'agent_cost_usd',
    'Cost in USD',
    ['agent_type']
)

# Errores
error_counter = Counter(
    'agent_errors_total',
    'Total errors',
    ['agent_type', 'error_type']
)
```

#### 2. Métricas de Negocio

```python
# Automation rate
automation_rate = Gauge(
    'support_automation_rate',
    'Percentage of automated queries'
)

# Confidence scores
confidence_histogram = Histogram(
    'agent_confidence_score',
    'Confidence scores',
    buckets=[0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
)

# Customer satisfaction
csat_gauge = Gauge(
    'customer_satisfaction_score',
    'CSAT score'
)
```

### Logging Estructurado

```python
import structlog

logger = structlog.get_logger()

def process_query(query_id: str, query: str):
    log = logger.bind(
        query_id=query_id,
        query_length=len(query)
    )

    log.info("query_received")

    try:
        result = agent.invoke({"query": query})

        log.info(
            "query_processed",
            confidence=result["confidence"],
            escalated=result["escalate"],
            duration_ms=elapsed_ms
        )

        return result

    except Exception as e:
        log.error(
            "query_failed",
            error=str(e),
            error_type=type(e).__name__
        )
        raise
```

### Tracing con LangSmith

**LangSmith** es la plataforma oficial de observabilidad para aplicaciones LangChain/LangGraph. Proporciona:

- ✅ **Tracing automático** de todos los componentes
- 📊 **Métricas detalladas** (latencia, tokens, costos)
- 🔍 **Debugging visual** de flujos de agentes
- 📈 **Evaluación y comparación** de versiones
- 🚨 **Alertas** en tiempo real

#### Configuración Básica

```python
# .env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__your_api_key
LANGCHAIN_PROJECT=production-support-agent
```

#### Tracing Automático

```python
from langsmith import Client
from utils.langsmith_config import get_runnable_config, add_run_metadata

client = Client()

# Todo código LangGraph se traza automáticamente
def process_customer_query(query: str, user_id: str):
    # Configurar tags y metadata para filtrado
    config = get_runnable_config(
        tags=["production", "customer-support", "v2.0"],
        metadata={
            "user_id": user_id,
            "session_id": get_session_id(),
            "environment": "prod"
        },
        run_name=f"SupportQuery_{user_id}"
    )

    # Esta llamada se traza automáticamente con todo el contexto
    result = agent.invoke({"query": query}, config=config)

    # Añadir metadata adicional después de la ejecución
    add_run_metadata({
        "escalated": result.get("escalate", False),
        "confidence": result.get("confidence", 0),
        "response_length": len(result.get("response", ""))
    })

    return result
```

#### Logging de Decisiones para Debugging

```python
from utils.langsmith_config import log_agent_decision

def routing_agent(state):
    intent = classify_intent(state["query"])

    # Registrar decisión para debugging posterior
    log_agent_decision(
        agent_name="Router",
        decision=f"route_to_{intent}",
        reasoning=f"Query classified as {intent} with keywords: {keywords}",
        confidence=classification_confidence
    )

    return {"intent": intent}
```

#### Análisis en LangSmith UI

En la interfaz de LangSmith puedes:

1. **Ver traces en tiempo real**
   - Flujo completo del grafo (nodos y edges)
   - Prompts exactos enviados al LLM
   - Respuestas completas
   - Tiempo de cada paso

2. **Filtrar y buscar**
   ```
   # Buscar por tags
   tag:production AND tag:customer-support

   # Buscar por metadata
   metadata.user_id = "user123"

   # Buscar por contenido
   "billing question"

   # Buscar errores
   status:error
   ```

3. **Comparar versiones**
   - A/B testing de prompts
   - Comparar latencia entre versiones
   - Medir impacto de cambios

4. **Analizar métricas**
   - Latencia (p50, p95, p99)
   - Tokens y costos
   - Error rates
   - Success rates

#### Monitoreo de Producción con LangSmith

```python
from langsmith import Client
from datetime import datetime, timedelta

def monitor_production_health():
    """
    Monitorea la salud del sistema en producción.
    """
    client = Client()

    # Obtener runs de las últimas 24 horas
    runs = client.list_runs(
        project_name="production-support-agent",
        start_time=datetime.now() - timedelta(days=1),
        filter='tag:production'
    )

    # Calcular métricas
    total = len(list(runs))
    errors = sum(1 for r in runs if r.error)
    avg_latency = sum(r.latency for r in runs if r.latency) / total

    error_rate = errors / total if total > 0 else 0

    # Alertar si hay problemas
    if error_rate > 0.05:  # 5% error rate
        alert_team(f"⚠️ High error rate: {error_rate:.1%}")

    if avg_latency > 5000:  # 5 segundos
        alert_team(f"⚠️ High latency: {avg_latency:.0f}ms")

    return {
        "total_requests": total,
        "error_rate": error_rate,
        "avg_latency_ms": avg_latency
    }
```

#### Evaluación Continua

```python
from langsmith import Client
from langsmith.evaluation import evaluate

client = Client()

# Crear dataset de casos de test
dataset_name = "support-agent-golden-set"

# Evaluar contra el dataset
def accuracy_evaluator(run, example):
    """Evalúa si la respuesta es correcta."""
    predicted_intent = run.outputs.get("intent")
    expected_intent = example.outputs.get("expected_intent")

    return {
        "key": "intent_accuracy",
        "score": int(predicted_intent == expected_intent)
    }

# Ejecutar evaluación
results = evaluate(
    lambda inputs: agent.invoke(inputs),
    data=dataset_name,
    evaluators=[accuracy_evaluator],
    experiment_prefix="support-agent-v2"
)

print(f"Accuracy: {results['accuracy']:.1%}")
```

#### Mejores Prácticas de Observabilidad

1. **Tags Consistentes**
   ```python
   # Usar estrategia de tags definida
   tags = [
       "production",              # Ambiente
       "v2.1",                    # Versión
       "customer-support",        # Dominio
       "high-priority"            # Criticidad
   ]
   ```

2. **Metadata Rico**
   ```python
   metadata = {
       "user_id": user_id,
       "session_id": session_id,
       "feature_flags": enabled_flags,
       "model_config": {
           "model": "gpt-4o-mini",
           "temperature": 0.7
       }
   }
   ```

3. **Naming Descriptivo**
   ```python
   # Nombres que describen la operación
   run_name = f"SupportTicket_{ticket_id}_Classification"
   ```

4. **Secciones Lógicas**
   ```python
   from utils.langsmith_config import trace_section

   with trace_section("UserAuthentication", tags=["auth"]):
       user = authenticate(credentials)

   with trace_section("QueryProcessing", tags=["llm"]):
       response = process_query(user_query)

   with trace_section("ResponseValidation", tags=["validation"]):
       validated = validate_response(response)
   ```

Para más detalles sobre debugging con LangSmith, ver:
- 📚 [Documentación completa](../docs/05_debugging_langsmith.md)
- 💡 [Ejemplo básico](../ejemplos/debugging_langsmith.py)
- 🎯 [Ejercicio 4.4](../ejercicios/modulo_4/ejercicio_4_4_debugging/)

### Dashboards

```yaml
# Grafana Dashboard Config
dashboard:
  title: "LangGraph Agents - Production"

  panels:
    - title: "Requests per Minute"
      metric: rate(agent_requests_total[1m])
      type: graph

    - title: "p95 Latency"
      metric: histogram_quantile(0.95, agent_request_duration_seconds)
      type: singlestat

    - title: "Error Rate"
      metric: rate(agent_errors_total[5m]) / rate(agent_requests_total[5m])
      type: graph
      alert_threshold: 0.05  # 5%

    - title: "Cost per Hour"
      metric: sum(rate(agent_cost_usd[1h]))
      type: singlestat

    - title: "Automation Rate"
      metric: support_automation_rate
      type: gauge
```

---

## 💰 Optimización de Costos {#costos}

### Estrategias de Optimización

#### 1. Selección de Modelo

```python
# Routing basado en complejidad
def select_model(query_complexity: str) -> str:
    if query_complexity == "simple":
        return "gpt-4o-mini"  # $0.15/1M tokens
    elif query_complexity == "medium":
        return "gpt-4o"  # $2.50/1M tokens
    else:
        return "gpt-4"  # $30/1M tokens

# Ahorro: 80% en consultas simples
```

#### 2. Caching Inteligente

```python
import hashlib
from functools import lru_cache

def cache_key(query: str, context: str) -> str:
    content = f"{query}:{context}"
    return hashlib.md5(content.encode()).hexdigest()

@lru_cache(maxsize=1000)
def cached_llm_call(cache_key: str, prompt: str):
    return llm.invoke(prompt)

# Ahorro: 30-40% con cache hit rate >50%
```

#### 3. Batch Processing

```python
# Procesar múltiples queries en paralelo
async def process_batch(queries: List[str]):
    tasks = [agent.ainvoke({"query": q}) for q in queries]
    results = await asyncio.gather(*tasks)
    return results

# Throughput: 10x mejora
```

#### 4. Prompt Optimization

```python
# MAL: Prompt verboso (500 tokens)
prompt_bad = f"""
You are a highly skilled and experienced customer support agent
with extensive knowledge of our products and services. Please
analyze the following customer query in great detail and provide
a comprehensive, thoughtful response...

Query: {query}
"""

# BIEN: Prompt conciso (50 tokens)
prompt_good = f"""Respond to customer query:

{query}

Be concise and helpful."""

# Ahorro: 90% en prompt tokens
```

### Cálculo de Costos

```python
def estimate_costs(
    requests_per_day: int,
    avg_tokens_per_request: int,
    model: str = "gpt-4o-mini"
):
    # Precios (input + output)
    model_costs = {
        "gpt-4o-mini": 0.15 / 1_000_000,  # por token
        "gpt-4o": 2.50 / 1_000_000,
        "gpt-4": 30.00 / 1_000_000
    }

    cost_per_token = model_costs[model]
    tokens_per_day = requests_per_day * avg_tokens_per_request
    cost_per_day = tokens_per_day * cost_per_token

    return {
        "cost_per_day": cost_per_day,
        "cost_per_month": cost_per_day * 30,
        "cost_per_request": cost_per_day / requests_per_day
    }

# Ejemplo
costs = estimate_costs(
    requests_per_day=1000,
    avg_tokens_per_request=500,
    model="gpt-4o-mini"
)
# Output: {"cost_per_month": $2.25}
```

---

## ✅ Mejores Prácticas {#mejores-prácticas}

### 1. Gestión de Errores

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def resilient_llm_call(prompt: str):
    try:
        return llm.invoke(prompt)
    except RateLimitError:
        logger.warning("rate_limit_hit")
        raise  # Retry
    except APIError as e:
        logger.error("api_error", error=str(e))
        raise
    except Exception as e:
        logger.error("unexpected_error", error=str(e))
        # Fallback
        return fallback_response()
```

### 2. Validación de Inputs

```python
from pydantic import BaseModel, validator

class CustomerQuery(BaseModel):
    query: str
    user_id: str

    @validator('query')
    def query_not_empty(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Query cannot be empty')
        if len(v) > 5000:
            raise ValueError('Query too long (max 5000 chars)')
        return v.strip()

    @validator('user_id')
    def valid_user_id(cls, v):
        if not v.startswith('user_'):
            raise ValueError('Invalid user_id format')
        return v
```

### 3. Circuit Breaker

```python
from pybreaker import CircuitBreaker

llm_breaker = CircuitBreaker(
    fail_max=5,  # Open after 5 failures
    timeout_duration=60  # Stay open for 60s
)

@llm_breaker
def protected_llm_call(prompt: str):
    return llm.invoke(prompt)

try:
    result = protected_llm_call(prompt)
except CircuitBreakerError:
    # LLM service is down, use fallback
    result = fallback_service(prompt)
```

### 4. Testing en Producción

```python
# A/B Testing
def get_agent_variant(user_id: str) -> str:
    if hash(user_id) % 100 < 10:  # 10% traffic
        return "variant_b"
    return "variant_a"

# Feature Flags
from launchdarkly import LDClient

ld_client = LDClient(sdk_key="your-key")

def should_use_new_feature(user_id: str) -> bool:
    user = {"key": user_id}
    return ld_client.variation("new-agent-feature", user, False)
```

### 5. Deployment

```yaml
# docker-compose.yml
version: '3.8'

services:
  agent-api:
    image: company/agent-api:latest
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - REDIS_URL=redis://redis:6379
    ports:
      - "8000:8000"
    depends_on:
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
```

---

## 📚 Recursos Adicionales

- [LangGraph Production Guide](https://langchain-ai.github.io/langgraph/how-tos/production/)
- [LangSmith Monitoring](https://docs.smith.langchain.com/)
- [OpenAI Best Practices](https://platform.openai.com/docs/guides/production-best-practices)
- [Prometheus for LLMs](https://prometheus.io/)

---

## 🎓 Resumen del Módulo

Has aprendido a:
✅ Diseñar sistemas multi-agente para casos reales
✅ Implementar monitoring y observabilidad
✅ Optimizar costos y rendimiento
✅ Desplegar a producción con confianza
✅ Manejar errores y edge cases
✅ Medir ROI y valor de negocio

**¡Felicitaciones por completar el tutorial!** 🎉

Ahora tienes las habilidades para construir sistemas multi-agente de nivel producción con LangGraph.
