# Señales vistas desde el tiempo y la frecuencia

Simulación en Python de un pulso rectangular, una función escalón y una senoide. El programa utiliza `np.fft.fft()` para calcular magnitud y fase, verifica la linealidad y el desplazamiento circular y compara las senoides de 8 y 16 Hz. Genera las gráficas utilizadas en la presentación.

## Cómo ejecutarlo

Se requiere Python 3.10 o posterior. En una terminal, dentro de esta carpeta:

```bash
python -m venv .venv
```

Activa el entorno: `.venv\Scripts\activate` en Windows o `source .venv/bin/activate` en macOS/Linux. Después:

```bash
python -m pip install -r requirements.txt
python analisis_senales.py
```

El programa crea `resultados/` y guarda cinco figuras PNG y `resumen.txt`. Las figuras incluidas en esta carpeta permiten consultar el resultado sin instalar Python.

## Qué muestra cada archivo

| Archivo | Contenido |
| --- | --- |
| `pulso.png` | Pulso en tiempo, magnitud y fase. |
| `escalon.png` | Escalón en tiempo, magnitud y fase. |
| `senoide.png` | Senoide de 8 Hz con picos en ±8 Hz. |
| `desplazamiento.png` | Magnitud conservada y fase modificada al desplazar el pulso. |
| `frecuencias.png` | Comparación temporal y espectral de 8 y 16 Hz. |
| `resumen.txt` | Parámetros y errores de comprobación numérica. |

## Consideraciones del análisis

Se toman 512 muestras a 256 Hz durante 2 segundos. La resolución espectral es de 0.5 Hz. La FFT se divide entre 512; para una senoide real de amplitud 1 aparecen dos picos de magnitud 0.5. La fase no se dibuja donde la magnitud es casi nula porque allí el ángulo no es estable.

La prueba de desplazamiento usa `np.roll`, es decir, un **corrimiento circular** de 32 muestras. La FFT presupone una secuencia periódica. Por su parte, el escalón tiene una duración finita en el programa: sus resultados no describen la transformada continua de un escalón ideal infinito.

## Subirlo a GitHub

Crea un repositorio en tu cuenta y carga el contenido de esta carpeta: el archivo Python, `requirements.txt`, `README.md`, `.gitignore` y `resultados/`. Ejecuta el programa localmente cuando quieras regenerar las figuras.
