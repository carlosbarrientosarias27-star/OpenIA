# Guía de Contribución

¡Gracias por tu interés en contribuir! Esta guía cubre todo lo que necesitas para empezar: configuración del entorno, convenciones de código y proceso de Pull Request.

---

# Requisitos previos

| Herramienta | Versión mínima | Comprobación |
|-------------|---------------|--------------|
| Python      | 3.11          | `python --version` |
| Git         | 2.40          | `git --version` |
| uv *(recomendado)* | 0.4 | `uv --version` |

> **Nota:** Se puede usar `pip` + `venv` en lugar de `uv`, pero los ejemplos de esta guía usan `uv` por velocidad y reproducibilidad.

---

# Configuración del entorno de desarrollo

## 1. Fork y clon

```bash
# Haz fork desde GitHub y luego:
git clone https://github.com/TU_USUARIO/nombre-repo.git
cd nombre-repo
```

## 2. Crear entorno virtual e instalar dependencias

```bash
# Con uv (recomendado)
uv venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows

uv pip install -e ".[dev]"

# Con pip tradicional
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

El extra `[dev]` instala todas las herramientas de desarrollo: `pytest`, `ruff`, `mypy`, `pre-commit`, etc.

## 3. Configurar pre-commit

```bash
pre-commit install
```

Esto instala hooks que se ejecutan antes de cada commit: linting (`ruff`), formateo (`ruff format`) y comprobación de tipos (`mypy`).

## 4. Copiar variables de entorno

```bash
cp .env.example .env
# Edita .env con tus valores locales (API keys, etc.)
```

## 5. Verificar que todo funciona

```bash
pytest
```

Si todos los tests pasan, el entorno está correctamente configurado.

---

# Estructura del repositorio

```
.
├── src/
│   ├── core/
│   ├── tokens/
│   ├── precios/
│   ├── modelos/
│   └── utils/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── docs/
├── .env.example
├── pyproject.toml
└── README.md
```

---

# Convenciones de código

## Estilo

- **Formateador:** `ruff format` (compatible con Black, líneas de 88 caracteres).
- **Linter:** `ruff check` con reglas `E`, `F`, `I`, `UP`, `B`.
- **Tipos:** Todos los métodos públicos deben tener anotaciones de tipo completas. Se comprueba con `mypy --strict`.

Ejecutar manualmente:

```bash
ruff format .
ruff check . --fix
mypy src/
```

## Nomenclatura

| Elemento | Convención | Ejemplo |
|----------|-----------|---------|
| Módulos y paquetes | `snake_case` | `token_counter.py` |
| Clases | `PascalCase` | `PriceCalculator` |
| Funciones y métodos | `snake_case` | `count_tokens()` |
| Constantes | `UPPER_SNAKE_CASE` | `MAX_CONTEXT_TOKENS` |
| Variables privadas | prefijo `_` | `_cache` |

### Docstrings

Se usa el estilo **Google**. Todo símbolo público debe tener docstring:

```python
def estimate(self, usage: TokenUsage, model: str) -> PriceEstimate:
    """Estima el coste de una llamada a partir del uso de tokens.

    Args:
        usage: Conteo de tokens de entrada y salida.
        model: Identificador del modelo (p. ej. ``"gpt-4o"``).

    Returns:
        PriceEstimate con el desglose de costes en la moneda configurada.

    Raises:
        ModelNotFoundError: Si el modelo no tiene tarifas registradas.
    """
```

---

# Commits semánticos

Este proyecto sigue [Conventional Commits](https://www.conventionalcommits.org/es/v1.0.0/).

## Formato

```
<tipo>(<ámbito>): <descripción corta en imperativo>

[cuerpo opcional]

