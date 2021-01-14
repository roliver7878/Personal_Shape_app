
from flask import Flask, request, jsonify, make_response 
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager






# Making Flask Application
app = Flask(__name__)
jsonify
# Object of Api class
api = Api(app)





# Application Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/authdb_dev'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ThisIsHardestThing'
app.config['JWT_SECRET_KEY'] = 'Dude!WhyShouldYouEncryptIt'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

# SqlAlchemy object
db = SQLAlchemy(app)

# JwtManager object
jwt = JWTManager(app)

# Generating tables before first request is fetched
@app.before_first_request
def create_tables():

    db.create_all()

# Checking that token is in blacklist or not
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):

    jti = decrypted_token['jti']

    return models.RevokedTokenModel.is_jti_blacklisted(jti)

   
# Importing models and resources
import models.users, controllers.users
import models.profiles, controllers.profiles
import models.products, controllers.products
import models.programs, controllers.programs


# Api Endpoints

# Users
api.add_resource(controllers.users.UserRegistration, '/registration')
api.add_resource(controllers.users.UserLogin, '/login')
api.add_resource(controllers.users.UserLogoutAccess, '/logout/access')
api.add_resource(controllers.users.UserLogoutRefresh, '/logout/refresh')
api.add_resource(controllers.users.TokenRefresh, '/token/refresh')
api.add_resource(controllers.users.AllUsers, '/users')
api.add_resource(controllers.users.SecretResource, '/secret')

# Profiles
api.add_resource(controllers.profiles.NewProfile, '/profiles')
api.add_resource(controllers.profiles.AllProfiles, '/profiles')
api.add_resource(controllers.profiles.UpdateProfile, '/profiles')
api.add_resource(controllers.profiles.DeleteProfile, '/profiles/<id_profile>')

# Products
api.add_resource(controllers.products.NewProduct, '/products')
api.add_resource(controllers.products.AllProducts, '/products')

# Programs
api.add_resource(controllers.programs.NewProgram, '/programs')
api.add_resource(controllers.programs.AllPrograms, '/programs')