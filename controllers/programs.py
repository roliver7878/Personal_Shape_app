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
parser.add_argument('start_date', required=False)
parser.add_argument('end_date', required=False)

# C - Create
class NewProgram(Resource):
  
    # @jwt_required
    def post(self):

        data = parser.parse_args()
        name = data['name']
        start_date = data['start_date'],
        end_date = data['end_date']

        # create model instance with the params
        new_program = ProgramModel(
            name=name,
            start_date=start_date
            end_date=end_date

            
        )

        try:
            # save model instance to db
            new_program.save_to_db()
            return {'message': f'Program created'}
        
        except:
            return jsonify({'message': 'Something went wrong'}), 500

class AllPrograms(Resource):
    
    # @jwt_required
    def get(self):
        return ProgramModel.return_all()

class DeleteProgram(Resource):

def delete(self, id_program):
    ProgramModel.delete(id_program)
    return {'message': f'Program deleted'}


class UpdateProgram(Resource):
    
    def put(self):
        data = parser.parse_args()
        id = data['id']
        name = data['name']
        start_Date = data['startDate']
        end_date = data['endDate']

        # get params from the request
        data = parser.parse_args()
        fullName = data['fullName']
        user_id = data['userId']
