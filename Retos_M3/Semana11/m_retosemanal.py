def solicitar_entero(mensaje, minimo=1):
    """
    Solicita al usuario un número entero igual o mayor al mínimo indicado.

    Parámetros:
        mensaje (str): Mensaje que se mostrará al usuario.
        minimo (int): Valor mínimo permitido.

    Retorna:
        int: Número entero válido.
    """
    while True:
        try:
            numero = int(input(mensaje))

            if numero < minimo:
                print(f"El número debe ser mayor o igual que {minimo}.")
                continue

            return numero

        except ValueError:
            print("Entrada inválida. Escribe un número entero.")


def crear_lista(numero_lista):
    """
    Crea una lista con la longitud y los elementos indicados por el usuario.

    Parámetros:
        numero_lista (int): Número utilizado para identificar la lista.

    Retorna:
        list: Lista creada por el usuario.
    """
    longitud = solicitar_entero(
        f"\n¿Cuántos elementos tendrá la lista {numero_lista}? "
    )

    nueva_lista = []

    print(f"Ingresa los elementos de la lista {numero_lista}:")

    for posicion in range(1, longitud + 1):
        while True:
            elemento = input(f"Elemento {posicion}: ").strip()

            if elemento == "":
                print("El elemento no puede estar vacío.")
            else:
                nueva_lista.append(elemento)
                break

    return nueva_lista


def crear_varias_listas():
    """
    Solicita la cantidad de listas y permite crear cada una.

    Retorna:
        list: Lista que contiene todas las listas creadas.
    """
    cantidad_listas = solicitar_entero(
        "¿Cuántas listas deseas crear? "
    )

    listas = []

    for numero_lista in range(1, cantidad_listas + 1):
        listas.append(crear_lista(numero_lista))

    return listas


def mostrar_listas(listas, titulo):
    """
    Muestra todas las listas junto con un título descriptivo.

    Parámetros:
        listas (list): Lista que contiene las listas que se mostrarán.
        titulo (str): Texto que identifica el tipo de listas mostradas.
    """
    print("\n" + "=" * 60)
    print(titulo)
    print("=" * 60)

    for numero_lista, lista in enumerate(listas, start=1):
        print(f"Lista {numero_lista}: {lista}")


def eliminar_elementos_en_listas_posteriores(listas):
    """
    Elimina de cada lista los elementos que aparecen en alguna lista posterior.

    La comparación ignora mayúsculas y minúsculas. La última lista no se
    modifica porque no existen listas después de ella.

    Parámetros:
        listas (list): Lista que contiene las listas originales.

    Retorna:
        list: Nuevas listas después de eliminar las coincidencias.
    """
    listas_modificadas = []

    for indice, lista_actual in enumerate(listas):
        elementos_posteriores = set()

        for lista_posterior in listas[indice + 1:]:
            for elemento in lista_posterior:
                elementos_posteriores.add(elemento.casefold())

        lista_filtrada = []

        for elemento in lista_actual:
            if elemento.casefold() not in elementos_posteriores:
                lista_filtrada.append(elemento)

        listas_modificadas.append(lista_filtrada)

    return listas_modificadas


def ejecutar_programa():
    """
    Controla la ejecución completa del reto semanal.
    """
    print("=" * 60)
    print("ELIMINACIÓN DE ELEMENTOS EN LISTAS POSTERIORES")
    print("=" * 60)

    listas_originales = crear_varias_listas()

    mostrar_listas(
        listas_originales,
        "LISTAS ORIGINALES"
    )

    listas_modificadas = eliminar_elementos_en_listas_posteriores(
        listas_originales
    )

    mostrar_listas(
        listas_modificadas,
        (
            "LISTAS MODIFICADAS: SE ELIMINARON LOS ELEMENTOS "
            "QUE TAMBIÉN ESTABAN EN LISTAS POSTERIORES"
        )
    )
