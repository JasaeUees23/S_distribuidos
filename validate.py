#!/usr/bin/env python
import pika
import requests
import sys
import json
from job import Job
from proceso import ejecutar


def getLocalNodesList(nodes_data):
    #nodes_data = read_json_file(NODES_FILE)
    if nodes_data:
        nodes = []
        for value in list(nodes_data.values()):
            nodes += value
        return nodes
    else:
        return False

def validateCedula(cedula):
    validate = False
    if cedula.isdigit() and len(cedula) == 10:
        validate = True

    return validate


def send_form(list_nodes, form):
    #print(type(form))
    cedula = form["cedula"]

    if not validateCedula(cedula):
        with open("error.json", "a") as outfile:
            json.dump(form, outfile)
            return False

    for ip in list_nodes:
        list_nodes = False
        api_url = "http://" + ip + ":5000/forms/" + cedula
        try:
            response = requests.get(api_url)
            if response.status_code == 600: #Codigo que indica que el formulario no existe en el alamcen, y por lo tanto debe crearlo
                api_url = "http://" + ip + ":5000/forms"
                #api_url = "http://190.100.2.206:5000/forms"
                response = requests.post(api_url, json=form)
                print(response.json())
                list_nodes = getListNodes("http://" + ip + ":5000")
                break
            else:
                with open("data.json", "a") as outfile:
                    json.dump(form, outfile)
                print("Formulario duplicado - Cedula: " + cedula)
                break
        except:
            continue

    if list_nodes:
        print(list_nodes)

    return list_nodes


def getListNodes(ip):
    api_url = ip + "/nodeslist"
    response = requests.get(api_url)
    nodes_data = response.json()
    list_nodes = False

    if response.status_code == 201:
        list_nodes = getLocalNodesList(nodes_data["data"])

    return list_nodes

ip = sys.argv[1]
print(ip)
list_nodes = getListNodes(ip)

# Establecer conexión
con = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
ch = con.channel()

# Declarar la cola
ch.queue_declare(queue='formularios')

# Definir la función callback
def process(ch, method, properties, body):
    datos = body.decode('utf-8')
    #print("Se ha recibido el siguiente mensaje: %s" % datos)
    t = Job.importar(datos)
    #print(datos)
    #ejecutar(t)
    send_form(list_nodes, json.loads(datos))




# Enganchar el callback
ch.basic_consume(queue='formularios',
                 auto_ack=True,
                 on_message_callback=process)

# Poner en espera
print('Esperando mensajes...')
ch.start_consuming()

