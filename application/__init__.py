from flask_cors import CORS
from flask import Flask, render_template, redirect, request, session
from flask_session import Session

app = Flask(__name__)
CORS(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
from application.route import * 