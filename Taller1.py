from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

tipo_medicion = {'sensor':'HC-SR04', 'variable':'Distancia', 'unidades': 'Centimetros'}

mediciones = [
    {'fecha': '2019-09-23 10:02:41', **tipo_medicion, 'valor': 110},
    {'fecha': '2019-09-23 11:10:15', **tipo_medicion, 'valor': 120},
    {'fecha': '2019-09-23 05:55:45', **tipo_medicion, 'valor': 138},
    {'fecha': '2019-09-24 09:22:15', **tipo_medicion, 'valor': 124},
    {'fecha': '2019-09-23 00:15:10', **tipo_medicion, 'valor': 135},
    {'fecha': '2019-10-04 12:30:36', **tipo_medicion, 'valor': 115},
    {'fecha': '2019-10-04 15:27:25', **tipo_medicion, 'valor': 140}
]

@app.route('/mediciones', methods=['POST'])
def postOne():
    now = datetime.now()
    body = request.json
    body['fecha'] = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
    mediciones.append({**body, **tipo_medicion})
    return jsonify(mediciones)
    
@app.route('/')
def get():
    return jsonify(tipo_medicion)

@app.route('/mediciones', methods = ['GET'])
def getAll():
    return jsonify(mediciones)

@app.route('/mediciones/<porcentaje>', methods = ['GET'])
def getMayores(porcentaje):
    cantidad = len(mediciones)*float(porcentaje)
    lista = sorted(mediciones,key = lambda medicion: medicion['valor'])
    lista = lista[len(lista)-int(cantidad)-1:]

    return jsonify(lista) 

@app.route('/mediciones/<string:fecha>', methods=['DELETE'])
def deleteOne(fecha):
    x = False
    for medicion in mediciones:
        if (fecha in medicion['fecha']):
            x = True
            mediciones.remove(medicion)
    return 'Eliminado' if x else "No Encontrado"""

@app.route('/mediciones/<string:fecha>', methods=['PUT'])
def putOne(fecha):
    body = request.json
    x = False
    for medicion in mediciones:
        if(fecha in medicion['fecha']):
            x = True
            medicion['valor'] = body['valor']
    return 'Modificado' if x else 'No Encontrado'

app.run(port = 5000, debug = True)