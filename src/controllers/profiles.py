from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from models.profiles import ProfileModel
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
parser.add_argument('fullName', required=False)
parser.add_argument('userId', required=False)

class NewProfile(Resource):
  
    # @jwt_required
    # POST /profiles
    # Create route
    @jwt_required
    def post(self):

        # get params from the request
        data = parser.parse_args()
        fullName = data['fullName']
        username = get_jwt_identity()

        
        current_user = UserModel.find_by_username(username)
        user_id = current_user.id
        profile_model = ProfileModel.query.filter_by(user_id=user_id).first()
        

        if profile_model:
            return make_response(jsonify({
            'message': f'profile for user {username} already exists'
        }), 500)


        # create model instance with the params
        new_profile = ProfileModel(
            full_name=fullName,
            user_id=user_id
        )


        try:
            # save model instance to db
            new_profile.save_to_db()
            return make_response(jsonify({
            'message': 'new profile created'
        }), 200)
        
        except:
            return make_response(jsonify({
            'message': 'something went wrong'
        }), 500)

class AllProfiles(Resource):
    
    # @jwt_required
    def get(self):
        return ProfileModel.return_all()


class DeleteProfile(Resource):
    
    @jwt_required
    def delete(self, id_profile):
        username = get_jwt_identity()
        current_user = UserModel.find_by_username(username)

        if not current_user:
            return make_response(jsonify({
            'message': f'no user has that jwt'
        }), 500)


        user_id = current_user.id
        profile_model = ProfileModel.query.filter_by(id=id_profile, user_id=user_id).first()

        if not profile_model:
            return make_response(jsonify({
            'message': f'user does not own profile with id {id}'
        }), 500)

        ProfileModel.delete(id_profile)
        return {'message': f'Profile deleted'}

class UpdateProfile(Resource):
    
    @jwt_required
    def put(self, id_profile):
        data = parser.parse_args()
        fullName = data['fullName']

        username = get_jwt_identity()
        current_user = UserModel.find_by_username(username)

        if not current_user:
            return make_response(jsonify({
            'message': f'no user has that jwt'
        }), 500)


        user_id = current_user.id

        profile_model = ProfileModel.query.filter_by(id=id_profile, user_id=user_id).first()

        
        if not profile_model:
            return make_response(jsonify({
            'message': f'user does not own profile with id {id_profile}'
        }), 500)

        valid_data = ProfileModel.put(self, id_profile, fullName)

        if not valid_data:
            return make_response(jsonify({
                'message': f'Invalid data entered'
            }), 500)       


        return {'message': f'Profile updated'}        