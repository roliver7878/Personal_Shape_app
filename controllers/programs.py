from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from models.programs import ProgramModel

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
parser.add_argument('startDate', required=False)
parser.add_argument('endDate', required=False)

class NewProgram(Resource):
  
    # @jwt_required
    def post(self):

        data = parser.parse_args()
        name = data['name']
        startDate = data['startDate'],
        endDate = data['endDate']

        new_program = ProgramModel(
            name=name,
            endDate=endDate
        )

        try:
            new_program.save_to_db()
            return {'message': f'Program created'}
        
        except:
            return jsonify({'message': 'Something went wrong'}), 500

class AllPrograms(Resource):
    
    # @jwt_required
    def get(self):
        return ProgramModel.return_all()