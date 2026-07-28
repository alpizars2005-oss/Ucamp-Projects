import matplotlib.pyplot as plt


def solicitar_anio(mensaje):
    """
    Solicita un año válido al usuario.

    Parámetros:
        mensaje (str): Texto que se mostrará al solicitar el año.

    Retorna:
        int: Año ingresado por el usuario.
    """
    while True:
        try:
            anio = int(input(mensaje))

            if anio <= 0:
                print("El año debe ser mayor que cero.")
                continue

            return anio

        except ValueError:
            print("Entrada inválida. Escribe un año usando números enteros.")


def solicitar_venta(anio):
    """
    Solicita y valida la cantidad de ventas correspondiente a un año.

    Parámetros:
        anio (int): Año del que se solicitarán las ventas.

    Retorna:
        float: Cantidad de ventas registrada.
    """
    while True:
        try:
            ventas = float(input(f"Ingresa las ventas del año {anio}: $"))

            if ventas < 0:
                print("Las ventas no pueden ser negativas.")
                continue

            return ventas

        except ValueError:
            print("Entrada inválida. Escribe una cantidad numérica.")


def capturar_ventas():
    """
    Solicita el rango de años y las ventas de cada año.

    Retorna:
        tuple: Lista de años y lista de ventas capturadas.
    """
    print("=" * 55)
    print("REGISTRO DE VENTAS POR AÑO")
    print("=" * 55)

    anio_inicial = solicitar_anio("Ingresa el año inicial: ")

    while True:
        anio_final = solicitar_anio("Ingresa el año final: ")

        if anio_final < anio_inicial:
            print("El año final no puede ser menor que el año inicial.")
        else:
            break

    anios = list(range(anio_inicial, anio_final + 1))
    ventas = []

    print("\nCaptura las ventas de cada año:")

    for anio in anios:
        ventas.append(solicitar_venta(anio))

    return anios, ventas


def graficar_ventas(anios, ventas):
    """
    Genera una gráfica de líneas con las ventas registradas.

    Parámetros:
        anios (list): Años incluidos en el rango.
        ventas (list): Ventas correspondientes a cada año.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(anios, ventas, marker="o")
    plt.title(f"Ventas del {anios[0]} al {anios[-1]}")
    plt.xlabel("Año")
    plt.ylabel("Ventas")
    plt.xticks(anios)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    lista_anios, lista_ventas = capturar_ventas()
    graficar_ventas(lista_anios, lista_ventas)
