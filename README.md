# S_distribuidos

#Autores
- @SteckMera
- @JuanBetancourt
- @AngeloAlejandro
- @EduardoRengifo
- @AngelMera

#Instrucciones

1.- Para la ejecucion de los programas input y validator se requieren lo siguiente:
- Python3 version 3.6 o superior
- RabbitMQ - www.rabbitmq.com
- Librerias Pika para la integración de las cola de mensajes (RabbitMQ)

2.- Para el sistema de coordinador de instancias y replicación se requiere:
- Python3 versión 3.6 o superior
- virtualenv
- flask
- netifaces

#Ejecución

Para generar formularios a la cola 
- Python3 input.py

Para recuperar, validar y enviar los formularios:
- python3 validate.py http://IP:PORT
- python3 validate.py http://190.100.2.205:5000

Para generar reportes:
- python3 report.py IP:PORT FIELD VALUE CONDITION
- python3 report.py 190.100.2.205:5000 edad 30 ">="

Para iniciar el coordinador de instancias y replicación:
- source venv/bin/activate
- export FLASK_APP=api.py
- flask run --host=0.0.0.0

