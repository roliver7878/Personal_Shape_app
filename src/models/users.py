from models.profiles import ProfileModel #Importing the class named ProfileModel from profile.py - Which is in the models directory 
from app import db
from models.programs import ProgramModel #Importing the class named ProfileModel from profile.py - Which is in the models directory 
from datetime import datetime
from passlib.hash import pbkdf2_sha256 as sha256
from flask import jsonify, make_response
import os, sys


class UserModel(db.Model):
    """
    User Model Class
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    Profile = db.relationship("ProfileModel", backref="user", lazy="dynamic")
    Program = db.relationship("ProgramModel", backref="user", lazy="dynamic")

    """
    Save user details in Database
    """
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    """
    Find user by username
    """
    @classmethod
    def find_by_username(cls, username):
        
        return cls.query.filter_by(username=username).first()

    """
    return all the user data in json form available in DB
    """
    @classmethod
    def return_all(cls):

        def to_json(user):
            return {
                'username': user.username,
                'password': user.password,
                'email': user.email
            }
        return {'users': list(map(lambda user: to_json(user), UserModel.query.all()))}

    """
    Delete user data
    """
    @classmethod
    def delete_all(cls):
        
        try:
        
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
        
            return {'message': f'{num_rows_deleted} row(s) deleted'}
        
        except:
        
            return {'message': 'Something went wrong'}

    """
    generate hash from password by encryption using sha256
    """
    @staticmethod
    def generate_hash(password):
        
        return sha256.hash(password)

    """
    Verify hash and password
    """
    @staticmethod
    def verify_hash(password, hash_):
        
        return sha256.verify(password, hash_)


    
    """
    Download user data
    """

    @staticmethod
    def download_all_data():

        cursor = db.session.connection().connection.cursor()
        cursor.execute(
            """SELECT table_name
            FROM information_schema.tables
            WHERE table_schema='public'""")
        table_names = cursor.fetchall()
        names = []
        for name in table_names:
            names.append(*name)

        timestamp = datetime.now().strftime("%Y-%m-%d;%H%:%M:%S")
        path = f"backup/All_table_time_{timestamp}"
        for name in names:
            filename = f"{path}/{name}.csv"
            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError:
                    raise "Can't create path"

            with open(filename, 'w') as sys.stdout:
                cursor.copy_to(sys.stdout, f"{name}", sep=',')

        return make_response(jsonify({
            'message': 'data downloaded'
        }), 200)





class RevokedTokenModel(db.Model):
    """
    Revoked Token Model Class
    """

    __tablename__ = 'revoked_tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    """
    Save Token in DB
    """
    def add(self):
    
        db.session.add(self)
        db.session.commit()

    """
    Checking that token is blacklisted
    """
    from app import jwt
    @classmethod
    def is_jti_blacklisted(cls, jti):
    
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)

    blacklist = set()
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in blacklist
