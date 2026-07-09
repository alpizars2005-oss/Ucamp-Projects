def mostrar_letras_vecinas(letra):
    abecedario_minusculas = "abcdefghijklmnopqrstuvwxyz"
    abecedario_mayusculas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if letra in abecedario_minusculas:
        abecedario = abecedario_minusculas
    elif letra in abecedario_mayusculas:
        abecedario = abecedario_mayusculas
    else:
        print("Error: Debes ingresar una letra válida del alfabeto.")
        return

    posicion = abecedario.index(letra)

    letra_anterior = abecedario[posicion - 1]
    letra_siguiente = abecedario[(posicion + 1) % len(abecedario)]

    print(f"Letra anterior: {letra_anterior}")
    print(f"Letra siguiente: {letra_siguiente}")


while True:
    entrada = input("Ingresa una letra o escribe 'Salir' para salir: ")

    if entrada == "Salir":
        print("Programa finalizado.")
        break

    if len(entrada) != 1:
        print("Debes ingresar solamente una letra.")
    else:
        mostrar_letras_vecinas(entrada)