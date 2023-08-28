from application.models import *


class SearchDetails(db.Model):
    __tablename__ = 'search_details'
    id = Column(Integer, primary_key=True)
    ip = Column(String(255,"utf8mb4_unicode_ci"), nullable=False)
    result_index= Column(String(255,"utf8mb4_unicode_ci"), nullable=False)
    flight_details = Column(Text(collation="utf8mb4_unicode_ci"))
    trace_id = Column(Text(collation="utf8mb4_unicode_ci"))
    origin = Column(String(255,"utf8mb4_unicode_ci"), nullable=False)
    destination =Column(String(255,"utf8mb4_unicode_ci"), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)





class SearchDetailsSchema(ma.Schema):
    default_error_messages = {
        "required": "Missing data for required field.",
        "null": "Field may not be null.",
        "validator_failed": "Invalid value.",
    }
    id = fields.Int(dump_only=True)
    ip = fields.Str(required=True)
    result_index = fields.Str()
    flight_details = fields.Str()
    trace_id = fields.Str()
    origin  = fields.Str()
    destination = fields.Str()
    is_active = fields.Bool()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

   


SearchDetails_schema = SearchDetailsSchema()
SearchDetails_schema = SearchDetailsSchema(many=True)