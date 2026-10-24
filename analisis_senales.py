"""Analiza pulso, escalón y senoide mediante la FFT de NumPy.

Uso: python analisis_senales.py
Las figuras y un resumen numérico se escriben en resultados/.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # Guarda PNG sin requerir una ventana gráfica.
import matplotlib.pyplot as plt
import numpy as np


# Parámetros de muestreo comunes a todos los experimentos.
FS = 256  # Muestras por segundo.
N = 512  # Dos segundos de observación: N / FS = 2 s.
T = np.arange(N) / FS
F = np.fft.fftshift(np.fft.fftfreq(N, d=1 / FS))
RESULTADOS = Path(__file__).resolve().parent / "resultados"

# Paleta de las figuras incluidas en la presentación.
FONDO = "#121D30"
TEXTO = "#F4F1E8"
REJILLA = "#526078"
VERDE = "#C5E86C"
CORAL = "#FF8E72"
AZUL = "#78C9DB"


def fft_normalizada(x):
    """Calcula FFT(x)/N y centra el componente de 0 Hz en el eje horizontal."""
    return np.fft.fftshift(np.fft.fft(x)) / N


def preparar_estilo():
    """Configura Matplotlib para figuras legibles sobre fondo oscuro."""
    plt.rcParams.update({
        "figure.facecolor": FONDO, "axes.facecolor": FONDO,
        "axes.edgecolor": REJILLA, "axes.labelcolor": TEXTO,
        "text.color": TEXTO, "xtick.color": TEXTO,
        "ytick.color": TEXTO, "font.size": 11,
    })


def preparar_eje(ax):
    ax.grid(color=REJILLA, alpha=0.28)
    ax.spines[["top", "right"]].set_visible(False)


def figura_senal(x, archivo):
    """Dibuja tiempo, magnitud y fase de una señal en un solo PNG."""
    X = fft_normalizada(x)
    magnitud = np.abs(X)
    fase = np.angle(X)

    # Cerca de cero, el ángulo se vuelve inestable por ruido numérico.
    fase[magnitud < 0.005 * magnitud.max()] = np.nan
    visible = np.abs(F) <= 32  # Acercamiento para estudiar la parte principal.

    fig = plt.figure(figsize=(10.8, 5.5), layout="constrained")
    area = fig.add_gridspec(2, 2, height_ratios=[1, 1.05])
    tiempo = fig.add_subplot(area[0, :])
    espectro = fig.add_subplot(area[1, 0])
    angulo = fig.add_subplot(area[1, 1])

    tiempo.plot(T, x, color=VERDE, lw=2.5)
    tiempo.set(title="01  Señal muestreada", xlabel="Tiempo (s)",
               ylabel="Amplitud", xlim=(0, N / FS))
    espectro.plot(F[visible], magnitud[visible], color=CORAL, lw=2)
    espectro.set(title="02  Magnitud", xlabel="Frecuencia (Hz)",
                 ylabel="|X[k]|/N")
    angulo.scatter(F[visible], fase[visible], color=AZUL, s=10)
    angulo.set(title="03  Fase", xlabel="Frecuencia (Hz)",
               ylabel="Fase (rad)", ylim=(-3.4, 3.4))

    for ax in (tiempo, espectro, angulo):
        preparar_eje(ax)
    fig.savefig(RESULTADOS / archivo, dpi=155, facecolor=FONDO)
    plt.close(fig)


def figura_desplazamiento(pulso, desplazado):
    """Compara magnitud y cambio de fase tras un corrimiento circular."""
    X, Y = fft_normalizada(pulso), fft_normalizada(desplazado)
    zona = (F >= -24) & (F <= 24)
    significativos = zona & (np.abs(X) > 0.01 * np.max(np.abs(X)))
    fig, ax = plt.subplots(1, 2, figsize=(10.8, 3.7), layout="constrained")

    ax[0].plot(F[zona], np.abs(X[zona]), color=VERDE, lw=2.7, label="Original")
    ax[0].plot(F[zona], np.abs(Y[zona]), color=CORAL, lw=1.7,
               ls="--", label="Desplazada")
    ax[0].set(title="Magnitud: curvas superpuestas", xlabel="Frecuencia (Hz)",
              ylabel="|X[k]|/N")
    # La razón Y/X mide el cambio de fase en componentes no nulas.
    ax[1].scatter(F[significativos], np.angle(Y[significativos] / X[significativos]),
                  color=AZUL, s=16)
    ax[1].set(title="Diferencia de fase", xlabel="Frecuencia (Hz)",
              ylabel="Ángulo (rad)", ylim=(-3.4, 3.4))
    for eje in ax:
        preparar_eje(eje)
    ax[0].legend(facecolor=FONDO, labelcolor=TEXTO, edgecolor=REJILLA)
    fig.savefig(RESULTADOS / "desplazamiento.png", dpi=155, facecolor=FONDO)
    plt.close(fig)


def figura_frecuencias(seno_8, seno_16):
    """Expone el periodo más corto y el traslado de los picos a 16 Hz."""
    zona = (F >= 0) & (F <= 22)
    fig, ax = plt.subplots(1, 2, figsize=(10.8, 3.7), layout="constrained")
    ax[0].plot(T, seno_8, color=VERDE, label="8 Hz")
    ax[0].plot(T, seno_16, color=CORAL, alpha=0.85, label="16 Hz")
    ax[0].set(title="Doble oscilación en el mismo tiempo", xlabel="Tiempo (s)",
              ylabel="Amplitud", xlim=(0, 0.5))

    for x, etiqueta, color in [(seno_8, "8 Hz", VERDE), (seno_16, "16 Hz", CORAL)]:
        ax[1].stem(F[zona], np.abs(fft_normalizada(x)[zona]),
                   linefmt=color, markerfmt="o", basefmt=" ", label=etiqueta)
    ax[1].set(title="Picos positivos", xlabel="Frecuencia (Hz)", ylabel="|X[k]|/N")
    for eje in ax:
        preparar_eje(eje)
        eje.legend(facecolor=FONDO, labelcolor=TEXTO, edgecolor=REJILLA)
    fig.savefig(RESULTADOS / "frecuencias.png", dpi=155, facecolor=FONDO)
    plt.close(fig)


def main():
    RESULTADOS.mkdir(exist_ok=True)
    preparar_estilo()

    # Un pulso de 0.25 s, un escalón y dos frecuencias de la senoide.
    pulso = (np.abs(T - 0.75) < 0.125).astype(float)
    escalon = (T >= 0.75).astype(float)
    seno_8 = np.sin(2 * np.pi * 8 * T)
    seno_16 = np.sin(2 * np.pi * 16 * T)

    figura_senal(pulso, "pulso.png")
    figura_senal(escalon, "escalon.png")
    figura_senal(seno_8, "senoide.png")

    # La linealidad permite transformar cada término antes o después de sumar.
    a, b = 0.7, 1.2
    lhs = fft_normalizada(a * pulso + b * seno_8)
    rhs = a * fft_normalizada(pulso) + b * fft_normalizada(seno_8)
    error_linealidad = np.max(np.abs(lhs - rhs))

    # np.roll desplaza circularmente 32 muestras (0.125 s).
    # Esa periodicidad es la que usa la transformada discreta de Fourier.
    m = 32
    desplazado = np.roll(pulso, m)
    k_sobre_n = np.fft.fftshift(np.fft.fftfreq(N))
    factor = np.exp(-2j * np.pi * k_sobre_n * m)
    X = fft_normalizada(pulso)
    Y = fft_normalizada(desplazado)
    error_desplazamiento = np.max(np.abs(Y - X * factor))
    error_magnitud = np.max(np.abs(np.abs(Y) - np.abs(X)))
    figura_desplazamiento(pulso, desplazado)
    figura_frecuencias(seno_8, seno_16)

    reporte = (
        f"Muestreo: {FS} Hz; duración: {N/FS:g} s; N = {N}; resolución: {FS/N:g} Hz\n"
        f"Linealidad, error máximo: {error_linealidad:.3e}\n"
        f"Desplazamiento circular: {m} muestras = {m/FS:g} s\n"
        f"Desplazamiento, error máximo: {error_desplazamiento:.3e}\n"
        f"Conservación de magnitud, diferencia máxima: {error_magnitud:.3e}\n"
        "Senoide: picos en ±8 Hz; al duplicar la frecuencia, ±16 Hz.\n"
        "Nota: el escalón analizado es un registro finito, no un escalón infinito.\n"
    )
    (RESULTADOS / "resumen.txt").write_text(reporte, encoding="utf-8")
    print(reporte)


if __name__ == "__main__":
    main()
