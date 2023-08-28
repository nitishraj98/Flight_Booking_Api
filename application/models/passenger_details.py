from application.models import *


class PassengerDetails(db.Model):
    __tablename__ = 'passengers_details'
    id = Column(Integer, primary_key=True)
    uuid = Column(String(255,"utf8mb4_unicode_ci"), nullable=False)
    flight_uuid	= Column(String(255,"utf8mb4_unicode_ci	"), nullable=False)
    passenger_details = Column(String(255,"utf8mb4_unicode_ci"), nullable=False)
    ip = Column(String(255,"utf8mb4_unicode_ci"), nullable=False)
    search_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    is_active = Column(Integer, nullable=False, default=1)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    
    
    

class PassengerDetailsSchema(ma.Schema):
    default_error_messages = {
        "required": "Missing data for required field.",
        "null": "Field may not be null.",
        "validator_failed": "Invalid value.",
    }
    id = fields.Int()
    user_id = fields.Int()
    search_id = fields.Int()
    uuid = fields.Str()
    flight_uuid = fields.Str()
    passenger_details= fields.Str()
    ip = fields.Str()
    is_active = fields.Int()
    create_at = fields.DateTime()
    update_at = fields.DateTime()

PassengerDetails_schema = PassengerDetailsSchema()
PassengerDetails_schema = PassengerDetailsSchema(many=True)
    
    

   




