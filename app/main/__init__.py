from flask_restplus import Api
from flask import Blueprint

from .controller.artwork_retrieval_controller import api as artwork_ns

main = Blueprint('api', __name__)

api = Api(main,
          title='ARTWORK RETRIEVAL API WITH FLASK RESTPLUS AND JWT',
          version='1.0',
          description='An artwrok retrieval for flask restplus web service'
          )

api.add_namespace(artwork_ns, path='/artwork')

#from . import view
#from .controller.artwork_retrieval_controller import ArtworkSimList