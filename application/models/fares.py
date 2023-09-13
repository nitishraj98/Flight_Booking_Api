from application.models import *

class Fare(db.Model):
    __tablename__ = 'fare'

    id = Column(Integer, primary_key=True)
    adult = Column(VARCHAR(255), nullable=False)
    child = Column(VARCHAR(255), nullable=False)
    infant = Column(VARCHAR(255), nullable=False)

class FareSchema(ma.Schema):
    default_error_messages = {
        "required": "Missing data for required field.",
        "null": "Field may not be null.",
        "validator_failed": "Invalid value.",
    }
    id = fields.Int
    adult = fields.Str()
    child = fields.Str()
    infant = fields.Str()