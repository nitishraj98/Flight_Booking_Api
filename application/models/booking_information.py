from application.models.__init__ import *


class BookingInformation(db.Model):
    __tablename__ = 'booking_informations'
    id = Column(Integer, primary_key=True)
    pnr = Column(String(255,"utf8mb4_unicode_ci"))
    booking_id	= Column(String(255,"utf8mb4_unicode_ci"))
    booking_history = Column(String)
    user_id = Column(Integer)
    payment_id = Column(Integer)
    is_active = Column(Integer, default=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    
class BookingInformationSchema(ma.Schema):
    default_error_messages = {
        "required": "Missing data for required field.",
        "null": "Field may not be null.",
        "validator_failed": "Invalid value.",
    }
    id = fields.Int(dump_only=True)
    pnr = fields.Str()
    booking_id = fields.Str()
    booking_history = fields.Str()
    user_id = fields.Int()
    payment_id = fields.Int()
    is_active = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    

BookingInformation_schema = BookingInformationSchema()
BookingInformation_schema = BookingInformationSchema(many=True)
    
   






