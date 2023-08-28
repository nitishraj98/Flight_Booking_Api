from application.models import *


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    email = Column(String(255,"utf8mb4_unicode_ci"), unique=True, nullable=False)
    name = Column(String(255,"utf8mb4_unicode_ci"), nullable=False)
    mobile_no = Column(String(100,"utf8mb4_unicode_ci"), unique=True, nullable=False)
    password = Column(String(255,"utf8mb4_unicode_ci"), nullable=False)
    remember_token = Column(String(100,"utf8mb4_unicode_ci"), nullable=False)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    is_active = Column(Integer, default=True)
    otp = Column(String(100,"utf8mb4_unicode_ci"))





class UserSchema(ma.Schema):
    default_error_messages = {
        "required": "Missing data for required field.",
        "null": "Field may not be null.",
        "validator_failed": "Invalid value.",
    }
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    mobile_no = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    confirm_password = fields.Str(required=True)
    is_active = fields.Bool()   
    otp = fields.Str(required=True)




user_schema = UserSchema()
users_schema = UserSchema(many=True)


class GenOtp(db.Model):
    __tablename__ = 'generate_otp'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    email = Column(String(255,"utf8mb4_unicode_ci"), unique=True, nullable=False)
    name = Column(String(255,"utf8mb4_unicode_ci"), nullable=False)
    mobile_no = Column(String(100,"utf8mb4_unicode_ci"), unique=True, nullable=False)
    password = Column(String(255,"utf8mb4_unicode_ci"), nullable=False)
    otp = Column(String(255,"utf8mb4_unicode_ci"), nullable=False)


class GenOtpSchema(ma.Schema):
    default_error_messages = {
        "required": "Missing data for required field.",
        "null": "Field may not be null.",
        "validator_failed": "Invalid value.",
    }
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    mobile_no = fields.Str(required=True)
    password = fields.Str(required=True)
    otp = fields.Str(required=True)


