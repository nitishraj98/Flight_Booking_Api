from application.__init__ import app
from application.config import parseConfig
from flask_jwt_extended import JWTManager
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields




mysqlAnrari = parseConfig("anraridb","/etc/anrari.conf","=","mysql")


print(
f'mysql+pymysql://{mysqlAnrari.username}:{mysqlAnrari.password}:{mysqlAnrari.host}/{mysqlAnrari.database}')


app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{mysqlAnrari.username}:{mysqlAnrari.password}@{mysqlAnrari.host}/{mysqlAnrari.database}'

app.config['SQLALCHEMY_BINDS'] = {
'anraridb': f'mysql+pymysql://{mysqlAnrari.username}:{mysqlAnrari.password}@{mysqlAnrari.host}/{mysqlAnrari.database}'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)















