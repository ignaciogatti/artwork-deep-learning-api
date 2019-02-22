from flask import request
from flask_restplus import Resource
from ..service.artwork_encode_service import predict
from ..utils.dto import ArtworkDto

api = ArtworkDto.api

@api.route('/predict/<image>')
@api.param('image', 'The image to encode')
class ArtworkCodeMatrix(Resource):
    @api.doc('code_matrix_arwroks')
    def post(self, image):
        """Encode artwork"""
        data = request.json
        return predict(data)
