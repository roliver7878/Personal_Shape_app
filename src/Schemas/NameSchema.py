from app import ma
from marshmallow.validate import Length

class NameCountSchema(ma.SQLAlchemyAutoSchema):
    username = ma.String()
    count = ma.Integer()

name_count_schema = NameCountSchema()
name_count_schemas = NameCountSchema(many=True)