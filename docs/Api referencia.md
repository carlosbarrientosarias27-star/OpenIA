# Referencia de API

Documentación de todas las clases y funciones públicas del proyecto.  
Generada a partir de los docstrings siguiendo el estándar [Google Style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

---

# Módulo `tokens`

## `tokens.tokenizer.Tokenizer`

Clase principal para tokenizar texto y contar tokens según el vocabulario de un modelo.

```python
class Tokenizer:
    def __init__(self, model: str = "gpt-4o") -> None
```

**Parámetros:**

| Nombre | Tipo | Descripción |
|--------|------|-------------|
| `model` | `str` | Nombre del modelo cuyo vocabulario se usará. Por defecto `"gpt-4o"`. |

**Raises:** `ValueError` si el modelo no está soportado.

---

## `Tokenizer.count`

```python
def count(self, text: str) -> int
```

Cuenta el número de tokens que ocupa un texto para el modelo configurado.

**Parámetros:**

| Nombre | Tipo | Descripción |
|--------|------|-------------|
| `text` | `str` | Texto a tokenizar. Puede ser vacío (devuelve `0`). |

**Retorna:** `int` — Número de tokens.

**Ejemplo:**

```python
from tokens.tokenizer import Tokenizer

tok = Tokenizer(model="gpt-4o")
n = tok.count("Hola, ¿cómo estás?")
print(n)  # → 8
```

---

## `Tokenizer.encode`

```python
def encode(self, text: str) -> list[int]
```

Convierte texto en una lista de IDs de tokens.

**Parámetros:**

| Nombre | Tipo | Descripción |
|--------|------|-------------|
| `text` | `str` | Texto a codificar. |

**Retorna:** `list[int]` — Lista de IDs de tokens.

**Ejemplo:**

```python
ids = tok.encode("Hola mundo")
print(ids)  # → [39, 3452, 952]
```

---

## `Tokenizer.truncate`

```python
def truncate(self, text: str, max_tokens: int) -> str
```

Trunca el texto para que no supere `max_tokens` tokens, preservando palabras completas siempre que sea posible.

**Parámetros:**

| Nombre | Tipo | Descripción |
|--------|------|-------------|
| `text` | `str` | Texto de entrada. |
| `max_tokens` | `int` | Límite máximo de tokens. Debe ser > 0. |

**Retorna:** `str` — Texto truncado.

**Raises:** `ValueError` si `max_tokens <= 0`.

**Ejemplo:**

```python
texto_largo = "palabra " * 10_000
corto = tok.truncate(texto_largo, max_tokens=512)
print(tok.count(corto))  # → 512
```

---

## `tokens.validator.validate_context`

```python
def validate_context(
    text: str,
    model: str,
    reserved_output: int = 0,
) -> bool
```

Comprueba si un texto cabe en la ventana de contexto del modelo, descontando opcionalmente tokens reservados para la respuesta.

**Parámetros:**

| Nombre | Tipo | Descripción |
|--------|------|-------------|
| `text` | `str` | Texto a validar. |
| `model` | `str` | Nombre del modelo. |
| `reserved_output` | `int` | Tokens a reservar para la salida. Por defecto `0`. |

**Retorna:** `bool` — `True` si cabe, `False` si excede el límite.

**Ejemplo:**

```python
from tokens.validator import validate_context

ok = validate_context("Un texto corto.", model="gpt-4o", reserved_output=1000)
print(ok)  # → True
```

---

# Módulo `precios`

## `precios.calculadora.PriceCalculator`

Calcula el coste económico de una llamada a un modelo a partir del uso de tokens.

```python
class PriceCalculator:
    def __init__(self, currency: str = "USD") -> None
```

**Parámetros:**

| Nombre | Tipo | Descripción |
|--------|------|-------------|
| `currency` | `str` | Moneda de salida. Valores aceptados: `"USD"`, `"EUR"`. Por defecto `"USD"`. |

---

## `PriceCalculator.estimate`

```python
def estimate(
    self,
    usage: TokenUsage,
    model: str,
) -> PriceEstimate
```

Estima el coste de una llamada dados el uso de tokens y el modelo.

**Parámetros:**

| Nombre | Tipo | Descripción |
|--------|------|-------------|
| `usage` | `TokenUsage` | Objeto con conteo de tokens de entrada y salida. |
| `model` | `str` | Nombre del modelo para consultar tarifas. |

**Retorna:** [`PriceEstimate`](#modelesprecioestimate) con el desglose de costes.

**Raises:** `ModelNotFoundError` si el modelo no tiene tarifas registradas.

**Ejemplo:**

```python
from precios.calculadora import PriceCalculator
from modelos.uso import TokenUsage

calc = PriceCalculator(currency="EUR")
usage = TokenUsage(input_tokens=1500, output_tokens=300)
estimate = calc.estimate(usage, model="gpt-4o")

print(estimate.total)        # → 0.0243
print(estimate.currency)     # → "EUR"
```

---

## `PriceCalculator.batch_estimate`

```python
def batch_estimate(
    self,
    usages: list[TokenUsage],
    model: str,
) -> list[PriceEstimate]
```

Estima el coste para una lista de usos. Equivalente a llamar `estimate` en bucle pero más eficiente al reutilizar la consulta de tarifas.

**Parámetros:**

| Nombre | Tipo | Descripción |
|--------|------|-------------|
| `usages` | `list[TokenUsage]` | Lista de usos de tokens. |
| `model` | `str` | Modelo a usar para todas las estimaciones. |

**Retorna:** `list[PriceEstimate]` en el mismo orden que `usages`.

---

## `precios.tarifas.get_rates`

```python
def get_rates(model: str) -> ModelRates
```

Obtiene las tarifas (por millón de tokens) para un modelo dado.

**Parámetros:**

| Nombre | Tipo | Descripción |
|--------|------|-------------|
| `model` | `str` | Identificador del modelo (e.g. `"gpt-4o"`, `"claude-3-5-sonnet"`). |

**Retorna:** [`ModelRates`](#modelesmodelorates) con las tarifas de entrada y salida.

**Raises:** `ModelNotFoundError` si el modelo no está en el catálogo.

**Ejemplo:**

```python
from precios.tarifas import get_rates

rates = get_rates("gpt-4o")
print(rates.input_per_million)   # → 2.50
print(rates.output_per_million)  # → 10.00
```

---

# Módulo `modelos`

## `modelos.uso.TokenUsage`

Representa el consumo de tokens de una llamada.

```python
class TokenUsage(BaseModel):
    input_tokens: int
    output_tokens: int
    cached_tokens: int = 0
```

**Atributos:**

| Nombre | Tipo | Descripción |
|--------|------|-------------|
| `input_tokens` | `int` | Tokens de prompt (entrada). |
| `output_tokens` | `int` | Tokens generados (salida). |
| `cached_tokens` | `int` | Tokens servidos desde caché (descuento aplicable). Por defecto `0`. |

**Propiedad calculada:**

```python
@property
def total_tokens(self) -> int:
    return self.input_tokens + self.output_tokens
```

---

## `modelos.precio.PriceEstimate`

Resultado del cálculo de precio para una llamada.

```python
class PriceEstimate(BaseModel):
    input_cost: float
    output_cost: float
    currency: str
    model: str
```

**Propiedad calculada:**

```python
@property
def total(self) -> float:
    return round(self.input_cost + self.output_cost, 6)
```

---

## `modelos.modelo.ModelRates`

Tarifas de un modelo concreto.

```python
class ModelRates(BaseModel):
    model: str
    input_per_million: float
    output_per_million: float
    cached_input_per_million: float = 0.0
```

---

# Módulo `core`

## `core.facade.EstimationFacade`

Punto de entrada unificado para estimar el coste de un texto antes de enviarlo a un modelo.

```python
class EstimationFacade:
    def __init__(
        self,
        model: str,
        currency: str = "USD",
    ) -> None
```

## `EstimationFacade.estimate_from_text`

```python
def estimate_from_text(
    self,
    prompt: str,
    expected_output_tokens: int = 0,
) -> PriceEstimate
```

**Ejemplo completo:**

```python
from core.facade import EstimationFacade

facade = EstimationFacade(model="gpt-4o", currency="EUR")
estimate = facade.estimate_from_text(
    prompt="Explica la relatividad especial en 3 párrafos.",
    expected_output_tokens=400,
)

print(f"Coste estimado: {estimate.total} {estimate.currency}")
# → Coste estimado: 0.005120 EUR
```

---

# Excepciones

| Excepción | Módulo | Descripción |
|-----------|--------|-------------|
| `ModelNotFoundError` | `precios.excepciones` | El modelo solicitado no tiene tarifas registradas. |
| `ContextLimitExceededError` | `tokens.excepciones` | El texto supera el límite de contexto del modelo. |
| `UnsupportedModelError` | `tokens.excepciones` | El modelo no está soportado por el tokenizador. |
| `CurrencyConversionError` | `precios.excepciones` | No se pudo obtener el tipo de cambio. |