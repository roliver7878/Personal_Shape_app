from app import db
import datetime
from passlib.hash import pbkdf2_sha256 as sha256


class ProfileModel(db.Model):

    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    user = db.relationship('UserModel')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_all(cls):

        def to_json(profile):
            return {
                'fullName': profile.full_name,
                'user': profile.user_id
            }
        return {'profiles': list(map(lambda profile: to_json(profile), ProfileModel.query.all()))}


    @classmethod
    def delete(self, id_profile):
        profile = ProfileModel.query.filter_by(id=id_profile).one()
        db.session.delete(profile)
        db.session.commit()


    def put(self, id_profile, full_name):
        profile = ProfileModel.query.filter_by(id=id_profile).one()
        profile.full_name = full_name
        db.session.add(profile)
        db.session.commit() 