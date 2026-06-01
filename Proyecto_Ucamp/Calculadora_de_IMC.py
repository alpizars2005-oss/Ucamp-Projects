print("CALCULADORA DE IMC")
print("-------------------")
nombre = input("Por favor, ingresa tu nombre(s): ")

while nombre == "":
    print("Error, el nombre no puede estar vacío")
    nombre = input("Ingresa tu nombre: ")

apellido_paterno = input("Ingresa tu apellido paterno: ")
apellido_materno = input("Ingresa tu apellido materno: ")

edad = input("Ingresa tu edad: ")

while edad.isdigit() == False:
    print("Error, debes ingresar solo números")
    edad = input("Ingresa tu edad: ")

while True:
    try:
        peso = float(input("Ingresa tu peso en kg: "))
        break
    except:
        print("Error, debes ingresar un número válido")

while True:
    try:
        estatura = float(input("Ingresa tu estatura en metros: "))
        break
    except:
        print("Error, debes ingresar un número válido")

imc = peso / (estatura ** 2)
if imc < 18.5:
    clasificacion = "Bajo peso"

elif imc < 25:
    clasificacion = "Peso normal"

elif imc < 30:
    clasificacion = "Sobrepeso"

else:
    clasificacion = "Obesidad"

print("\n--- DATOS DEL USUARIO ---")
print("Nombre completo:", nombre, apellido_paterno, apellido_materno)
print("Edad:", edad)
print("Peso:", peso, "kg")
print("Estatura:", estatura, "m")
print("Tu IMC es:", round(imc, 2))
print("Clasificación:", clasificacion)
print("\nGracias por usar la calculadora de IMC")


