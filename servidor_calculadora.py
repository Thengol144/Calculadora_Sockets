import socketserver
import threading
import math
import statistics
import time

# Valor del comandode apagado
APAGADO = "off"

# Lock paraproteger las variables de estadísticas
lock = threading.Lock()
# Variables de estadísticas
activos, atendidas, errores, bytes_transmitidos, tiempo_resp = 0, 0, 0, 0, 0.0

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

class CalculadoraHandler(socketserver.StreamRequestHandler):

    def handle(self):

        # Declaramos las variables para las estadístcas como globales (para soportar varios clientes a la vez)
        global activos, atendidas, errores, bytes_transmitidos, tiempo_resp

        # Protegemos la cantidad de clientes activos
        with lock:
            # Contabilizamos un nuevo cliente activo
            activos += 1

        try:

            while True:
                # Leemos el comando introducido
                cmd = self.rfile.readline()

                # Guardamos el instante de inicio de la operacion
                inicio = time.time()

                # Finalizamos el blucle en caso de introducirse un comando vacío
                if not cmd:
                    break

                # Decodificamos el comando para optener la operación y los argumentos en caso de haberlos
                operacion = cmd.decode('utf-8').strip()

                # Finalizamos el blucle en caso de introducirse elcomando de apagado
                if operacion == APAGADO:
                    break

                # calculamos el resultado de la operación
                resultado, es_error = self.calcular(operacion)
                respuesta = resultado
                # Codificamos y enviamos la respuesta al cliente
                self.wfile.write(respuesta.encode('utf-8'))

                # Calculamos la duración como ladiferencia entre el instante actual y el de inicio
                duracion = time.time() - inicio

                # Protegemos las variables para las estadísticas
                with lock:

                    # Contbilizamos la operación atendida
                    atendidas += 1
                    # Sumamos la cantidad de bytes transmitidos, tanto en la petición como en la respuesta
                    bytes_transmitidos += len(operacion) + len(respuesta)
                    # Sumamos la duración al tiempo de respuesta total de todas laspeticiones
                    tiempo_resp += duracion

                    # Contabilizamos el error en caso de haberse producido
                    if es_error:
                        errores += 1

                    # Mostramos todas las estadísticas actualizadas
                    print(f"MÉTRICAS -> Clientes activos: {activos} / Atendidas: {atendidas} / "
                          f"Errores: {errores} / Datos: {bytes_transmitidos}B / T.Medio: {(tiempo_resp/atendidas)*1000:.2f}ms")

        finally:
            # Restamos el cliente que finaliza sus peticiones
            with lock:
                activos -= 1


    def calcular(self, operacion):

        try:

            # Separamos la operación en tokens
            operacion = operacion.split()
            # Obtenemos la operación y el conjunto de argumentos
            op, nums = operacion[0].lower(), [float(x) for x in operacion[1:]]

            # Ejecutamos la operación correspondiente
            match op:
                case "add":
                    resultado = math.fsum(nums) # SUMA
                case "sub":
                    resultado = nums[0] - math.fsum(nums[1:]) # RESTA
                case "mult":
                    resultado = math.prod(nums) # MULTIPLICACIÓN
                case "div":
                    resultado = nums[0] / nums[1]  # DIVISIÓN
                case "sqrt":
                    resultado = math.sqrt(nums[0]) # RAÍZ CUADRADA
                case "mean":
                    resultado = statistics.mean(nums) # MEDIA ARITMÉTICA
                case "std":
                    resultado = statistics.stdev(nums) # DESCIACIÓN ESTÁNDAR
                case _:
                    raise ValueError("Operación no válida")  # OPERACIÓN NO VÁLIDA

            # Devolvemos el resultado o error
            return f"RESULTADO: {str(resultado)}", False
        except Exception as e:
            return f"ERROR: {str(e)}", True


# Declaramos el servidor
server = ThreadedTCPServer(('localhost', 5088), CalculadoraHandler)
# Mostramos un mensaje de incio
print("Servidor de calculadora iniciado y esperando operaciones...")

try:
    # Iniciamos el servidor
    server.serve_forever()
except KeyboardInterrupt:
    pass
# Cerramos elservidor
server.server_close()               
                
