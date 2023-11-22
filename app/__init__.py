from flask import Flask
from app import routes
from os import environ

app = Flask(__name__)
app.config.update({'SECRET_KEY': environ.get('SECRET_KEY')})
app.register_blueprint(routes.bp)
