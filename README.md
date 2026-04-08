# 🧮 OPENIA — Calculadora de Precios, Tokens y Proyecciones

![CI Pipeline](https://github.com/tu-usuario/openia/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Librería Python para calcular **costes de uso de APIs de IA**, gestionar **tokens**, estimar **precios** por modelo y generar **proyecciones económicas** de consumo. Diseñada para ser modular, testeable y fácilmente integrable en cualquier proyecto que consuma modelos de lenguaje.

---

# 📋 Tabla de contenidos

- [Descripción](#descripción)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura de carpetas](#estructura-de-carpetas)
- [Tests](#tests)
- [Pipeline CI](#pipeline-ci)
- [Licencia](#licencia)

---

# Descripción

**OPENIA** proporciona tres módulos principales dentro del paquete `calculadora`:

| Módulo | Responsabilidad |
|---|---|
| `precios.py` | Consulta y cálculo de precios por modelo y proveedor |
| `tokens.py` | Conteo y estimación de tokens para distintos modelos |
| `proyecciones.py` | Proyecciones de coste mensual/anual según volumen de uso |

---

# Instalación

## Requisitos previos

- Python 3.10 o superior
- `pip` actualizado

## Instalación desde el repositorio

```bash
# 1. Clona el repositorio
git clone https://github.com/tu-usuario/openia.git
cd openia

# 2. Crea y activa un entorno virtual (recomendado)
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows

# 3. Instala las dependencias
pip install -r requirements.txt

# 4. Instala el paquete en modo editable
pip install -e .
```

---

# Uso

## Calcular el coste de una llamada

```python
from calculadora.precios import calcular_precio

coste = calcular_precio(modelo="gpt-4o", tokens_entrada=500, tokens_salida=300)
print(f"Coste estimado: ${coste:.6f}")
```

## Contar tokens de un texto

```python
from calculadora.tokens import contar_tokens

n_tokens = contar_tokens("Hola, ¿cuántos tokens tiene esta frase?", modelo="gpt-4o")
print(f"Tokens: {n_tokens}")
```

## Generar una proyección mensual

```python
from calculadora.proyecciones import proyeccion_mensual

resultado = proyeccion_mensual(
    modelo="gpt-4o",
    llamadas_dia=1000,
    tokens_por_llamada=800
)
print(f"Coste mensual estimado: ${resultado['total_mes']:.2f}")
```

## Script de inicio rápido

El archivo `main.py` en la raíz incluye ejemplos de uso de los tres módulos:

```bash
python main.py
```

---

# Estructura de carpetas

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

---

# Tests

El proyecto usa **pytest** como framework de testing. Los tests cubren los tres módulos del paquete `calculadora`.

## Ejecutar todos los tests

```bash
pytest
```

## Ejecutar con reporte de cobertura

```bash
pytest --cov=calculadora --cov-report=term-missing
```

## Ejecutar un módulo de tests específico

```bash
pytest tests/test_precios.py
pytest tests/test_tokens.py
pytest tests/test_proyecciones.py
```

## Ejecutar con salida detallada

```bash
pytest -v
```

> La configuración de pytest se encuentra en `pytest.ini` y los fixtures compartidos en `conftest.py`.

---

# Pipeline CI

El proyecto incluye un pipeline de **Integración Continua** con GitHub Actions que se ejecuta automáticamente en cada `push` y `pull request` a la rama principal.

## ¿Qué hace el pipeline?

1. **Lint** — Comprueba el estilo de código con `flake8`
2. **Tests** — Ejecuta la suite completa con `pytest`
3. **Cobertura** — Genera informe de cobertura de código

## Estado actual

![CI Pipeline](https://github.com/tu-usuario/openia/actions/workflows/ci.yml/badge.svg)

## Configuración del workflow

El workflow se define en `.github/workflows/ci.yml`. Ejemplo de configuración:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Lint with flake8
        run: flake8 calculadora/ tests/
      - name: Run tests
        run: pytest --cov=calculadora
```

---

# Licencia

Este proyecto está licenciado bajo los términos de la licencia **MIT**. Consulta el archivo [LICENSE](LICENSE MIT) para más información.

---

> Documentación técnica extendida disponible en la carpeta [`docs/`](docs/).