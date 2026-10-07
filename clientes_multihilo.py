import socket
import threading
import time
import random

# Host y número de puerto
host, port = "localhost", 5088
# Cantidad de cliente para la simulación
NUM_CLIENTES = 50
# Tasa para la distribución del táfico
LAMBDA = 2.0
# Duración en segundos de la simulación
DURACION = 10
# Etiqueta para el uso del acumulador
answer_command = "ans"

# Operaciones de muestra
OPERACIONES = [

    # Operaciones normales
    "add 12 8",
    "sub 50 15 5",
    "mult 4 2.5",
    "div 100 4",
    "sqrt 144",
    "mean 10 20 30 40",
    "std 2 4 6 8 10",

    # Operaciones empleando el acumulador
    "add ans 10",
    "mult ans ans",
    "div ans 2",

    # Operaciones erróneas
    "div 10 0",
    "sqrt -9"
]

def cliente_multihilo(id_cliente):

    # Marcamos el instante de finalización de la simulación del cliente
    fin = time.time() + DURACION
    # Valor del acumulador de cada cliente
    answer_value = "0"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

        # El cliente seconecta al servidor
        sock.connect((host, port))

        # Mientras no hayamos llegado al instante final mandamos peticiones
        while time.time() < fin:

            # Generamos un comando aleatorio
            cmd = random.choice(OPERACIONES)

            # Sustituimos la etiqueta del acumulador por su valor en caso de haberse usado 
            if answer_command in cmd:
                cmd = cmd.replace(answer_command, answer_value)

            # Codificamos y enviamos el comando
            sock.sendall((cmd + "\n").encode('utf-8'))
            # Obtenemos la respuesta del servidor
            respuesta = str(sock.recv(1024), 'utf-8')

            # En caso de no haberse producido ningún error actualizamos el valor del acumulador
            if "ERROR" not in respuesta:
                answer_value = respuesta.split()[-1]

            # Imprimimos la operación enviada por el cliente y la respuesta recibida
            print(f"Cliente {id_cliente} -> Enviado: {cmd} / Recibido: {respuesta}")

            # El cliente espera un tiempo hasta intentar hacer la siguiente petición, calculado de 
            # manera aleatoria siguiendo una distribución exponencial
            time.sleep(random.expovariate(LAMBDA))

        # Al acabarse el tiempo el cliente manda el comando de cierre para finalizar la conexión
        sock.sendall("off\n".encode('utf-8'))

# Declaramos los hilos de clientes
clientes = [threading.Thread(target=cliente_multihilo, args=(i,)) for i in range(NUM_CLIENTES)]

# Iniciamos todos los clientes
for cliente in clientes:
    cliente.start()

# Esperamos aque acaben todos los clientes
for cliente in clientes:
    cliente.join()

# Mensaje de cierre
print("Las peticiones para realizar operaciones han finalizado.")