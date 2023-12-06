from flask import Flask, request, jsonify, make_response
import json
import netifaces as ni
import requests

CURRENT_IP = ni.ifaddresses('enp0s3')[ni.AF_INET][0]['addr']
NODES_FILE = '/home/aialejandro/modulo_almacenamiento/leaders.json'
FORMS_FILE = '/home/aialejandro/modulo_almacenamiento/forms.json'
MIN_REPLICATIONS = 1

TYPES = {
    'nodes': NODES_FILE,
    'forms': FORMS_FILE,
}

app = Flask(__name__)

def read_json_file(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)      
    except FileNotFoundError as e:
        return False
    except Exception as e: 
        print(e)
    
def write_json_file(filename, data):
    try:
        with open(filename, "w") as outfile:
            outfile.write(json.dumps(data, indent=4))
        return True
    except Exception as e:
        print("Error al grabar. {}".format(e))
        return False

def getRemoteFile(node, type):
    try:
        req = requests.get('http://{}:5000/{}'.format(node, type), timeout=2)
        data = json.dumps(req.json()['data'], indent=4)
        #Actualizar archivo
        with open(TYPES[type], "w") as outfile:
            outfile.write(data)
            print("Archivo local actualizado: {}".format(type))
        return True
    except Exception as e:
        print("Nodo no disponible: {}".format(node))
        return False

def getLocalNodesList():
    nodes_data = read_json_file(NODES_FILE)
    if nodes_data:
        nodes = []           
        for value in list(nodes_data.values()):
            nodes += value
        return nodes
    else:
        return False

def getCurrentLeaderNode():
    nodes = read_json_file(NODES_FILE)
    return nodes["L"][0]

def updateNodesFile():
    #Verificar el lider conectandose a cualquier nodo del archivo local (al primero que responda)
    nodes_list = getLocalNodesList()
    if nodes_list:
        for node in list(filter(lambda node: node != CURRENT_IP, nodes_list)):
            if getRemoteFile(node, 'nodes'):
                return True
        print("No se ha obtenido respuesta de ningún nodo.")
    else:
        print("No se ha encontrado el archivo local de nodos.")
    
    ip = input('Indique la IP del líder o de cualquier nodo:')
    #Intentar actualizarse desde el nodo ingresado
    if not ip == CURRENT_IP:
        if getRemoteFile(ip, 'nodes'):
            return True
    #Crear un nuevo archivo con este nodo como líder
    nodes_data = {"L": ["{}".format(CURRENT_IP)],'N':[]}
    if write_json_file(NODES_FILE, nodes_data):
        print("Archivo de nodos creado con este nodo como lider.")
        return True
    
    return False        

def updateFiles():
    if not updateNodesFile():
        input("No se pudo obtener o crear archivo de nodos.")
        return False
    leader = getCurrentLeaderNode()
    if leader == CURRENT_IP:
        return True
    if not getRemoteFile(leader, 'forms'):
        input("No se pudo obtener o crear archivo de formularios.")
        return False

def become_leader():
    nodes_data = read_json_file(NODES_FILE)
    nodes_data['N'].append(nodes_data['L'][0])
    nodes_data['L'] = ["{}".format(CURRENT_IP)]
    if write_json_file(NODES_FILE, nodes_data):
        print("Este nodo ahora es lider.")

def send_update_requests():
    nodes_list = getLocalNodesList()
    replications = 0
    if nodes_list:
        for node in list(filter(lambda node: node != CURRENT_IP, nodes_list)):
            try:
                req = requests.get('http://{}:5000/updatenode'.format(node), timeout=2)
                if req.status_code == 200:
                    replications += 1
            except Exception as e:
                print("Nodo no disponible: {}".format(node))
    return replications

#################
#ROUTES DE LIDER#
#################

@app.get('/report')
def report_route():
    key = request.args.get('key')
    value = request.args.get('value')
    condition = request.args.get('condition') 
    if not key or not value:
        return make_response({'code':'ERROR','message':'Faltan parametros'}, 500)

    if condition:
        int_value = int(value)
        data = list(
            filter(
                lambda form: eval(f"form['{key}'] {condition} {int_value}"),
                read_json_file(FORMS_FILE).values()
            )
        )    
    else:
        data = list(
            filter(
                lambda form: form[key] == value,
                read_json_file(FORMS_FILE).values()
            )
        )

    return make_response({'code':'SUCCESS','data':data}, 201)

