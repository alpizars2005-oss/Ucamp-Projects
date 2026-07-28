import random

import matplotlib.pyplot as plt


def simular_maquina_galton(cantidad_canicas=3000, niveles=12):
    """
    Simula la caída de canicas en una máquina de Galton.

    Cada canica atraviesa una cantidad determinada de niveles. En cada nivel
    elige aleatoriamente entre izquierda (0) y derecha (1). La suma de los
    desplazamientos a la derecha determina el contenedor final.

    Parámetros:
        cantidad_canicas (int): Número de canicas que se simularán.
        niveles (int): Cantidad de obstáculos que atraviesa cada canica.

    Retorna:
        list: Contenedor final de cada canica.
    """
    resultados = []

    # Simular la caída de cada canica.
    for _ in range(cantidad_canicas):
        contenedor = 0

        # En cada nivel la canica puede ir a la izquierda o a la derecha.
        for _ in range(niveles):
            direccion = random.randint(0, 1)
            contenedor += direccion

        resultados.append(contenedor)

    return resultados


def graficar_histograma(resultados, niveles=12):
    """
    Grafica la cantidad de canicas que terminó en cada contenedor.

    Parámetros:
        resultados (list): Contenedor final de cada canica.
        niveles (int): Cantidad de niveles de la máquina de Galton.
    """
    # Los límites permiten centrar cada barra sobre su número de contenedor.
    limites = [numero - 0.5 for numero in range(niveles + 2)]

    plt.figure(figsize=(10, 6))
    plt.hist(resultados, bins=limites, edgecolor="black", rwidth=0.9)
    plt.title("Simulación de la Máquina de Galton")
    plt.xlabel("Contenedor final")
    plt.ylabel("Cantidad de canicas")
    plt.xticks(range(niveles + 1))
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # El proyecto requiere exactamente 3000 canicas y 12 niveles.
    resultados_simulacion = simular_maquina_galton(
        cantidad_canicas=3000,
        niveles=12
    )

    graficar_histograma(
        resultados_simulacion,
        niveles=12
    )
