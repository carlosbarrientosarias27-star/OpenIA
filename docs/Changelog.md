# Changelog

Todos los cambios notables de este proyecto se documentan en este archivo.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es/1.1.0/),
y el proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

# [Sin publicar]

## Añadido
- Soporte inicial para tarifas en EUR mediante conversión con `forex-python`.
- Propiedad calculada `TokenUsage.total_tokens`.

## En progreso
- Pipeline asíncrono en `core/pipeline.py` (ADR-004).

---

# [1.2.0] — 2025-03-14

## Añadido
- `PriceCalculator.batch_estimate()`: estima el coste de una lista de usos en una sola llamada, reutilizando la consulta de tarifas.
- Nuevo atributo `TokenUsage.cached_tokens` para reflejar tokens servidos desde caché con descuento.
- Soporte para el modelo `claude-3-5-sonnet-20241022` en el catálogo de tarifas.

## Cambiado
- `Tokenizer` ahora acepta el parámetro `model` en el constructor en lugar de en cada llamada a `count()`. Esto reduce la carga de inicializar el vocabulario repetidamente.
- Las tarifas de `gpt-4o` se han actualizado a los precios de marzo 2025 (entrada: $2.50/M, salida: $10.00/M).

## Corregido
- `Tokenizer.truncate()` devolvía un token extra en textos con caracteres Unicode multibyte (#47).
- `PriceCalculator.estimate()` no aplicaba el descuento de `cached_tokens` cuando era igual al total de `input_tokens` (#51).

---

# [1.1.1] — 2025-01-28

## Corregido
- `validate_context()` lanzaba `KeyError` en lugar de `UnsupportedModelError` para modelos desconocidos (#38).
- La serialización de `PriceEstimate` a JSON incluía el campo `total` duplicado (#40).

---

# [1.1.0] — 2025-01-10

## Añadido
- Módulo `core/facade.py` con `EstimationFacade`: interfaz de alto nivel que combina tokenización y cálculo de precio en un único punto de entrada.
- Excepción `ContextLimitExceededError` para señalizar de forma explícita cuando un texto supera el límite del modelo.
- Tests de integración para el flujo completo texto → tokens → precio.

## Cambiado
- `get_rates()` ahora lanza `ModelNotFoundError` (antes devolvía `None`). **Requiere actualizar código que comprobaba `if rates is None`.**
- Se migra el logging de `print()` a `loguru`. Los consumidores que capturaban `stdout` deben actualizar su configuración.

## Obsoleto
- `tokens.counter.count_tokens()` (función suelta): usar `Tokenizer.count()` en su lugar. Se eliminará en v2.0.

## Seguridad
- Actualización de `tiktoken` a 0.7.0 para resolver una vulnerabilidad de path traversal en la carga de vocabularios locales (CVE-2024-XXXXX).

---

# [1.0.0] — 2024-11-20

Primera versión estable con API pública comprometida.

## Añadido
- `Tokenizer`: tokenización y conteo de tokens para modelos GPT-4o, GPT-4-turbo y GPT-3.5-turbo.
- `Tokenizer.encode()` y `Tokenizer.truncate()`.
- `validate_context()`: validación de límite de contexto con tokens reservados para salida.
- `PriceCalculator.estimate()`: cálculo de coste con tarifas de entrada/salida por modelo.
- Modelos de dominio `TokenUsage`, `PriceEstimate` y `ModelRates` basados en Pydantic v2.
- `get_rates()`: consulta de tarifas del catálogo interno.
- Documentación completa: arquitectura, referencia de API y guía de contribución.
- CI con GitHub Actions: lint, tipos, tests y cobertura mínima del 90 %.

---

# [0.3.0] — 2024-10-05

## Añadido
- Separación de `tokens/` y `precios/` en módulos independientes (antes en un único `core.py`). Ver `docs/arquitectura.md` para la justificación.
- Protocolo `Tokenizer` en `core/ports.py` para desacoplar la implementación concreta.

## Cambiado
- **BREAKING:** `estimate_price(text, model)` queda eliminada. Usar `PriceCalculator.estimate(usage, model)`.

---

# [0.2.0] — 2024-09-01

## Añadido
- Soporte para `gpt-4-turbo` y `gpt-3.5-turbo` en el tokenizador.
- Parámetro `reserved_output` en la función de validación de contexto.

## Corregido
- Conteo incorrecto de tokens en textos vacíos (devolvía `None` en lugar de `0`).

---

# [0.1.0] — 2024-07-15

## Añadido
- Prototipo inicial: tokenización con `tiktoken` y estimación de precio para `gpt-4o`.
- Tests unitarios básicos.
- `README.md` con instrucciones de instalación.

---
