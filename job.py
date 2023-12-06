import json

class Job:
    def __init__(self, id, cedula, nombre, apellido, edad, sexo, telefono, celular, email, direccion, tipo_sangre, nacionalidad, ciudad, estado_civil, fecha_nacimiento, sueldo, cargas_familiares, profesion, lugar_trabajo, telefono_trabajo):
        self.id = id
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.sexo = sexo
        self.telefono = telefono
        self.celular = celular
        self.email = email
        self.direccion = direccion
        self.tipo_sangre = tipo_sangre
        self.nacionalidad = nacionalidad
        self.ciudad = ciudad
        self.estado_civil = estado_civil
        self.fecha_nacimiento = fecha_nacimiento
        self.sueldo = sueldo
        self.cargas_familiares = cargas_familiares
        self.profesion = profesion
        self.lugar_trabajo = lugar_trabajo
        self.telefono_trabajo = telefono_trabajo


    def exportar(self):
        return json.dumps(self.__dict__)

    @classmethod
    def importar(cls, datos):
        try:
            dic = json.loads(datos)
            return cls(dic['id'],dic['cedula'],dic['nombre'],dic['apellido'],dic['edad'],dic['sexo'],dic['telefono'],dic['celular'],dic['email'],dic['direccion'],dic['tipo_sangre'],dic['nacionalidad'],dic['ciudad'],dic['estado_civil'],dic['fecha_nacimiento'],dic['sueldo'],dic['cargas_familiares'],dic['profesion'],dic['lugar_trabajo'],dic['telefono_trabajo'])
        except:
            print("Formato incorrecto")

