from flask import Flask, jsonify
import os

app = Flask(__name__)
# Configure SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'saga_logs.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False