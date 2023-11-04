#!/usr/bin/env python
import pika
from job import Job
from random import randint

def getDatosFormulario(index):
    print(index)
    data = {1: {'cedula':'0000000001','nombre':'JOSE PEREZ','edad':50,'sexo':'M'},
    2: {'cedula':'0000000002','nombre':'LUIS SOJOS','edad':40,'sexo':'M'},
    3: {'cedula':'0000000003','nombre':'ANGEL MERA','edad':30,'sexo':'M'},
    4: {'cedula':'0000000004','nombre':'ANGELO ALEJANDRO','edad':20,'sexo':'M'},
    5: {'cedula':'0000000005','nombre':'JUAN BETANCOURT','edad':10,'sexo':'M'},
    6: {'cedula':'0000000006','nombre':'CARLOS RENGIFO','edad':55,'sexo':'M'},
    7: {'cedula':'0000000007','nombre':'STEVEN MERA','edad':34,'sexo':'M'},
    8: {'cedula':'0000000008','nombre':'LEONEL PAVAROTI','edad':43,'sexo':'M'},
    9: {'cedula':'0000000009','nombre':'EEDY PAVON','edad':19,'sexo':'M'},
    10: {'cedula':'0000000010','nombre':'ANDRES CALAMARO','edad':69,'sexo':'M'},
    11: {'cedula':'0000000011','nombre':'JOSIAS JR.','edad':38,'sexo':'M'}}

    return data[index]


# Establecer conexion
con = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
ch = con.channel()

# Declarar la cola
ch.queue_declare(queue='formularios')

# Generar un trabajo

data = getDatosFormulario(randint(1,11))

t = Job(data['cedula'],data['nombre'],data['edad'],data['sexo'])

# Publicar el mensaje
ch.basic_publish(exchange='',
                 routing_key='formularios',
                 body=t.exportar().encode('utf-8'))
print("mensaje enviado")

# Cerrar conexion
con.close()



