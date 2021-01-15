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

# C - Create
class NewProduct(Resource):
  
    # @jwt_required
    def post(self):

        # get params from the request
        data = parser.parse_args()
        name = data['name']
        brand = data['brand']

        # make a new model instance with the params
        new_product = ProductModel(
            name=name,
            brand=brand
        )

        try:
            # save model instance to db
            new_product.save_to_db()
            return {'message': f'Product created'}
        
        except:
            return jsonify({'message': 'Something went wrong'}), 500

# R - Read
class AllProducts(Resource):
    
    # @jwt_required
    def get(self):
        return ProductModel.return_all()

# D - Delete
class DeleteProduct(Resource):
    
    def delete(self, id_product):
        ProductModel.delete(id_product)
        return {'message': f'Product deleted'}

# U - Update
class UpdateProduct(Resource):
    
    def put(self, id_product):
        # get product from database
        product = ProductModel.query.get(id_product)

        # update fields in the product
        data = parser.parse_args()
        product.name = data['name']
        product.brand = data['brand']

        # save product to db
        product.save_to_db()
        return {'message': f'Product updated'}        
