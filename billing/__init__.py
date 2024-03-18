from flask import Flask, jsonify, render_template, redirect, request, send_file, url_for
from flask_sqlalchemy import SQLAlchemy
import logging

print("This file runs before the app")
print(f"__name__: {__name__}")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:1234@mysql/billdb"  # Note the database name change to 'billdb'

db = SQLAlchemy(app)