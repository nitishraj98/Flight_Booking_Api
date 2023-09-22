from flask_cors import CORS
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from datetime import timedelta
from flask_jwt_extended import JWTManager 

app = Flask(__name__)
CORS(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["JWT_SECRET_KEY"] = "super-secret"  
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=10)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)
Session(app)
from application.route import * 