# Memoria Final — Refactorización de `costesInicio.py`

# 1. Descripción del proyecto

El archivo `costesInicio.py` es el punto de partida de una calculadora de costes de APIs de inteligencia artificial. Su función es estimar el gasto en tokens para distintos modelos (OpenAI, Anthropic, Google) a partir de llamadas individuales o proyecciones mensuales.

Durante la revisión del código original se detectaron varios problemas de distinta gravedad: importaciones innecesarias, incompatibilidades técnicas, errores de diseño arquitectónico y datos desactualizados. A continuación se documentan todos ellos junto con los cambios aplicados.

---

# 2. Problemas detectados en el código original

## 2.1 Importación de `OpenAI` sin uso real

```python
# Código original
import os
from openai import OpenAI
```

**Problema:** Se importa el cliente `OpenAI` pero nunca se instancia ni se utiliza en ningún punto del archivo. Igualmente, `os` se importa pero no se emplea en ninguna operación. Estas importaciones generan dependencias innecesarias, aumentan el tiempo de arranque y confunden a cualquier desarrollador que lea el código pensando que el cliente se usa activamente.

**Cambio realizado:** Se eliminaron ambas importaciones. El archivo solo conserva `import tiktoken`, que sí se usa en el método `estimar_tokens`.

---

## 2.2 `tiktoken` no es compatible con modelos ajenos a OpenAI

```python
def estimar_tokens(self, texto: str) -> int:
    encoding = tiktoken.encoding_for_model(self.modelo)
    return len(encoding.encode(texto))
```

**Problema:** `tiktoken` es una librería de OpenAI y únicamente conoce los tokenizadores de sus propios modelos. Si se instancia `CalculadoraCostes("claude-3-sonnet")` o `CalculadoraCostes("gemini-1.5-pro")` y luego se llama a `estimar_tokens()`, la función lanza una excepción `KeyError` porque `tiktoken` no reconoce esos identificadores de modelo.

Dado que el diccionario `PRECIOS` incluye modelos de tres proveedores distintos (OpenAI, Anthropic y Google), este fallo es completamente reproducible con el uso normal de la clase.

**Cambio realizado:** Se añadió un bloque `try/except` que intenta usar `tiktoken` cuando el modelo es de OpenAI y, en caso de fallo, aplica la estimación universal de referencia (1 token ≈ 4 caracteres), indicándolo con un comentario. Se añadió además una lista interna `MODELOS_OPENAI` para diferenciar proveedores.

---

## 2.3 Código ejecutable en el ámbito global del módulo

```python
# Código original — ejecutado al importar el archivo
calc = CalculadoraCostes("gpt-4o-mini")
print("=" * 60)
...
```

**Problema:** Todo el bloque de ejemplos y prints se ejecuta directamente en el ámbito global, sin estar protegido por `if __name__ == "__main__":`. Esto provoca que al importar `costesInicio` desde cualquier otro módulo del proyecto (por ejemplo, desde `main.py` o los tests) se imprima toda la salida en consola y se ejecute código que no debería correr en ese contexto. Es un error de diseño habitual que rompe la reusabilidad del módulo.

**Cambio realizado:** Todo el bloque de ejemplos se trasladó dentro del bloque `if __name__ == "__main__":`, de forma que solo se ejecuta cuando el script se lanza directamente.

---

## 2.4 Precios desactualizados y nombre de modelo incorrecto

```python
PRECIOS = {
    ...
    "claude-3-sonnet": {"input": 3.00, "output": 15.00},
    ...
}
```

**Problema:** El identificador `"claude-3-sonnet"` no corresponde a ningún modelo real de Anthropic. El nombre correcto en la API es `"claude-3-sonnet-20240229"`. Usar el alias abreviado provoca que el modelo nunca sea reconocido correctamente si se integrara una llamada real a la API. Además, los precios de varios modelos estaban desactualizados respecto a las tarifas vigentes en 2025.

**Cambio realizado:** Se corrigió el identificador a `"claude-3-5-sonnet-20241022"` (versión estable más reciente en el momento de la revisión) y se revisaron los precios de todos los modelos contrastándolos con las páginas oficiales de cada proveedor.

---

### 2.5 Sin validación de entradas en los métodos públicos

```python
def calcular_costes(self, tokens_input: int, tokens_output: int) -> dict:
    coste_input = (tokens_input / 1_000_000) * self.precios["input"]
```

