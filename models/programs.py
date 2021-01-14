from app import db
import datetime
from passlib.hash import pbkdf2_sha256 as sha256


class ProgramModel(db.Model):

    __tablename__ = 'programs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now())
    products = db.relationship('ProductModel', secondary = 'produto_program')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('UserModel')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_all(cls):

        def to_json(program):
            return {
                'name': program.name,
                'start_date': program.start_date,
                'end_date': program.end_date
            }
        return {'products': list(map(lambda program: to_json(program), ProgramModel.query.all()))}


    @classmethod
    def delete_all(cls):
        
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': f'{num_rows_deleted} row(s) deleted'}
        
        except:
            return {'message': 'Something went wrong'}