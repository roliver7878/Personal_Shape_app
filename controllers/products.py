from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from models.products import ProductModel

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt
)

import pdb

parser = reqparse.RequestParser()
parser.add_argument('name', required=False)
parser.add_argument('brand', required=False)

class NewProduct(Resource):
  
    # @jwt_required
    def post(self):

        data = parser.parse_args()
        name = data['name']
        brand = data['brand']

        new_product = ProductModel(
            name=name,
            brand=brand
        )

        try:
            new_product.save_to_db()
            return {'message': f'Profile created'}
        
        except:
            return jsonify({'message': 'Something went wrong'}), 500

class AllProducts(Resource):
    
    # @jwt_required
    def get(self):
        return ProductModel.return_all()