**Problema:** Los métodos no validan que los parámetros sean valores positivos. Un valor de `tokens_input = 0` en `proyectar_uso_mensual` provoca una `ZeroDivisionError` en la línea `"coste_por_llamada": (...) / llamadas_mensuales` si `llamadas_por_dia` es 0. Del mismo modo, valores negativos producen resultados sin sentido sin ningún aviso.

**Cambio realizado:** Se añadieron guardas al inicio de cada método público que comprueban que los parámetros numéricos sean mayores que cero, lanzando `ValueError` con un mensaje descriptivo si no se cumple la condición.

---

## 2.6 Aproximación incorrecta en el Ejemplo 3

```python
# Ejemplo 3 — código original
calc_documentos.proyectar_uso_mensual(
    llamadas_por_dia=16,  # 500 al mes ≈ 16 al día
    ...
)
print(f"Documentos procesados: {proyeccion_docs['llamadas_mensuales']}")
```

**Problema:** Con `llamadas_por_dia=16` y `dias_mes=30` (valor por defecto), el resultado real es `16 × 30 = 480` documentos, no 500 como indica el comentario y el enunciado del ejemplo. El print además etiqueta el resultado como "Documentos procesados" cuando en realidad devuelve `llamadas_mensuales`, que es 480. Esto introduce una inconsistencia entre lo que el código dice y lo que calcula.

**Cambio realizado:** Se ajustó el valor a `llamadas_por_dia=17` (que da `510 ≈ 500`) y se actualizó el comentario para ser honesto sobre la aproximación. Alternativamente, se puede pasar `dias_mes=31` para obtener `496`. Se documentó la decisión en el comentario inline.

---

# 3. Resumen de cambios aplicados

| # | Tipo de problema | Gravedad | Cambio aplicado |
|---|---|---|---|
| 1 | Importaciones no utilizadas (`os`, `OpenAI`) | Media | Eliminadas |
| 2 | `tiktoken` incompatible con modelos no-OpenAI | Alta | Fallback a estimación por caracteres |
| 3 | Código ejecutable en ámbito global | Alta | Envuelto en `if __name__ == "__main__":` |
| 4 | Nombre de modelo incorrecto (`claude-3-sonnet`) | Media | Corregido al identificador oficial |
| 5 | Sin validación de entradas (posible `ZeroDivisionError`) | Alta | Guardas con `ValueError` añadidas |
| 6 | Aproximación incorrecta en Ejemplo 3 | Baja | Ajuste del parámetro y comentario |

---

# 4. Estructura final del proyecto

Tras la refactorización, el código de `costesInicio.py` queda integrado en la estructura del proyecto `OPENIA` de la siguiente manera:

```
openia/
│
├── calculadora/              # Paquete principal
│   ├── __init__.py
│   ├── precios.py            # Lógica de precios por modelo
│   ├── tokens.py             # Conteo y estimación de tokens
│   └── proyecciones.py       # Proyecciones de coste
│
├── docs/                     # Documentación técnica
│   ├── Api referencia.md
│   ├── arquitectura.md
│   ├── Changelog.md
│   ├── errores de seguridad.md
│   ├── errores del flake8.md
│   ├── Fallo test_precio.md
│   └── Guia de Construccion.md
│
├── tests/                    # Suite de tests
│   ├── __init__.py
│   ├── test_precios.py
│   ├── test_proyecciones.py
│   └── test_tokens.py
│
├── .github/                  # Configuración de GitHub Actions
├── .vscode/                  # Configuración del editor
├── main.py                   # Punto de entrada / ejemplos
├── conftest.py               # Fixtures compartidos de pytest
├── costesInicio.py           # Script de costes iniciales
├── requirements.txt          # Dependencias del proyecto
├── setup.cfg                 # Configuración del paquete y herramientas
├── pytest.ini                # Configuración de pytest
├── .gitignore
└── LICENSE

```

La clase `CalculadoraCostes` ha sido dividida en módulos separados dentro de `calculadora/` para seguir el principio de responsabilidad única, lo que también facilita la cobertura de tests existente en `tests/`.

---

# 5. Conclusión

El código original de `costesInicio.py` presentaba errores que impedirían su funcionamiento correcto en un entorno real: fallaría al estimar tokens para modelos de Anthropic o Google, rompería cualquier módulo que lo importara debido al código global, y produciría una excepción no controlada si algún parámetro fuera cero. Los cambios aplicados resuelven todos estos problemas manteniendo la misma interfaz pública de la clase para no romper la compatibilidad con el resto del proyecto.