@app.route('/forms', methods=['GET', 'POST'])
def forms_route():
    if request.method == 'GET':
        data = read_json_file(FORMS_FILE)
        if not data:
            return make_response({'code':'SUCCESS','data':{}}, 201)
        return make_response({'code':'SUCCESS','data':data}, 201)
    elif request.method == "POST":
        received_data = request.json
        #Primero verificar si el nodo actual es lider, sino enviar el request al lider
        leader = getCurrentLeaderNode()
        if leader == CURRENT_IP:
            forms_data = read_json_file(FORMS_FILE)
            if not forms_data:
                data_to_save = {received_data['cedula']:received_data}
            else:
                forms_data[received_data['cedula']] = received_data
                data_to_save = forms_data
            if write_json_file(FORMS_FILE, data_to_save):
                print('Formulario {} guardado.'.format(received_data['cedula']))
                #Enviar a todos los nodos a replicarse
                replications = send_update_requests()
                if replications >= MIN_REPLICATIONS:
                    return make_response({'code':'SUCCESS','message':'Formulario {} guardado.'.format(received_data['cedula'])}, 201)
                else:
                    return make_response({'code':'ERROR','message':'No hubo suficientes replicaciones'}, 500)
        else:
            try:
                req = requests.post('http://{}:5000/forms'.format(leader), json=received_data, timeout=2)
                return req.json()
            except Exception as e:
                print("Lider no disponible: {}".format(leader))
                #Convertirse en lider, grabar y decirle a todos que graben
                become_leader()
                replications = send_update_requests()
                if replications >= MIN_REPLICATIONS:
                    return make_response({'code':'SUCCESS','message':'Formulario {} guardado.'.format(received_data['cedula'])}, 201)
                else:
                    return make_response({'code':'ERROR','message':'No hubo suficientes replicaciones'}, 500)

        
@app.route('/forms/<form_id>')
def get_form_by_id(form_id):
    forms = read_json_file(FORMS_FILE)
    if forms:
        if form_id in forms.keys():
            return make_response({'code':'SUCCESS','data':forms[form_id]}, 201)    
    return make_response({'code':'ERROR','message':'No existe el formulario'}, 600)

@app.route('/count')
def get_form_count():
    forms = read_json_file(FORMS_FILE)
    if forms:
        return make_response({'code':'SUCCESS','count':len(forms)}, 201)
    return make_response({'code':'ERROR','message':'No existe el archivo de formularios'}, 500)

@app.route('/nodes', methods=['GET'])
def nodes_route():
    #Guardar el nodo que hace la solicitud si no existe
    if request.remote_addr not in getLocalNodesList():
        nodes_data = read_json_file(NODES_FILE)
        nodes_data['N'].append(request.remote_addr)
        write_ok = write_json_file(NODES_FILE, nodes_data)
        if write_ok:
            print("Nodo {} agregado al archivo de nodos.".format(request.remote_addr))
    data = read_json_file(NODES_FILE)
    if not data:
        return make_response({'code':'ERROR','message':'Error leyendo archivo de nodos'}, 500)    
    return make_response({'code':'SUCCESS','data':data}, 201)

@app.route('/nodeslist', methods=['GET'])
def nodes_list_route():
    data = read_json_file(NODES_FILE)
    if not data:
        return make_response({'code':'ERROR','message':'Error leyendo archivo de nodos'}, 500)    
    return make_response({'code':'SUCCESS','data':data}, 201)

#################
#ROUTES DE NODOS#
#################
#Actualizarse del lider
@app.route('/updatenode', methods=['GET'])
def update_from_leader_route():
    leader = getCurrentLeaderNode()
    if not getRemoteFile(leader, 'nodes'):
        return make_response({'code':'ERROR','message':'Error actualizando archivo de nodos'}, 500)
    if not getRemoteFile(leader, 'forms'):
        return make_response({'code':'ERROR','message':'Error actualizando archivo de formularios'}, 500)
    return make_response({'code':'SUCCESS','message':'Nodo actualizado'}, 201)

#########
#STARTUP#
#########

#Al iniciarse:
#1. Actualizar su archivo de lideres
#2. Si no es lider, ponerse al dia con el lider

print("IP ACTUAL: {}".format(CURRENT_IP))
updateFiles()
