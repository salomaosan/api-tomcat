from flask_restful import Resource
from flask_restful import reqparse
from models.hostname_models import get_hostname
from models.get_data import get_dados


class TomcatResource(Resource):
    def get(self, jmx_server, jmx_port, jmx_key):
        dados = get_dados(jmx_server, jmx_port, jmx_key)
        return dados

class HostnameResource(Resource):
    def get(self):
        hostname = get_hostname()
        return {"message": f'Api is running on {hostname}'}

class HealthcheckResource(Resource):
    def get(self):
        return {"message": "Api is working"}

class HelloResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('idade', type=str, required=True, help='O campo idade deve ser preenchido')

    def get(self, name, sobrenome):
        message = f'Hello {name} {sobrenome}'
        return {'message': message}

    def post(self, name):
        data = HelloResource.parser.parse_args()
        idade = data['idade']
        return {'message': f'A idade de {name} é {idade} anos.'}