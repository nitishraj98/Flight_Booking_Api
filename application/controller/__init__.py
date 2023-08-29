import random
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from flask import Flask, request, jsonify,json
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from application import app
from application.controller.email_controller import send_registration_email
from application.models.users import User, UserSchema, GenOtp, GenOtpSchema
from application.models.authenticate import TobApiDetails, TobApiDetailsSchema
from application.models.flights import SearchDetails, SearchDetailsSchema
from application.database import db
from application.controller.payment_controller import *
from flask_bcrypt import Bcrypt
from flask import session
from application.utils import book, calculate_insurance, ticket_for_true_lcc, ticket_for_false_lcc
from application.models.city_details import AirportCityCountryDetails,AirportCityCountryDetailsSchema
from application.models.ssr import SSRDetails,SSRDetailsSchema
from application.models.flight_details import FlightDetails,FlightDetails_schema
from application.models.payment import *
from datetime import datetime
import bcrypt
from application.models.flight_details import *
from application.models.passenger_details import *
from application.models.book_details import *
from application.models.ticket_details import *
from application.models.insurance_details import *
from flask import session
import uuid
from application.config import *
import razorpay
# import uuid
from datetime import datetime
from application.models.payment import *
import schedule
import time







