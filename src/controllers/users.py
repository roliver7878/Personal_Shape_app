from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from models.users import UserModel, RevokedTokenModel
from datetime import timedelta

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
parser.add_argument('username', help='username cannot be blank', required=True)
parser.add_argument('password', help='password cannot be blank', required=True)
parser.add_argument('email', required=False)

class UserRegistration(Resource):
    """
    User Registration Api
    """

    def post(self):

        data = parser.parse_args()
        username = data['username']
        email = data['email']

        # Checking if  user already exist/created
        if UserModel.find_by_username(username):
            return {'message': f'User {username} already exists'}

        # create new user
        new_user = UserModel(
            username=username,
            password=UserModel.generate_hash(data['password']),
            email=email
        )

        # try:
            
            # Saving user in DB and Generating Access and Refresh token
        new_user.save_to_db()
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        return make_response(jsonify({
            'message': f'User {username} was created',
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200)
        
        # except:
        #     return make_response(jsonify({ 'message': "Failed to register" }), 500)


class UserLogin(Resource):
    """
    User Login Api
    """

    def post(self):
    
        data = parser.parse_args()
        username = data['username']

        # Searching user by username
        current_user = UserModel.find_by_username(username)
        
        # user does not exists
        if not current_user:
        
            return jsonify({'message': f'User {username} doesn\'t exist'})
        
        # user exists, comparing password and hash
        if UserModel.verify_hash(data['password'], current_user.password):
            
            # generating access token and refresh token
            access_token = create_access_token(identity=username, expires_delta=timedelta(days=1) )
            refresh_token = create_refresh_token(identity=username)
        
            return jsonify({
        
                'message': f'Logged in as {username}',
                'access_token': access_token,
                'refresh_token': refresh_token
            })
        
        else:
        
            return jsonify({'message': "Wrong credentials"})


class UserLogoutAccess(Resource):
    """
    User Logout Api 
    """
    
    @jwt_required
    def post(self):
        
        jti = get_raw_jwt()['jti']
        
        try:
            # Revoking access token
            revoked_token = RevokedTokenModel(jti=jti)
            
            revoked_token.add()
    
            return jsonify({'message': 'Access token has been revoked'})
    
        except:
    
            return jsonify({'message': 'Something went wrong'}), 500


class UserLogoutRefresh(Resource):
    """
    User Logout Refresh Api 
    """
    @jwt_refresh_token_required
    def post(self):

        jti = get_raw_jwt()['jti']
        
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            pdb.set_trace()
            return jsonify({'message': 'Refresh token has been revoked'})
        except:
            return jsonify({'message': 'Something went wrong'}), 500


class TokenRefresh(Resource):
    """
    Token Refresh Api
    """

    @jwt_refresh_token_required
    def post(self):
        
        # Generating new access token
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
    
        return jsonify({'access_token': access_token})


class AllUsers(Resource):
    
    # @jwt_required
    def get(self):
        """
        return all user api
        """
        return UserModel.return_all()

    def delete(self):
        """
        delete all user api
        """
        return UserModel.delete_all()


class SecretResource(Resource):

    """
    Secrest Resource Api
    You can create crud operation in this way
    """
    @jwt_required
    def get(self):
        return jsonify({'answer': 'You are accessing super secret blueprint'})