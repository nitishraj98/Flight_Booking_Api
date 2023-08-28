from application.models import *


class TobApiDetails(db.Model):
    __tablename__ = 'tob_api_details'
    id = Column(Integer, primary_key=True)
    tokenId = Column(Text(collation="utf8mb4_unicode_ci"), nullable=False)
    ApiName = Column(Text(collation="utf8mb4_unicode_ci"))
    UserName = Column(Text(collation="utf8mb4_unicode_ci"))
    Password = Column(Text(collation="utf8mb4_unicode_ci"))
    AuthenticateUrl = Column(Text(collation="utf8mb4_unicode_ci"))
    SearchUrl = Column(Text(collation="utf8mb4_unicode_ci"))
    BookUrl = Column(Text(collation="utf8mb4_unicode_ci"))
    isActive = Column(Boolean, nullable=False, default=True)
    user_id = Column(Integer)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)



 

class TobApiDetailsSchema(ma.Schema):
    default_error_messages = {
        "required": "Missing data for required field.",
        "null": "Field may not be null.",
        "validator_failed": "Invalid value.",
    }
    id = fields.Int(dump_only=True)
    tokenId = fields.Str(required=True)
    ApiName = fields.Str()
    UserName = fields.Str()
    Password = fields.Str()
    AuthenticateUrl = fields.Str()
    SearchUrl = fields.Str()
    BookUrl = fields.Str()
    isActive = fields.Bool()
   
    created_at = fields.DateTime()
    updated_at = fields.DateTime()



TobApiDetails_schema = TobApiDetailsSchema()
TobApiDetails_schema = TobApiDetailsSchema(many=True)