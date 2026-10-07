**************************************************************************
**************************** EJECUCIÓN ***********************************
**************************************************************************

En una terminal ejecutar este comando:

    uv run servidor_calculadora.py 

Una vez iniciado el servidor ejecutar el cliente monohilo:

    uv run cliente_monohilo.py

O lasimulación de tráfico declientes multihilo:

    uv run clientes_multihilo.py


**************************************************************************
************************ MANUAL DE USUARIO *******************************
**************************************************************************

Las operaciones que permite la calculadora son las siguientes:

- add, sub, mult, div, sqrt, mean, std
- off
- clear

Siguen el siguiente formato -> <operacion> <valor1> <valor2> . . . <valorN>

Se puede emplear el acumulador como valor para una operación simplemente 
escribiendo "ans" e internamente se sustutuirá por su valor numérico.

En el caso de la suma, la multiplicación, la media aritmética y la desviación estándar
se devuelve el resultado de aplicar la operación correspondiente a todo el conjunto de 
parámetros ya que no hay una cantidad fija para estos.

La resta devuelve el resultado de restarle al primer parámetro todos los demás.

Para la división se toma el primer parámetro como dividendo y el segundo como 
divisor, cualquier otro parámetro posterior a estos será ignorado para la operación.

En la raíz cuadrada solamente se emplea el primer parámetro, cualquier otro posterior 
será ignorado.

El comando off cierra la calculadora y acaba el proceso.

El comando clear reinicia el valor del acumulador a 0.

****************************EJEMPLOS DE OPERACIONES***********************
    # Operaciones normales
    > add 12 8
    > sub 50 15 5
    > mult 4 2.5
    > div 100 4
    > sqrt 144
    > mean 10 20 30 40
    > std 2 4 6 8 10

    # Operaciones empleando el acumulador
    > add ans 10
    > mult ans ans
    > div ans 2

    # Operaciones de control
    > off
    > clear


**************************************************************************
****************** DETALLES DE LA IMPLEMENTACIÓN *************************
***************************** Y ******************************************
********************** DECISIONES TOMADAS ********************************
**************************************************************************

Para el uso de la funcionalidad del acumulador se ha decidido gestionarlo de manera local
por el cliente, quien es responsable de la gestión, la cual consiste en actualizar el valor
únicamente cuando se devuelven resultados carentes de errores, de manera que el valor del
acumulador corresponde al del último resultado válido, se ha tomado esta decisión debido a que
no se ha considerado necesario incluir la logica del acumulador en las peticiones que se le mandan
al servidor y que este se limite unicamente a realizar las operaciones y devolver sus resultados.

En relación con lo anterior se ha decidido que las respuesta que da el servidor a operaciones que hayan
terminado provocando un error contengan la palabra "ERROR", con el objetivo de facilitarle al cliente la
identificación de errores relevante para la gestión del acumulador. De esta manera el servidor no guarda
ningún estado relativo a cada cliente, así que procesa cada petición de manera independiente.

Cabe recalcar que el hecho de emplear etiquetas hace que haya una sobrecarga al enviar datos que no corresponden 
al resultado, ya que es equivalente a emplear cabeceras de control. No obstante el uso de cabeceras en esta práctica 
particular no supone un problema debido a la simplicidad del problema a resolver, pero este aspecto sí se debería tener
en cuenta en casos reales donde la sobrecarga debe ser lo mínima posible en afán de mejorar el rendimiento de la 
transmisión de datos y el aprovechamiento del sistema, especialmente si se trata de uno distribuido.

En el servidor se han protegido las variables locales relativas a las estadísticas de actividad mediante Locks 
para asegurar la exclusión mutua para dichos valores, asegurando así la integridad de la información que maneja el servidor.

El servidor en la función "calcular" gestiona los errores sin interrumpir la ejecución de las peticiones de
cliente mediante el uso del prefijo "ERROR" en sus respuestas para operaciones erróneas, sin importar si el error es ocasionado
por una excepción al tratar de hacer un cálculo o si el usuario emplea una sintaxis incorrecta.

Por último se ha desarrollado una simulación de tráfico de clientes multihilo, que generan un tráfico de 
peticiones ficticias. Dicho tráfico sigue una distribución exponencial, cuya tasa puede regularse, al igual
que lacantidad de clientes y laduración de la simulación. Dicha simulación se ha implementado para estudiar la escalabilidad
del problema y su adaptación al aumento de carga de trabajo.