[pie opcional: BREAKING CHANGE, referencias a issues]
```

## Tipos válidos

| Tipo | Cuándo usarlo |
|------|--------------|
| `feat` | Nueva funcionalidad visible para el usuario |
| `fix` | Corrección de un bug |
| `docs` | Solo cambios en documentación |
| `style` | Formato, espacios, comas (sin cambio de lógica) |
| `refactor` | Refactorización sin cambio de comportamiento |
| `perf` | Mejora de rendimiento |
| `test` | Añadir o corregir tests |
| `chore` | Tareas de mantenimiento (deps, CI, build) |
| `ci` | Cambios en la configuración de CI/CD |

## Ejemplos

```bash
# ✅ Correcto
git commit -m "feat(precios): añadir soporte para tarifas en EUR"
git commit -m "fix(tokens): corregir conteo erróneo con caracteres Unicode"
git commit -m "docs(api_referencia): documentar método batch_estimate"
git commit -m "test(tokens): añadir casos de prueba para truncate()"

# ❌ Incorrecto
git commit -m "arreglos varios"
git commit -m "WIP"
git commit -m "fixed bug"
```

## Cambios que rompen compatibilidad

Añadir `!` después del tipo o un pie `BREAKING CHANGE:`:

```bash
git commit -m "feat(modelos)!: renombrar TokenUsage.tokens_entrada a input_tokens

BREAKING CHANGE: El atributo anterior queda eliminado.
Actualizar todos los usos a input_tokens."
```

---

# Ejecutar tests

## Tests unitarios

```bash
pytest tests/unit/
```

### Tests de integración

Requieren las variables de entorno del `.env`:

```bash
pytest tests/integration/
```

### Cobertura

```bash
pytest --cov=src --cov-report=term-missing --cov-report=html
# El informe HTML se genera en htmlcov/index.html
```

## Filtros útiles

```bash
# Solo tests de un módulo
pytest tests/unit/tokens/ -v

# Solo tests con una marca concreta
pytest -m "not slow"

# Detener al primer fallo
pytest -x
```

### Requisito de cobertura

Los PRs deben mantener una cobertura global **≥ 90 %**. La CI rechazará PRs que la bajen.

---

# Proceso de Pull Request

## 1. Crear una rama

```bash
git checkout -b tipo/descripcion-corta
# Ejemplos:
git checkout -b feat/soporte-eur
git checkout -b fix/unicode-truncate
git checkout -b docs/guia-contribucion
```

## 2. Desarrollar y hacer commits

Trabaja en tu rama haciendo commits atómicos siguiendo las convenciones de arriba. Cada commit debe compilar y pasar los tests.

## 3. Mantener la rama actualizada

```bash
git fetch origin
git rebase origin/main
```

Se prefiere `rebase` sobre `merge` para mantener un historial lineal.

## 4. Abrir el Pull Request

- Ve a GitHub y abre el PR contra `main`.
- Rellena la plantilla de PR (se carga automáticamente).
- Comprueba que todos los checks de CI estén en verde antes de solicitar revisión.

### Plantilla de PR

```markdown
## Descripción
<!-- Qué cambia y por qué -->

## Tipo de cambio
- [ ] Bug fix
- [ ] Nueva funcionalidad
- [ ] Breaking change
- [ ] Documentación

## Tests
- [ ] He añadido tests que cubren el cambio
- [ ] Todos los tests existentes pasan

## Checklist
- [ ] El código sigue las convenciones del proyecto
- [ ] He actualizado la documentación si es necesario
- [ ] He añadido una entrada en CHANGELOG.md
```

## 5. Revisión y merge

- Al menos **1 aprobación** de un maintainer es obligatoria.
- El merge se hace con **Squash and Merge** para mantener el historial limpio.
- El título del PR se usará como mensaje del commit final (debe seguir Conventional Commits).

---

# Reportar bugs

Usa las [GitHub Issues](../../issues) con la plantilla de bug report. Incluye siempre:

1. Versión del proyecto (`python -c "import pkg; print(pkg.__version__)"`)
2. Versión de Python y sistema operativo
3. Pasos mínimos para reproducir el error
4. Comportamiento esperado vs. comportamiento observado
5. Traceback completo si aplica

---

# Código de conducta

Este proyecto sigue el [Contributor Covenant v2.1](https://www.contributor-covenant.org/es/version/2/1/code_of_conduct/). Sé respetuoso, constructivo e inclusivo en todas las interacciones.