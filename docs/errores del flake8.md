# 📝 Reporte de Errores: Flake8 Audit

## 1. Espacios en blanco al final de la línea (W291)
Archivos afectados:

calculadora/proyecciones.py (Líneas 17, 18, 19, 20)

tests/test_precios.py(Línea 25)

Descripción: Has dejado espacios vacíos (presionaste la barra espaciadora) justo antes de pulsar "Enter".

Por qué importa: Estos espacios son "invisibles" y pueden causar problemas en sistemas de control de versiones como Git, ensuciando los historiales de cambios.

Solución: Borra cualquier espacio que esté al final de esas líneas. El cursor debe terminar inmediatamente después del último carácter o símbolo.

## 2. Marcadores de seno de la cuerda F ( F541)

Archivo afectado: main.py (Línea 37)

Descripción: Has declarado una cadena como f"texto", pero no hay ninguna variable dentro de llaves {}.

Por qué importa: Usar el prefijo f consume recursos innecesarios (aunque mínimos) si no se va a realizar ninguna interpolación de variables.

Solución:

Opción A: Quita la f del principio si es solo texto plano: "Tu texto aquí".

Opción B: Incluye la variable que falta entre llaves: f"El resultado es {variable}".

# 🛠️ Guía de corrección paso a paso
Sigue estos pasos para que tu código pase el check de Flake8:

Paso 1: Corregirmain.py
Busca la línea 37. Probablemente se vea así:

Pitón
print(f"Calculando costes...") # Error F541 (falta variable)
Cambial a:

Pitón
print("Calculando costes...") # Eliminamos la 'f' innecesaria
Paso 2: Limpiar calculadora/proyecciones.py y tests/test_precios.py
Para eliminar los espacios finales (W291), puedes hacerlo manualmente o usar un comando si estás en Linux/Mac:

Intento
# Elimina espacios al final de las líneas en todo el proyecto
sed -i 's/[[:space:]]*$//' calculadora/proyecciones.py tests/test_precios.py
Si usas VS Code, puedes activar la opción "files.trimTrailingWhitespace": true en tu configuración para que esto no vuelva a ocurrir.

Paso 3: Verificar la longitud de línea
Has ejecutado Flake8 con --max-line-length=100. Asegúrate de que las nuevas líneas que escribas no superen este límite para evitar el error E501. 

# 📊 Tabla resumen para tu documentación

| Archivo | Error | Tipo | Gravedad | Solución |
| :--- | :--- | :--- | :--- | :--- |
| `calculadora/proyecciones.py` | `W291` | Estilo | Baja | Eliminar espacios invisibles (trailing whitespace) al final de las líneas 17 a 20. |
| `main.py` | `F541` | Sintaxis | Media | Quitar el prefijo `f` de la cadena en la línea 37, ya que no contiene variables entre llaves `{}`. |
| `tests/test_precios.py` | `W291` | Estilo | Baja | Eliminar el espacio en blanco al final de la línea 25. |