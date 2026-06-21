# Proyecto Módulo 2 - Fundamentos de Python
# Autor: Angel Alfredo Alpizar Sanchez
# Descripción:
# Este programa contiene la solución de dos retos:
# 1. Validar la longitud de una palabra.
# 2. Identificar el cuadrante de un punto en el plano cartesiano.

# ---------------------------------------------------------
# RETO 1: LONGITUD DE UNA PALABRA
# ---------------------------------------------------------

print("=========================================")
print("PROYECTO MÓDULO 2 - Fundamentos de Python")
print("=========================================")

print("\nRETO 1: Longitud de una palabra")

# Se solicita al usuario ingresar una palabra.
# strip() elimina espacios al inicio y al final para evitar errores de conteo.
palabra = input("Ingresa una palabra: ").strip()

# len() permite obtener la cantidad de caracteres de la palabra.
longitud = len(palabra)

# Se valida si la palabra tiene entre 4 y 8 letras.
if longitud >= 4 and longitud <= 8:
    print("La palabra es correcta.")
elif longitud < 4:
    print(f"Hacen falta letras. Solo tiene {longitud} letras.")
else:
    print(f"Sobran letras. Tiene {longitud} letras.")


# ---------------------------------------------------------
# RETO 2: ENCUENTRA EL CUADRANTE
# ---------------------------------------------------------

print("\nRETO 2: Encuentra el cuadrante")

# Se usa un ciclo while para repetir la solicitud de coordenadas
# en caso de que el usuario ingrese un valor no válido.
while True:
    try:
        # Se solicitan las coordenadas X y Y.
        # int() convierte el dato ingresado de texto a número entero.
        x = int(input("Ingrese X: "))
        y = int(input("Ingrese Y: "))

        # El proyecto indica que ninguna coordenada debe ser 0.
        if x == 0 or y == 0:
            print("Error: ninguna coordenada puede ser 0. Intenta nuevamente.\n")
        else:
            # Si las coordenadas son válidas, se termina el ciclo.
            break

    except ValueError:
        # Este mensaje aparece si el usuario escribe texto en lugar de números.
        print("Error: debes ingresar únicamente números enteros. Intenta nuevamente.\n")


# Se identifica el cuadrante de acuerdo con los signos de X y Y.
if x > 0 and y > 0:
    print("El punto se encuentra en el cuadrante I.")
elif x < 0 and y > 0:
    print("El punto se encuentra en el cuadrante II.")
elif x < 0 and y < 0:
    print("El punto se encuentra en el cuadrante III.")
elif x > 0 and y < 0:
    print("El punto se encuentra en el cuadrante IV.")