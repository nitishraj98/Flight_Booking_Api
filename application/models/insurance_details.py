from application.models import *


class InsuranceDetails(db.Model):
    __tablename__ = 'insurance_details'
    id = Column(Integer, primary_key=True)
    uuid = Column(String(50,"utf8mb4_0900_ai_ci"))
    flight_uuid	= Column(String(100,"utf8mb4_0900_ai_ci"))
    insurance_details = Column(String(100,"utf8mb4_0900_ai_ci"))
    userid = Column(Integer)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    price = Column(Integer)
    
    

class InsuranceDetailsSchema(ma.Schema):
    default_error_messages = {
        "required": "Missing data for required field.",
        "null": "Field may not be null.",
        "validator_failed": "Invalid value.",
    }
    id = fields.Int(dump_only=True)
    uuid = fields.Str()
    flight_uuid = fields.Str()
    insurance_details = fields.Str()
    userid = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    price = fields.Int()
    

InsuranceDetails_schema = InsuranceDetailsSchema()
InsuranceDetails_schema = InsuranceDetailsSchema(many=True)
   





