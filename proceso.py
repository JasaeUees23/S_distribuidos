#!/usr/bin/env python
import time

def ejecutar(job):
    if job.operacion =='esperar':
        print('Esperando...')
        time.sleep(2)
        print('DONE!!!')
    else:
        raise NotImplementedError('Operación "%s" no soportada.' % job.operacion)
