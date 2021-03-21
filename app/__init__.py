from flask import Flask
from flask_restful import Api
from resources.healthcheck_resource import HealthcheckResource
from resources.healthcheck_resource import HelloResource
from resources.healthcheck_resource import HostnameResource
from resources.healthcheck_resource import TomcatResource

app = Flask(__name__)
api = Api(app)

app.config['ENV'] = 'development'
app.config['DEBUG'] = True

api.add_resource(HealthcheckResource,'/healthcheck/')
api.add_resource(HelloResource,'/hello/<name>/<sobrenome>/')
api.add_resource(HostnameResource,'/hostname/')
api.add_resource(TomcatResource,'/<jmx_server>/<jmx_port>/<jmx_key>/')

app.run(host='0.0.0.0', port=5000)


