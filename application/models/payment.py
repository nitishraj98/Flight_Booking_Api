from application.models import *


class PaymentInformation(db.Model):
    __tablename__ = 'payment_informations'
    id = Column(Integer, primary_key=True)
    flight_uuid	= Column(String("utf8mb4_0900_ai_ci"))
    user_id = Column(Integer)
    is_active = Column(Integer, default=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    orderid = Column(String("utf8mb4_0900_ai_ci"))
    transaction = Column(String("utf8mb4_0900_ai_ci"))
    amount = Column(Integer)
    ip = Column(String(45,"utf8mb4_0900_ai_ci"))
    gateway_name = Column(String(255,"utf8mb4_0900_ai_ci"))
    gateway_status = Column(String("utf8mb4_0900_ai_ci"))
    search_id = Column(Integer)
    
    
    

class PaymentInformationSchema(ma.Schema):
    default_error_messages = {
        "required": "Missing data for required field.",
        "null": "Field may not be null.",
        "validator_failed": "Invalid value.",
    }
    id = fields.Int(dump_only=True)
    flight_uuid = fields.Str()
    user_id = fields.Int()
    is_active = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    orderid = fields.Str()
    transaction = fields.Str()
    ip = fields.Str()
    gateway_name = fields.Str()
    gateway_status = fields.Str()
    amount = fields.Int()
    search_id = fields.Int()
    
    

 




