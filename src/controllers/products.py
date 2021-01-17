from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from models.products import ProductModel
from models.users import UserModel
from Schemas.ProductSchema import product_schema, product_schemas
import json

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
parser.add_argument('id', required=False)
parser.add_argument('name', required=False)
parser.add_argument('brand', required=False)

class NewProduct(Resource):
  
    # @jwt_required
    # POST /profiles
    # Create route

    def post(self):

        # get params from the request
        data = parser.parse_args()
        name = data['name']
        brand = data['brand']


        # create model instance with the params
        new_product = ProductModel(
            name=name,
            brand=brand
        )


        try:
            # save model instance to db
            new_product.save_to_db()
            return make_response(jsonify({
            'message': 'new product created'
        }), 200)
        
        except:
            return make_response(jsonify({
            'message': 'something went wrong'
        }), 500)

class AllProducts(Resource):
    
    # @jwt_required
    def get(self):
        all_products = ProductModel.query.all()
        return ProductModel.return_all()


class DeleteProduct(Resource):
    
    def delete(self, id_product):

        product_model = ProductModel.query.filter_by(id=id_product).first()

        if not product_model:
            return make_response(jsonify({
            'message': f'No product with id {id_product} exists'
        }), 500)

        ProductModel.add(id_product)
        return {'message': f'Product deleted'}

class UpdateProduct(Resource):
    
    def put(self, id_product):
        data = parser.parse_args()
        name = data['name']
        brand = data['brand']

        product_model_object = ProductModel.query.filter_by(id=id_product).first()

        if not product_model_object:
            return make_response(jsonify({
            'message': f'No product with id {id_product} exists'
        }), 500)

        # product_model_object.update(product_fields)

        valid_data = ProductModel.put(self, id_product, name, brand)

        if not valid_data:
            return make_response(jsonify({
                'message': f'Invalid data entered'
            }), 500)       

        return make_response(jsonify({
            'message': f'Product with id {id_product} updated'
        }), 200)       