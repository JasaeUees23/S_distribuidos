from flask import Flask, request
import json
import netifaces as ni
import requests

CURRENT_IP = ni.ifaddresses('enp0s3')[ni.AF_INET][0]['addr']
LEADERS_FILE = '/home/aialejandro/modulo_almacenamiento/leaders.json'
TRANSACTIONS_FILE = ''

app = Flask(_name_)

# Al iniciarse:
# 1. Actualizar su archivo de lideres
# 2. Si no es lider, ponerse al dia con el lider, s dcir comunicación de los nodos con el líder

def updateLeadersFile():
    try:
        with open(LEADERS_FILE, 'r') as leaders_file:
            #Verificar el lider conectandose a cualquier nodo (al primero que responda)
            leaders_data = json.load(leaders_file)
            nodes = []            
            for value in leaders_data.values():
                nodes += value
            nodes_json = None
            for node in filter(lambda node: node != CURRENT_IP, nodes):
                try:
                    x = requests.get('http://{}:5000/leaders'.format(node))
                    data = x.json()
                    json_object = json.dumps(data, indent=4)
                    #Actualizar archivo
                    with open(LEADERS_FILE, "w") as outfile:
                        outfile.write(json_object)
                        print("Archivo de lideres actualizado")
                    break
                except Exception as e:
                    print("Nodo no disponible: {}".format(node))
                    print(e)
                    continue

            
            #Verificar si el lider segun el archivo en realidad es el lider
    except FileNotFoundError as e:
        # Si no hay archivo (es un nuevo nodo), se requiere ingresar la ip de cualquier nodo
        ip = input('No se ha encontrado el archivo de líderes. Indique la IP del líder o de cualquier nodo:')
        # Si la ip que se ingresa es la misma de este nodo, entonces es el lider

        # Si no conectarse a la ip y obtener el archivo de lideres
    except Exception as e: 
        print(e)

@app.get('/forms')
def list_forms():
    before_year = request.args.get('before_year') or '30000'
    after_year = request.args.get('after_year') or '0'
    qualifying_data = list(
        filter(
            lambda pl: int(before_year) > pl['publication_year'] > int(after_year),
            in_memory_datastore.values()
        )
    )

    return {"programming_languages": qualifying_data}

@app.route('/forms', methods=['GET', 'POST'])
def forms_route():
    if request.method == 'GET':
        return list_forms()
    elif request.method == "POST":
        #Primero verificar si el nodo actual es lider
        return create_programming_language(request.get_json(force=True))

@app.route('/forms/<form_id>')
def get_form_by_id(form_id):
    return in_memory_datastore[form_id]

@app.route('/leaders', methods=['GET'])
def leaders_route():
    with open(LEADERS_FILE, 'r') as leaders_file:
        leaders_data = json.load(leaders_file)
        return leaders_data

print("IP ACTUAL: {}".format(CURRENT_IP))
updateLeadersFile()