# 🛡️ Reporte de Seguridad: Bandit
El Error Principal:B101: assert_used

- Gravedad: Baja | Confianza: Alta

- Ubicación: 16 ocurrencias en ./tests/test_precios.py

- Descripción: Bandit ha detectado el uso de la palabra clave assert.

- Relacionado con CWE: CWE-703(Manejo inadecuado de condiciones de excepción).

# 🔍 ¿Por qué Bandit marca esto como un problema?
En Python, cuando compilas o ejecutas código con optimización (usando el flag -O), todas las sentencias assert se eliminan por completo del bytecode para mejorar el rendimiento.

El riesgo: Si usas assert para validar seguridad o lógica crítica en producción (ej. assert user.is_admin), un atacante podría saltarse esa validación simplemente ejecutando el código en modo optimizado.

La paradoja: En el archivo test_precios.py, los asserts son necesarios porque así es como funciona pytest. Bandit, por defecto, analiza todos los archivos y no sabe distinguir automáticamente que este es un archivo de pruebas donde el riesgo es irrelevante.

# 🛠️ Guía de solución paso a paso
Tienes tres formas de abordar esto, dependiendo de qué tan "limpio" quieras dejar tu pipeline de CI/CD:

- Opción A: Ignorar el error en la línea (Recomendado para casos aislados)
Si solo quieres que Bandit ignore una línea específica, añade un comentario # nosec:

Pitón
assert isinstance(calculadora.precios.PRECIOS_MODELS, dict)  # nosec

- Opción B: Excluir la carpeta de tests (La mejor práctica)
Como los tests deben usar asserts y no se despliegan en producción, lo ideal es configurar Bandit para que no analice la carpeta tests. Modifica tu comando de ejecución:

Intento
## Usa el flag -x para excluir directorios
bandit -r . -x ./tests
Nota: En tu log aparece que intentaste usar -x, pero hubo un error de sintaxis en el comando (./-x), asegúrate de escribirlo correctamente.

- Opción C: Cambiar assert por validaciones if/raise (Solo para código de producción)
Si este error apareciera en costesInicio.py, la solución correcta no sería ignorarlo, sino cambiarlo por una excepción real:

Pitón
## MAL (Bandit se quejará)
assert tokens_input > 0

## BIEN (Seguro para producción)
if tokens_input <= 0:
    raise ValueError("Los tokens deben ser mayores a cero")

# 📋 Resumen del estado del proyecto

| Archivo | Herramienta | Estado | Descripción del Incidente | Acción Correctiva |
| :--- | :--- | :--- | :--- | :--- |
| `costesInicio.py` | **Flake8** | ❌ Error | Importaciones no usadas (`os`, `openai`), líneas demasiado largas (>79 car.) y exceso de espacios en blanco. | Limpiar importaciones, ajustar saltos de línea y formatear según PEP 8. |
| `precios.py` | **Flake8** | ❌ Error | Falta un salto de línea (`newline`) al final del archivo. | Añadir una línea vacía al final del documento. |
| `test_precios.py` | **Bandit** | ⚠️ Alerta | **Falso Positivo:** Uso de `assert` detectado (`B101`). Bandit lo marca como riesgo porque los asserts se pueden omitir en producción. | **No corregir código:** Excluir la carpeta `./tests` del análisis de Bandit o usar `# nosec`. |