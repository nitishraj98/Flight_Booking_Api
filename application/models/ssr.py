from application.models import *


class SSRDetails(db.Model):
    __tablename__ = 'addon_ssr'
    id = Column(Integer, primary_key=True)
    uuid = Column(Text(collation="latin1_swedish_ci"))
    flight_uuid	= Column(Text(collation="latin1_swedish_ci"))
    ssr_details = Column(Text(collation="latin1_swedish_ci"))
    user_id = Column(Integer, nullable=False)
    is_modify = Column(Integer, nullable=False, default=True)
    create_at = Column(TIMESTAMP)
    update_at = Column(TIMESTAMP)
    amount = Column(Integer, nullable=False)
    
    

class SSRDetailsSchema(ma.Schema):
    default_error_messages = {
        "required": "Missing data for required field.",
        "null": "Field may not be null.",
        "validator_failed": "Invalid value.",
    }
    id = fields.Int(dump_only=True)
    uuid = fields.Str()
    flight_uuid = fields.Str()
    ssr_details = fields.Str()
    user_id = fields.Int()
    is_modify = fields.Int()
    create_at = fields.DateTime()
    update_at = fields.DateTime()
    amount = fields.Int()
    

   


SSRDetails_schema = SSRDetailsSchema()
SSRDetails_schema = SSRDetailsSchema(many=True)



