#!/usr/bin/env python
import requests
import sys
import json



def getDataReport(ip, field, value, condition):
    api_url = "http://" + ip + "/report?key=" + field + "&value=" + value + "&condition=" + condition
    #print(api_url)
    response = requests.get(api_url)
    rs = response.json()
    data = False

    if response.status_code == 201:
        data = rs["data"]

    return data


ip = sys.argv[1]
field = sys.argv[2]
value = sys.argv[3]

condition = ""

if len(sys.argv) == 5:
    condition = sys.argv[4]

#print(condition)

data = getDataReport(ip, field, value, condition)

if data:
    for row in data:
        print(row["cedula"] + "\t" + row["nombre"] + " " + row["apellido"] + "\t" + str(row["edad"]) + "\t" + row["sexo"] + "\t" + row["ciudad"] + "\t" + row["celular"] + "\t" + row["email"] + "\t" + row["estado_civil"])


    total = len(data)
    if field == "sexo":
        print(f"Cantidad de personas de sexo ({value}) es: {total}")

    if field == "edad":
        print(f"Cantidad de personas {condition} a ({value}) aÃ±os es: {total}")

    if field == "ciudad":
        print(f"Cantidad de personas que residen en la ciudad de ({value}) es: {total}")

    if field == "estado_civil":
        print(f"Cantidad de personas con estado civil ({value}) es: {total}")


else:
    print("Error al realizar la consulta")
