#!/usr/bin/env python
import pika
from job import Job

# Establecer conexión
con = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
ch = con.channel()

# Declarar la cola
ch.queue_declare(queue='formularios')

# Definir la función callback
def process(ch, method, properties, body):
    datos = body.decode('utf-8')
    print("Se ha recibido el siguiente mensaje: %s" % datos)
    t = Job.importar(datos)

# Enganchar el callback
ch.basic_consume(queue='formularios',
                 auto_ack=True,
                 on_message_callback=process)

# Poner en espera
print('Esperando mensajes...')
ch.start_consuming()
