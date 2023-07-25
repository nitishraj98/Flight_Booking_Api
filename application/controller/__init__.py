import random
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from flask import Flask, request, jsonify,json
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from application.__init__ import app
from application.controller.email_controller import send_registration_email
from application.models.users import User, UserSchema
from application.models.authenticate import TobApiDetails, TobApiDetailsSchema
from application.models.flights import SearchDetails, SearchDetailsSchema
from application.database import db
from application.controller.payment_controller import *
from flask_bcrypt import Bcrypt
from flask import session
from application.utils import ticket, book,calculate_insurance
from application.models.city_details import AirportCityCountryDetails,AirportCityCountryDetailsSchema




