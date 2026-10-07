import socket

# Host y número de puerto
host, port = "localhost", 5088
# Etiqueta para el uso del acumulador
answer_command = "ans"
# Valor del acumulador
answer_value = "0"
# Comando para reiniciar acumulador
clear_command = "clear"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

    # El cliente seconecta al servidor
    sock.connect((host, port))

    # Instrucciones de uso para el usuario
    print("Conectado a la calculadora \n")
    print("OPERACIONES:\n\n"
    "\t- add, sub, mult, div, sqrt, mean, std (formato -> <operacion> <valor1> <valor2> . . . <valorN>)\n"
    "\t- off para salir\n"
    "\t- clear para borrar el acumulador\n\n"
    "*Emplea 'ans' como valor del acumulador (ej: mult 5 ans)\n")

    # Blucke de ejecución
    while True:

        # Leemos el comando introducido por el usuario
        cmd = input("Calculadora > ")

        # Reiniciamos el acumulador en caso de tratarse del comando correspondiente
        if cmd.strip().lower() == clear_command:
            answer_value = "0"
            continue

        # Enviamos comando de salida al servidor y finalizamos el bucle en caso de haberse empleado dicho comando
        if not cmd or cmd.strip().lower() == "off":
            sock.sendall("off\n".encode('utf-8'))
            break

        # Sustituimos la etiqueta del acumulador por su valor en caso de haberse usado
        if answer_command in cmd:
            cmd = cmd.replace(answer_command, answer_value)            

        # Codificamos y enviamos la petición al servidor
        sock.sendall((cmd + "\n").encode('utf-8'))
        # Obtenemos la respuesta delservidor
        respuesta = str(sock.recv(1024), 'utf-8')

        # Actualizar el acumulador en caso de que no haya ocurrido un error
        if "ERROR" not in respuesta:
            answer_value = respuesta.split()[-1]

        # Imprimimos la respuesta obtenida
        print(respuesta.strip())

    # Mensaje de cierre
    print("Saliendo de la calculadora...")