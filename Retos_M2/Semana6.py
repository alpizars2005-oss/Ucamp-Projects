errores = 0

password = input("Ingrese una contraseña: ")

while password == "" or not password[0].isdigit():
    print("La contraseña debe comenzar con un número")
    errores += 1

    if errores == 3:
        print("Fin del programa")
        exit()

    password = input("Ingrese una contraseña: ")

confirmacion = input("Ingrese la contraseña nuevamente: ")

while confirmacion != password:
    print("Las contraseñas no coinciden")
    errores += 1

    if errores == 3:
        print("Fin del programa")
        exit()

    confirmacion = input("Ingrese la contraseña nuevamente: ")

print("Contraseña correcta")
print("Fin del programa")