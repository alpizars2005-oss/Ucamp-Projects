def crear_lista(nombre_lista):
    """
    Solicita al usuario la longitud y los elementos de una lista.

    Parámetros:
        nombre_lista (str): Nombre utilizado para identificar la lista.

    Retorna:
        list: Lista creada con los datos ingresados por el usuario.
    """

    # Solicitar y validar la cantidad de elementos
    while True:
        try:
            longitud = int(
                input(f"\n¿Cuántos elementos tendrá la {nombre_lista}? ")
            )

            if longitud <= 0:
                print("La cantidad debe ser mayor que cero.")
                continue

            break

        except ValueError:
            print("Entrada inválida. Escribe un número entero.")

    lista = []

    print(f"\nIngresa los elementos de la {nombre_lista}:")

    # Solicitar cada elemento de la lista
    for posicion in range(1, longitud + 1):
        while True:
            elemento = input(f"Elemento {posicion}: ").strip()

            if elemento == "":
                print("El elemento no puede estar vacío.")
            else:
                lista.append(elemento)
                break

    return lista


def eliminar_elementos_repetidos(primera_lista, segunda_lista):
    """
    Elimina de la primera lista los elementos que también
    se encuentren en la segunda lista.

    La comparación ignora mayúsculas y minúsculas.

    Parámetros:
        primera_lista (list): Lista de la que se eliminarán elementos.
        segunda_lista (list): Lista utilizada para buscar coincidencias.

    Retorna:
        tuple: Contiene la lista resultante y los elementos eliminados.
    """

    # Convertir los elementos de la segunda lista a minúsculas
    # para facilitar la comparación
    elementos_segunda = {
        elemento.casefold() for elemento in segunda_lista
    }

    lista_resultante = []
    elementos_eliminados = []

    # Revisar cada elemento de la primera lista
    for elemento in primera_lista:
        if elemento.casefold() in elementos_segunda:
            elementos_eliminados.append(elemento)
        else:
            lista_resultante.append(elemento)

    return lista_resultante, elementos_eliminados


def mostrar_lista(nombre_lista, lista):
    """
    Muestra los elementos de una lista de manera ordenada.

    Parámetros:
        nombre_lista (str): Nombre que se mostrará.
        lista (list): Lista que se desea imprimir.
    """

    print(f"\n{nombre_lista}:")

    if lista:
        for posicion, elemento in enumerate(lista, start=1):
            print(f"{posicion}. {elemento}")
    else:
        print("La lista está vacía.")


def main():
    """
    Función principal que controla la ejecución del programa.
    """

    print("=" * 50)
    print("     ELIMINACIÓN DE ELEMENTOS ENTRE DOS LISTAS")
    print("=" * 50)

    # Crear las dos listas
    lista_1 = crear_lista("primera lista")
    lista_2 = crear_lista("segunda lista")

    # Mostrar las listas originales
    print("\n" + "=" * 50)
    print("LISTAS ORIGINALES")
    print("=" * 50)

    mostrar_lista("Primera lista", lista_1)
    mostrar_lista("Segunda lista", lista_2)

    # Eliminar de la primera lista los elementos
    # que también aparecen en la segunda
    lista_resultante, elementos_eliminados = (
        eliminar_elementos_repetidos(lista_1, lista_2)
    )

    # Mostrar los resultados
    print("\n" + "=" * 50)
    print("RESULTADO")
    print("=" * 50)

    if elementos_eliminados:
        print(
            "\nSe eliminaron de la primera lista los "
            "siguientes elementos:"
        )

        for elemento in elementos_eliminados:
            print(f"- {elemento}")
    else:
        print(
            "\nNo se encontraron elementos de la segunda lista "
            "dentro de la primera."
        )

    mostrar_lista(
        "Primera lista después de eliminar las coincidencias",
        lista_resultante
    )

    print("\nPrograma finalizado correctamente.")


# Ejecutar el programa
if __name__ == "__main__":
    main()
