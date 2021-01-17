from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from models.programs import ProgramModel
from models.users import UserModel


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
parser.add_argument('start_date', required=False)
parser.add_argument('end_date', required=False)
parser.add_argument('user_id', required=False)




class NewProgram(Resource):
  
    # @jwt_required
    # POST /profiles
    # Create route
    @jwt_required
    def post(self):

        # get params from the request
        data = parser.parse_args()
        name = data['name']
        start_date = data['start_date']
        end_date = data['end_date']

        username = get_jwt_identity()

        
        current_user = UserModel.find_by_username(username)
        user_id = current_user.id
        program_model = ProgramModel.query.filter_by(user_id=user_id).first()
        

        if program_model:
            return make_response(jsonify({
            'message': f'profile for user {username} already exists'
        }), 500)


        # create model instance with the params
        new_program = ProgramModel(
            name=name,
            start_date=start_date,
            end_date=end_date,
            user_id=user_id
        )


        try:
            # save model instance to db
            new_program.save_to_db()
            return make_response(jsonify({
            'message': 'new program created'
        }), 200)
        
        except:
            return make_response(jsonify({
            'message': 'something went wrong'
        }), 500)

class AllPrograms(Resource):
    
    # @jwt_required
    def get(self):
        return ProgramModel.return_all()


class DeleteProgram(Resource):
    
    @jwt_required
    def delete(self, id_program):
        username = get_jwt_identity()
        current_user = UserModel.find_by_username(username)

        if not current_user:
            return make_response(jsonify({
            'message': f'no user has that jwt'
        }), 500)


        user_id = current_user.id
        program_model = ProgramModel.query.filter_by(id=id_program, user_id=user_id).first()

        if not program_model:
            return make_response(jsonify({
            'message': f'user does not own profile with id {id}'
        }), 500)

        ProgramModel.delete(id_program)
        return {'message': f'Program deleted'}

class UpdateProgram(Resource):
    
    @jwt_required
    def put(self, id_program):
        data = parser.parse_args()
        name = data['name']
        start_date = data['start_date']
        end_date = data['end_date']

        username = get_jwt_identity()
        current_user = UserModel.find_by_username(username)

        if not current_user:
            return make_response(jsonify({
            'message': f'no user has that jwt'
        }), 500)

        user_id = current_user.id

        program_model = ProgramModel.query.filter_by(id=id_program, user_id=user_id).first()

        if not program_model:
            return make_response(jsonify({
            'message': f'user does not own program with id {id_program}'
        }), 500)

        
        ProgramModel.put(self, id_program, name, start_date, end_date)
        return {'message': f'Program updated'}        