from flask import Flask, request
import json
import netifaces as ni
import requests

CURRENT_IP = ni.ifaddresses('enp0s3')[ni.AF_INET][0]['addr']
LEADERS_FILE = '/home/aialejandro/modulo_almacenamiento/leaders.json'
TRANSACTIONS_FILE = ''

app = Flask(_name_)

#Al iniciarse:
#1. Actualizar su archivo de lideres
#2. Si no es lider, ponerse al dia con el lider

def read_file(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)      
    except FileNotFoundError as e:
        return False
    except Exception as e: 
        print(e)
    
def write_file(filename, data):
    try:
        with open(filename, "w") as outfile:
            outfile.write(data)
        return True
    except Exception as e:
        print("Error al grabar. {}".format(e))
        return False

def getLocalLeadersList():
    leaders_data = read_file(LEADERS_FILE)
    if leaders_data:
        nodes = []            
        for value in leaders_data.values():
            nodes += value
        return nodes
    else:
        #Si no hay archivo (es un nuevo nodo), se requiere ingresar la ip de cualquier nodo
        ip = input('No se ha encontrado el archivo de líderes. Indique la IP del líder o de cualquier nodo:')
        #Si la ip que se ingresa es la misma de este nodo, entonces es el lider y se debe crear el archivo
        if ip == CURRENT_IP:
            leaders_data = {"L":"{}".format(CURRENT_IP)}
            write_ok = write_file(LEADERS_FILE, leaders_data)
            if write_ok:
                print("Archivo de lideres actualizado")
        #Si no conectarse a la ip y obtener el archivo de lideres

def getRemoteLeadersFile(node):
    try:
        req = requests.get('http://{}:5000/leaders'.format(node))
        json_object = json.dumps(req.json(), indent=4)
        #Actualizar archivo
        with open(LEADERS_FILE, "w") as outfile:
            outfile.write(json_object)
            print("Archivo de lideres actualizado")
        return True
    except:
        print("Nodo no disponible: {}".format(node))
        return False



def updateFiles():
    #Verificar el lider conectandose a cualquier nodo del archivo local (al primero que responda)
    leaders_list = getLocalLeadersList()
    file_saved = False
    for node in filter(lambda node: node != CURRENT_IP, nodes):
        if getRemoteLeadersFile(node):
            file_saved = True
            break
    if not file_saved:  

in_memory_datastore = {
   "COBOL" : {"name": "COBOL", "publication_year": 1960, "contribution": "record data"},
   "ALGOL" : {"name": "ALGOL", "publication_year": 1958, "contribution": "scoping and nested functions"},
   "APL" : {"name": "APL", "publication_year": 1962, "contribution": "array processing"},
}

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
        #TODO: Guardar el nodo que hace la solicitud
        return leaders_data

print("IP ACTUAL: {}".format(CURRENT_IP))
updateFiles()