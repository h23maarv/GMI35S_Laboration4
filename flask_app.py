from flask import Flask

from RuffelBagAB import RuffelBagAB

app = Flask(__name__)

app.register_blueprint(RuffelBagAB, url_prefix='/api/v1/cars')
