#Proyecto de semana 8, de mi bootcamp. Diccionario basico de los colores del arcoíris en español, inglés y francés. 
ingles = {
    "rojo": "red",
    "naranja": "orange",
    "amarillo": "yellow",
    "verde": "green",
    "azul": "blue",
    "violeta": "violet"
}

frances = {
    "rojo": "rouge",
    "naranja": "orange",
    "amarillo": "jaune",
    "verde": "vert",
    "azul": "bleu",
    "violeta": "violet"
}

print("Idiomas disponibles:")
print("1. Inglés")
print("2. Francés")

opcion = input("Seleccione un idioma (1 o 2): ")

oracion = input("Ingrese una oración en español: ").lower()

if opcion == "1":
    diccionario = ingles
    idioma = "inglés"
elif opcion == "2":
    diccionario = frances
    idioma = "francés"
else:
    print("Opción no válida")
    exit()

encontrado = False

for color in diccionario:
    if color in oracion:
        print(f'El color "{color}" se dice "{diccionario[color]}" en {idioma}.')
        encontrado = True

if not encontrado:
    print("No se encontró ningún color del arcoíris en la oración.")