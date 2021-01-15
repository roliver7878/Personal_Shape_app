from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from models.profiles import ProfileModel


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
    def post(self):

        # get params from the request
        data = parser.parse_args()
        fullName = data['fullName']
        user_id = data['userId']

        # create model instance with the params
        new_profile = ProfileModel(
            full_name=fullName,
            user_id=user_id
        )

        try:
            # save model instance to db
            new_profile.save_to_db()
            return {'message': f'Profile created'}
        
        except:
            return jsonify({'message': 'Something went wrong'}), 500

class AllProfiles(Resource):
    
    # @jwt_required
    def get(self):
        return ProfileModel.return_all()


class DeleteProfile(Resource):
    
    def delete(self, id_profile):
        ProfileModel.delete(id_profile)
        return {'message': f'Profile deleted'}

class UpdateProfile(Resource):
    
    def put(self):
        data = parser.parse_args()
        id = data['id']
        fullName = data['fullName']
        print(id)
        print(fullName)

        ProfileModel.put(self, id, fullName)
        return {'message': f'Profile updated'}        