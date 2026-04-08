# 📝 Reporte de Errores: Flake8

## 1. Importaciones no utilizadas (F401)

- Error: ./costesInicio.py:2:1: F401 'os' imported but unused

- Error: ./costesInicio.py:3:1: F401 'openai.OpenAI' imported but unused

- Explicación: Has importado las librerías os y OpenAI, pero no las estás usando en ninguna parte del código. Esto ensucia el entorno y consume memoria innecesariamente.

- Solución: Borra las líneas import os y from openai import OpenAI.

## 2. Espacios en blanco y líneas vacías (W293, E303, W291)

- Errores (W293): blank line contains whitespace. Tienes líneas que parecen vacías pero tienen espacios o tabulaciones.

- Error (E303): too many blank lines (3). Has dejado 3 líneas en blanco seguidas; el estándar PEP 8 recomienda máximo 2 entre clases/funciones y 1 dentro de ellas.

- Error (W291): trailing whitespace. Hay espacios al final de una línea de código antes del salto de línea.

- Solución: Limpia las líneas vacías para que sean realmente vacías y asegúrate de que no haya espacios "invisibles" al final de tus frases.

## 3. Longitud de línea excedida (E501)

- Error: line too long (X > 79 characters)

- Explicación: Python recomienda que las líneas no superen los 79 caracteres. Esto facilita la lectura de dos archivos en paralelo o en pantallas pequeñas.

- Solución: Divide las líneas largas. Por ejemplo:

Python
# En lugar de:
proyeccion = calc.proyectar_uso_mensual(llamadas_por_dia=100, tokens_input_por_llamada=200, tokens_output_por_llamada=300)

# Haz esto:
proyeccion = calc.proyectar_uso_mensual(
    llamadas_por_dia=100,
    tokens_input_por_llamada=200,
    tokens_output_por_llamada=300
)
## 4. Estructura y saltos de línea (E305, W292)

- Error (E305): expected 2 blank lines after class or function definition. Falta una línea en blanco extra antes de empezar el código principal tras definir la clase.

- Error (W292): no newline at end of file. Todos los archivos de Python deben terminar con una línea vacía final.

- Solución: Pulsa "Enter" al final de la última línea de tus archivos precios.py y costesInicio.py.

# 🛠️ Paso a paso para corregir el código

Sigue este orden para limpiar tu proyecto:

## Paso 1: Limpieza de Importaciones
Abre costesInicio.py y elimina:

Python
import os
from openai import OpenAI

Paso 2: Ajuste de la Clase y Espaciado

Asegúrate de que entre la definición de la clase y el primer método solo haya una línea. Borra los espacios en las líneas que están "vacías". Al terminar la clase CalculadoraCostes, deja dos líneas en blanco antes de calc = CalculadoraCostes(...).

## Paso 3: Acortar los print y llamadas

En los ejemplos del final (Ejemplo 4 especialmente), los print con muchas variables están superando los 100 caracteres. Usa paréntesis para romper las líneas:

Python
print(
    f"Tokens input: {conversacion['tokens_input']} "
    f"→ ${conversacion['coste_input_usd']:.6f}"
)

## Paso 4: El toque final

Ve al final de precios.py y costesInicio.py, coloca el cursor después del último carácter y presiona Enter una vez. Guarda los archivos.