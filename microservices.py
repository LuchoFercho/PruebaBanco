from flask import Flask
from flask import Response
from flask_restful import Api, Resource, reqparse
from flask import jsonify
import json
from CrudDynamoPrueba import crud_dynamo_banc

# import fuzz_search
app = Flask(__name__)
api = Api(app)

'''
EJEMPLO DE PETICION
curl -d "ef=/home/pdi/pdi/ocr-tp/1 Columna/28306771_EEFF_COLGAAP.tiff&nc=path_nc" -X POST http://localhost:1232/path
'''

# 400 Bad Request
r_400 = Response("Peticion invalida.", status=400)

# 500 Internal Server Error
r_500 = Response("Error interno del servidor", status=500)


class User(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("accion")       #Agregar, leer, actualizar, eliminar
        parser.add_argument("userid")       
        parser.add_argument("username")
        parser.add_argument("age")
        args = parser.parse_args()

        accion=args['accion']
        userid=int(args['userid'])
        username=args['username']
        if(args['age']!=None):
            age=int(args['age'])
        else:
            age=1000

        response=crud_dynamo_banc(accion,userid,username,age)
        return response

 

api.add_resource(User, "/")

app.run(debug=True, port=4000, host='0.0.0.0')