from flask import Flask
from flask_pymongo import PyMongo
app = Flask(__name__)
app.config["SECRET_KEY"] = "8K9Z8E0KgYT4a0e7"
app.config["MONGO_URI"] = "mongodb+srv://sudhrshan18:NaZFjUKdKlr2JrZF@cluster0.ma0bt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


mongodb_client = PyMongo(app)
db = mongodb_client.db
from application import routes
