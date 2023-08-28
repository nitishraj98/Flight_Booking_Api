from application.models import *


class BookDetails(db.Model):
    __tablename__ = 'book_details'
    id = Column(Integer, primary_key=True)
    booking_details	= Column(Integer)
    user_id = Column(Text(collation="latin1_swedish_ci"))
    total_amount = Column(String)
    is_active = Column(Integer, default=True)
    create_at = Column(TIMESTAMP)
    update_at = Column(TIMESTAMP)
    
class BookDetailsSchema(ma.Schema):
    default_error_messages = {
        "required": "Missing data for required field.",
        "null": "Field may not be null.",
        "validator_failed": "Invalid value.",
    }
    id = fields.Int(dump_only=True)
    booking_details = fields.Int()
    user_id = fields.Str()
    total_amount = fields.Str()
    is_active = fields.Int()
    create_at = fields.DateTime()
    update_at = fields.DateTime()
    

BookDetails_schema = BookDetailsSchema()
BookDetails_schema = BookDetailsSchema(many=True)
    
   






