from app import ma
from models.products import ProductModel
from marshmallow.validate import Length

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # model = ProductModel
        name = ma.String(required=True, validate=Length(min=2))
        brand = ma.String(required=True,  validate=Length(min=2))

product_schema = ProductSchema()
product_schemas = ProductSchema(many=True)
