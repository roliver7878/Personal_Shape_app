from app import db
import datetime
from passlib.hash import pbkdf2_sha256 as sha256

class ProdutoProgram(db.Model):
    __tablename__ = 'produto_program'
    program_id = db.Column(
    db.Integer, 
    db.ForeignKey('programs.id'), 
    primary_key = True)

    product_id = db.Column(
    db.Integer, 
    db.ForeignKey('products.id'), 
    primary_key = True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit() 

    @classmethod
    def return_all(cls):

        def to_json(produtoprogram):
            return {
                'product_id': produtoprogram.product_id,
                'program_id': produtoprogram.program_id
            }
        return {'product to programs': list(map(lambda produtoprogram: to_json(produtoprogram), ProdutoProgram.query.all()))}





class ProductModel(db.Model):

    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now())
    programs = db.relationship('ProgramModel', secondary = 'produto_program')

    def save_to_db(self):

        if len(self.name) > 2 and len(self.brand) > 2:

            db.session.add(self)
            db.session.commit()
        else:

            raise Exception

    @classmethod
    def return_all(cls):

        def to_json(product):
            return {
                'name': product.name,
                'brand': product.brand
            }
        return {'products': list(map(lambda product: to_json(product), ProductModel.query.all()))}
    
    @classmethod
    def delete(self, id_product):
        product = ProductModel.query.filter_by(id=id_product).one()
        db.session.delete(product)
        db.session.commit()
    
    def put(self, id_product, name, brand):
        product = ProductModel.query.filter_by(id=id_product).one()
        if (name < 2 and brand < 2):
            return False
        product.name = name
        product.brand = brand
        db.session.add(product)
        db.session.commit() 
        return True

    @classmethod
    def delete_all(cls):
        
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': f'{num_rows_deleted} row(s) deleted'}
        
        except:
            return {'message': 'Something went wrong'}