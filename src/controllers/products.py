from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from models.products import ProductModel, ProdutoProgram
from models.programs import ProgramModel
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
parser.add_argument('product_id', required=False)
parser.add_argument('program_id', required=False)


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
            'message': 'something went wrong. Check inputs are all valid and length greater than 2'
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

class JoinProdutoProgram(Resource):
    
    def post(self):

        data = parser.parse_args()
        program_id = data['program_id']
        product_id = data['product_id']

        # Check if product with product id does exist

        product_model_object = ProductModel.query.filter_by(id=product_id).first()

        if not product_model_object:
            return make_response(jsonify({
                'Message': f'Product with id {product_id} does not exist'
            }), 500)       
        

        # Check if program with program id does exist

        program_model_object = ProgramModel.query.filter_by(id=program_id).first()

        if not program_model_object:
            return make_response(jsonify({
                'Message': f'Program with id {program_id} does not exist'
            }), 500)       

        # Check if program with program id and product with product id already have join record

        produtoprogram_model_object = ProdutoProgram.query.filter_by(program_id=program_id, product_id=product_id).first()

        if produtoprogram_model_object:
            return make_response(jsonify({
                'Message': f'Program with id {program_id} and product with id {product_id} join record already exists'
            }), 500)


        # create model instance with the params
        new_produtoprogram_model_object = ProdutoProgram(
            program_id=program_id,
            product_id=product_id
        )


        try:
            # save model instance to db
            new_produtoprogram_model_object.save_to_db()
            return make_response(jsonify({
            'message': 'new product to program created'
        }), 200)
        
        except:
            return make_response(jsonify({
            'message': 'something went wrong. Check that the product id and program id exist'
        }), 500)

class AllProdutoPrograms(Resource):
    
    # @jwt_required
    def get(self):
        return ProdutoProgram.return_all()