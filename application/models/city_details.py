from application.models.__init__ import *


class AirportCityCountryDetails(db.Model):
    __tablename__ = 'airport_city_country_details'
    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    isActive = Column(Boolean, nullable=False, default=True)
    Airport_Name = Column(String(255,"utf8mb4_unicode_ci"), nullable=False)
    Aiport_Code= Column(String(255,"utf8mb4_unicode_ci"), nullable=False)
    City_Name = Column(String(255,"utf8mb4_unicode_ci"), nullable=False)
    City_Code = Column(String(255,"utf8mb4_unicode_ci"), nullable=False)
    Country_Name = Column(String(255,"utf8mb4_unicode_ci"), nullable=False)
    Country_Code =Column(String(255,"utf8mb4_unicode_ci"), nullable=False)
    Nationalty = Column(String(255,"utf8mb4_unicode_ci"), nullable=False)
    Currency = Column(String(255,"utf8mb4_unicode_ci"), nullable=False)





class AirportCityCountryDetailsSchema(ma.Schema):
    default_error_messages = {
        "required": "Missing data for required field.",
        "null": "Field may not be null.",
        "validator_failed": "Invalid value.",
    }
    id = fields.Int(dump_only=True)
    isActive = fields.Bool()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    Airport_Name = fields.Str()
    Aiport_Code = fields.Str()
    City_Name= fields.Str()
    City_Code  = fields.Str()
    Country_Name = fields.Str()
    Country_Code = fields.Str()
    Nationalty = fields.Str()
    Currency = fields.Str()
    

   


AirportCityCountryDetails_schema = AirportCityCountryDetailsSchema()
AirportCityCountryDetails_schema = AirportCityCountryDetailsSchema(many=True)