def mostrar_menu():
    """
    Muestra las opciones disponibles del programa.
    """
    print("\n" + "=" * 50)
    print("CONTROL DE CALIFICACIONES")
    print("=" * 50)
    print("1. Agregar un nuevo alumno")
    print("2. Ver alumnos y calificaciones")
    print("S. Salir")


def solicitar_nombre():
    """
    Solicita el nombre de un alumno y evita nombres en blanco.

    Retorna:
        str: Nombre válido del alumno.
    """
    while True:
        nombre = input("Nombre del alumno: ").strip()

        if nombre:
            return nombre

        print("Error: el nombre no puede estar en blanco.")


def solicitar_cantidad_calificaciones():
    """
    Solicita cuántas calificaciones se agregarán y valida la entrada.

    Retorna:
        int: Cantidad válida de calificaciones.
    """
    while True:
        try:
            cantidad = int(input("¿Cuántas calificaciones deseas agregar? "))

            if cantidad <= 0:
                print("Error: debes agregar al menos una calificación.")
                continue

            return cantidad

        except ValueError:
            print("Error: escribe un número entero válido.")


def solicitar_calificaciones(cantidad):
    """
    Solicita las calificaciones del alumno y evita que una entrada incorrecta
    detenga la ejecución del programa.

    Parámetros:
        cantidad (int): Número de calificaciones que se solicitarán.

    Retorna:
        list: Calificaciones numéricas capturadas.
    """
    calificaciones = []

    for numero in range(1, cantidad + 1):
        while True:
            try:
                calificacion = float(
                    input(f"Ingresa la calificación {numero}: ")
                )
                calificaciones.append(calificacion)
                break

            except ValueError:
                print(
                    "Error: la calificación debe ser numérica. "
                    "Vuelve a intentarlo."
                )

    return calificaciones


def agregar_alumno(alumnos):
    """
    Captura la información de un alumno y la agrega a la lista.

    Parámetros:
        alumnos (list): Lista donde se almacenan los alumnos registrados.
    """
    print("\n--- Agregar alumno ---")

    nombre = solicitar_nombre()
    cantidad = solicitar_cantidad_calificaciones()
    calificaciones = solicitar_calificaciones(cantidad)

    alumnos.append(
        {
            "nombre": nombre,
            "calificaciones": calificaciones
        }
    )

    print(f"\nAlumno '{nombre}' agregado correctamente.")


def mostrar_alumnos(alumnos):
    """
    Muestra cada alumno registrado junto con sus calificaciones y promedio.

    Parámetros:
        alumnos (list): Lista de alumnos registrados.
    """
    print("\n--- Alumnos y promedios ---")

    if not alumnos:
        print("Todavía no hay alumnos registrados.")
        return

    for alumno in alumnos:
        calificaciones = alumno["calificaciones"]
        promedio = sum(calificaciones) / len(calificaciones)

        print(
            f"{alumno['nombre']}: Promedio {promedio:.2f} "
            f"| Calificaciones: {calificaciones}"
        )


def confirmar_salida():
    """
    Confirma con el usuario si realmente desea cerrar el programa.

    Retorna:
        bool: True si confirma la salida y False si desea continuar.
    """
    print("\nSe cerrará el programa.")

    while True:
        respuesta = input(
            "¿Estás seguro de que deseas salir? (S/N): "
        ).strip().upper()

        if respuesta == "S":
            return True

        if respuesta == "N":
            print("Regresando al menú principal...")
            return False

        print("Opción inválida. Escribe S para sí o N para no.")


def main():
    """
    Controla el menú principal y mantiene el programa en ejecución hasta que
    el usuario confirme que desea salir.
    """
    alumnos = []

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ").strip().upper()

        if opcion == "1":
            agregar_alumno(alumnos)

        elif opcion == "2":
            mostrar_alumnos(alumnos)

        elif opcion == "S":
            if confirmar_salida():
                print("Programa cerrado correctamente.")
                break

        else:
            print("Opción inválida. Selecciona 1, 2 o S.")


if __name__ == "__main__":
    main()
