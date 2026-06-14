# Codigo similar a la semana 6 pero con validaciones para las calificaciones y el nombre del alumno, ademas de un contador para limitar a 3 calificaciones por alumno

alumnos = []

respuesta = "s"

while respuesta.lower() == "s":
    nombre = input("Ingrese el nombre del alumno: ")

    while nombre == "":
        print("Debe ingresar un nombre")
        nombre = input("Ingrese el nombre del alumno: ")

    calificaciones = []
    contador = 0

    while contador < 3:
        while True:
            try:
                calificacion = float(input("Ingrese una calificación: "))

                if calificacion < 0 or calificacion > 10:
                    print("La calificación debe estar entre 0 y 10")
                else:
                    calificaciones.append(calificacion)
                    contador += 1
                    break

            except ValueError:
                print("Debe ingresar un número válido")

        if contador < 3:
            agregar = input("¿Desea ingresar otra calificación? s/n: ")

            if agregar.lower() != "s":
                break

    promedio = sum(calificaciones) / len(calificaciones)

    alumnos.append([nombre, promedio])

    respuesta = input("¿Desea registrar otro alumno? s/n: ")

print("\nResultados:")

for alumno in alumnos:
    print("Alumno:", alumno[0], "- Promedio:", round(alumno[1], 2))

print("Fin del programa")