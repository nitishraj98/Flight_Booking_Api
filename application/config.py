from application import app
from configparser import ConfigParser

class parseConfig:
    def __init__(self,context,config_path,delimeter,app):
        config = ConfigParser(delimiters=(delimeter))
        config.read(config_path)
        if app == 'mysql':
            self.database = config.get(context,'database')
            self.username = config.get(context,'username')
            self.password = config.get(context,'password')
            self.host = config.get(context,'host')
            

        if app == 'misc':
            self.jwt_key = config.get(context, 'jwt_key')
            self.base_url = config.get(context,'base_url')
            self.sms_url = config.get(context,'sms_url')
            self.auth_url = config.get(context,'auth_url')
            self.secret_key = config.get(context,'secret_key')
            self.sender_email = config.get(context,'sender_email')
            self.sender_password = config.get(context,'sender_password')
            self.ClientId = config.get(context,'ClientId')
            self.UserName = config.get(context,'UserName')
            self.Password  = config.get(context,'Password')
            self.EndUserIp = config.get(context,'EndUserIp')
        
        if app == 'redis':
            self.host = config.get(context,'host')
            self.port = config.get(context,'port')
            self.password = config.get(context,'password')

jwt_secret = parseConfig("general","/etc/anrari.conf","=","misc")

app.config.update(
    TESTING = True,
    DEBUG=True,
    FLASK_ENV='development',
    JWT_BLACKLIST_ENABLED=True,
    JWT_BLACKLIST_TOKEN_CHECKS='access',
    MAIL_DEBUG=True,
    CORS_HEADERS="Content-Type", 
    JWT_SECRET_KEY=jwt_secret.jwt_key,
    BASE_URL=jwt_secret.base_url,
    SMS_URL=jwt_secret.sms_url,
    AUTH_URL=jwt_secret.auth_url,
    SECRET_KEY=jwt_secret.secret_key,
    SENDER_EMAIL=jwt_secret.sender_email,
    SENDER_PASSWORD=jwt_secret.sender_password,
    CLIENTID=jwt_secret.ClientId,
    USERNAME=jwt_secret.UserName,
    PASSWORD=jwt_secret.Password,
    ENDUSERIP=jwt_secret.EndUserIp



)





