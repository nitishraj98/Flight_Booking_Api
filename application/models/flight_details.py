from application.models import *


class FlightDetails(db.Model):
    __tablename__ = 'flight_details'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(50, collation="utf8mb4_0900_ai_ci"))
    result_index = Column(String(10, collation="utf8mb4_0900_ai_ci"), nullable=False)
    is_lcc = Column(Integer, default=0)
    trace_id = Column(String(100, collation="utf8mb4_0900_ai_ci"), nullable=False)
    fare_quote = Column(String(250, collation="utf8mb4_0900_ai_ci"))
    fare_rules = Column(String(250, collation="utf8mb4_0900_ai_ci"), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    create_at = Column(TIMESTAMP)
    update_at = Column(TIMESTAMP)
    journey_type = Column(Integer)
    isPassportRequired = Column(Integer,default=0)
    isInternational = Column(Integer, default=0)
    total_pax = Column(Integer, default=0)



    


class FlightDetailsSchema(ma.Schema):
    default_error_messages = {
        "required": "Missing data for required field.",
        "null": "Field may not be null.",
        "validator_failed": "Invalid value.",
    }
    uuid = fields.Str()
    result_index = fields.Str()
    is_lcc = fields.Int()
    trace_id = fields.Str()
    fare_quote  = fields.Str()
    fare_rules = fields.Str()
    is_active = fields.Bool()
    create_at = fields.DateTime()
    update_at = fields.DateTime()
    journey_type = fields.Int()


   

