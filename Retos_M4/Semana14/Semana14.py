from pathlib import Path

ARCHIVO_CONTACTOS = Path(__file__).with_name("contactos.txt")


def asegurar_archivo():
    """
    Verifica que el archivo de contactos exista.

    Si no existe, lo crea vacío para evitar que el programa se interrumpa.
    """
    if not ARCHIVO_CONTACTOS.exists():
        ARCHIVO_CONTACTOS.touch(encoding="utf-8")


def cargar_contactos():
    """
    Lee los contactos guardados en el archivo.

    Cada línea utiliza el formato:
    nombre|telefono|correo

    Retorna:
        list: Lista de diccionarios con la información de los contactos.
    """
    contactos = []

    try:
        with ARCHIVO_CONTACTOS.open("r", encoding="utf-8") as archivo:
            for numero_linea, linea in enumerate(archivo, start=1):
                linea = linea.strip()

                if not linea:
                    continue

                datos = linea.split("|")

                if len(datos) != 3:
                    print(
                        f"Aviso: la línea {numero_linea} tiene un formato inválido "
                        "y será ignorada."
                    )
                    continue

                nombre, telefono, correo = datos

                contactos.append(
                    {
                        "nombre": nombre.strip(),
                        "telefono": telefono.strip(),
                        "correo": correo.strip(),
                    }
                )

    except OSError as error:
        print(f"No fue posible leer el archivo: {error}")

    return contactos


def guardar_contactos(contactos):
    """
    Sobrescribe el archivo con la información actualizada de los contactos.

    Parámetros:
        contactos (list): Lista de contactos que se guardará.
    """
    try:
        with ARCHIVO_CONTACTOS.open("w", encoding="utf-8") as archivo:
            for contacto in contactos:
                archivo.write(
                    f"{contacto['nombre']}|"
                    f"{contacto['telefono']}|"
                    f"{contacto['correo']}\n"
                )

    except OSError as error:
        print(f"No fue posible actualizar el archivo: {error}")
        return False

    return True


def mostrar_contactos(contactos):
    """
    Muestra los contactos numerados en pantalla.

    Parámetros:
        contactos (list): Contactos que se mostrarán.
    """
    print("\n" + "=" * 60)
    print("CONTACTOS GUARDADOS")
    print("=" * 60)

    if not contactos:
        print("No hay contactos guardados.")
        return

    for numero, contacto in enumerate(contactos, start=1):
        print(
            f"{numero}. {contacto['nombre']} | "
            f"Tel: {contacto['telefono']} | "
            f"Correo: {contacto['correo']}"
        )


def seleccionar_contacto(contactos):
    """
    Solicita al usuario el número del contacto que desea modificar.

    Retorna:
        int: Índice del contacto seleccionado.
    """
    while True:
        try:
            opcion = int(
                input("\nEscribe el número del contacto que deseas modificar: ")
            )

            if 1 <= opcion <= len(contactos):
                return opcion - 1

            print("Opción fuera de rango. Intenta nuevamente.")

        except ValueError:
            print("Entrada inválida. Debes escribir un número.")


def solicitar_dato(mensaje):
    """
    Solicita un dato no vacío.

    Retorna:
        str: Texto válido ingresado por el usuario.
    """
    while True:
        dato = input(mensaje).strip()

        if dato:
            return dato

        print("El dato no puede quedar en blanco.")


def modificar_contacto(contacto):
    """
    Permite modificar el nombre, teléfono o correo de un contacto.

    Parámetros:
        contacto (dict): Contacto seleccionado.
    """
    while True:
        print("\n¿Qué dato deseas modificar?")
        print("1. Nombre")
        print("2. Teléfono")
        print("3. Correo")
        print("4. Modificar los tres datos")
        print("S. Guardar cambios y volver")

        opcion = input("Selecciona una opción: ").strip().upper()

        if opcion == "1":
            contacto["nombre"] = solicitar_dato("Nuevo nombre: ")
            print("Nombre actualizado.")

        elif opcion == "2":
            contacto["telefono"] = solicitar_dato("Nuevo teléfono: ")
            print("Teléfono actualizado.")

        elif opcion == "3":
            contacto["correo"] = solicitar_dato("Nuevo correo: ")
            print("Correo actualizado.")

        elif opcion == "4":
            contacto["nombre"] = solicitar_dato("Nuevo nombre: ")
            contacto["telefono"] = solicitar_dato("Nuevo teléfono: ")
            contacto["correo"] = solicitar_dato("Nuevo correo: ")
            print("Información actualizada.")

        elif opcion == "S":
            break

        else:
            print("Opción inválida. Intenta nuevamente.")


def ejecutar_programa():
    """
    Controla la ejecución del reto de la semana 14.
    """
    asegurar_archivo()
    contactos = cargar_contactos()

    if not contactos:
        mostrar_contactos(contactos)
        print(
            "\nAgrega contactos al archivo 'contactos.txt' "
            "antes de ejecutar nuevamente el programa."
        )
        return

    while True:
        mostrar_contactos(contactos)
        indice = seleccionar_contacto(contactos)

        contacto = contactos[indice]

        print(f"\nContacto seleccionado: {contacto['nombre']}")
        modificar_contacto(contacto)

        if guardar_contactos(contactos):
            print("\nLos cambios se guardaron correctamente en contactos.txt.")

        while True:
            continuar = input(
                "¿Deseas modificar otro contacto? (S/N): "
            ).strip().upper()

            if continuar == "S":
                break

            if continuar == "N":
                print("Programa finalizado.")
                return

            print("Opción inválida. Escribe S o N.")


if __name__ == "__main__":
    ejecutar_programa()
