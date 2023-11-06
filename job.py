import json

class Job:
    def __init__(self, cedula, nombre, edad, sexo):
        self.cedula = cedula
        self.nombre = nombre
        self.edad = edad
        self.sexo = sexo


    def exportar(self):
        return json.dumps(self.__dict__)

    @classmethod
    def importar(cls, datos):
        try:
            dic = json.loads(datos)
            return cls(dic['cedula1'], dic['nombre'],dic['edad'],dic['sexo'])
        except:
            print("Formato incorrecto")

