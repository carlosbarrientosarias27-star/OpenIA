# Arquitectura del Proyecto

# Visión General

Este documento describe la estructura de módulos del proyecto, las dependencias entre ellos y las decisiones de diseño que guían su organización.

---

# Diagrama de Módulos

```
┌─────────────────────────────────────────────────────────────────┐
│                        Aplicación / CLI                         │
└──────────────────────────────┬──────────────────────────────────┘
                               │
              ┌────────────────▼────────────────┐
              │           core/                  │
              │   Orquestación y lógica central  │
              └──┬─────────────────────────┬─────┘
                 │                         │
    ┌────────────▼──────────┐   ┌──────────▼────────────┐
    │      tokens/          │   │       precios/         │
    │  Gestión de tokens:   │   │  Cálculo de precios:   │
    │  tokenización,        │   │  tarifas, descuentos,  │
    │  conteo, validación   │   │  conversión de moneda  │
    └────────────┬──────────┘   └──────────┬─────────────┘
                 │                         │
    ┌────────────▼─────────────────────────▼─────────────┐
    │                    modelos/                         │
    │       Entidades de dominio (dataclasses/Pydantic)   │
    └────────────────────────┬───────────────────────────┘
                             │
    ┌────────────────────────▼───────────────────────────┐
    │                   utils/                            │
    │      Helpers transversales: logging, config, I/O   │
    └────────────────────────────────────────────────────┘
```

## Dependencias externas

| Módulo      | Dependencias externas                  |
|-------------|----------------------------------------|
| `tokens/`   | `tiktoken`, `transformers` (opcional)  |
| `precios/`  | `forex-python` (opcional)              |
| `modelos/`  | `pydantic`                             |
| `utils/`    | `loguru`, `python-dotenv`              |

---

# Descripción de Módulos

## `core/`

Punto de entrada de la lógica de negocio. Coordina `tokens/` y `precios/` para responder a las peticiones de la capa superior. No contiene lógica de dominio propia; su responsabilidad es orquestar.

**Archivos principales:**
- `core/pipeline.py` — flujo de procesamiento principal
- `core/facade.py` — API interna simplificada para la CLI y los tests de integración

---

## `tokens/`

Responsable exclusivamente de todo lo relacionado con la representación y manipulación de tokens:

- Tokenización de texto (conversión texto → lista de tokens)
- Conteo de tokens para un modelo dado
- Validación de límites de contexto
- Truncado y segmentación de secuencias largas

**Por qué existe como módulo independiente:**
Tokenizar texto es una operación con estado (depende del vocabulario del modelo) y computacionalmente costosa. Aislarla permite cachear el tokenizador, intercambiar el backend (OpenAI → HuggingFace) sin tocar el resto del sistema, y testearla de forma unitaria sin necesidad de lógica de precios.

---

## `precios/`

Responsable exclusivamente del cálculo económico:

- Consulta de tarifas por modelo y tipo de token (entrada / salida)
- Aplicación de descuentos por volumen o plan
- Conversión de moneda
- Estimación de coste antes de ejecutar una llamada

**Por qué `tokens/` y `precios/` están separados:**

Esta es la decisión de diseño más importante del proyecto y responde al **Principio de Responsabilidad Única (SRP)** de SOLID:

| Razón | Detalle |
|---|---|
| **Ejes de cambio distintos** | Los precios cambian cuando el proveedor actualiza sus tarifas. La tokenización cambia cuando se actualiza el modelo o el vocabulario. Son motivos de cambio completamente independientes. |
| **Testing aislado** | Podemos testear el cálculo de precios con conteos de tokens ficticios, y testear la tokenización sin ningún precio. |
| **Reutilización** | `tokens/` puede usarse en herramientas de monitorización que no necesitan precios. `precios/` puede recibir conteos de cualquier fuente. |
| **Escalabilidad del equipo** | Dos desarrolladores pueden trabajar en cada módulo en paralelo sin conflictos de merge. |

---

## `modelos/`

Define las entidades de dominio como estructuras de datos validadas (Pydantic `BaseModel` o `dataclass`):

- `TokenUsage` — conteo de tokens de entrada, salida y total
- `PriceEstimate` — coste estimado con desglose por tipo
- `ModelConfig` — configuración de un modelo (nombre, límite de contexto, tarifas)

Este módulo **no importa nada de `tokens/` ni de `precios/`**. Es la base del grafo de dependencias y puede ser importado por cualquier módulo sin crear ciclos.

---

## `utils/`

Funcionalidades transversales que no pertenecen a ningún dominio concreto:

- Configuración desde variables de entorno (`.env`)
- Logger centralizado
- Serialización/deserialización JSON
- Decoradores de utilidad (`@retry`, `@timer`)

---

# Principios de Diseño Aplicados

## Single Responsibility Principle (SRP)

Cada módulo tiene **un único motivo para cambiar**. El test práctico: si aparece un cambio de requisito, ¿qué módulos hay que tocar? Si la respuesta es siempre uno solo, el SRP se está cumpliendo.

## Dependency Inversion Principle (DIP)

`core/` depende de **interfaces** (protocolos de Python / ABCs), no de implementaciones concretas de `tokens/` o `precios/`. Esto permite sustituir el tokenizador o el motor de precios sin modificar el núcleo.

```python
# core/ports.py
from typing import Protocol

class Tokenizer(Protocol):
    def count(self, text: str, model: str) -> int: ...

class PriceCalculator(Protocol):
    def estimate(self, token_usage: TokenUsage, model: str) -> PriceEstimate: ...
```

## Regla de dependencias (acíclica)

```
CLI / API  →  core  →  tokens, precios  →  modelos  →  utils
```

Las flechas van siempre en una sola dirección. Ningún módulo importa de un nivel superior al suyo.

---

# Decisiones Pendientes / ADRs

| # | Decisión | Estado |
|---|----------|--------|
| ADR-001 | Usar Pydantic v2 en lugar de dataclasses | ✅ Aceptado |
| ADR-002 | Soporte multi-proveedor en `precios/` | 🔄 En evaluación |
| ADR-003 | Cache de tokenizadores con `functools.lru_cache` | ✅ Aceptado |
| ADR-004 | Async en `core/pipeline.py` | ⏳ Pendiente |