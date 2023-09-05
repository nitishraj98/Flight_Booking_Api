from application.models import *


class TicketDetails(db.Model):
    __tablename__ = 'ticket_details'
    id = Column(Integer, primary_key=True)
    ticket_details	= Column(String)
    user_id = Column(Integer)
    booking_id = Column(Integer)
    is_active = Column(Integer, default=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    
class TicketDetailsSchema(ma.Schema):
    default_error_messages = {
        "required": "Missing data for required field.",
        "null": "Field may not be null.",
        "validator_failed": "Invalid value.",
    }
    id = fields.Int(dump_only=True)
    ticket_details = fields.Str()
    user_id = fields.Int()
    booking_id = fields.Int()
    is_active = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
   






