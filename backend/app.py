import json
from flask import Flask, Response
import os
import src.core.db_operations as db
from src.controllers.data import Data

app = Flask(__name__)

DEBUG = bool(os.environ.get("DEBUG", False))
app.config["DEBUG"] = DEBUG
PORT = os.environ.get("PORT", 5050)


@app.route("/")
def welcome():
    return "Welcome, go to /data to see a connection!"


@app.route("/data")
def data():
    data = Data.fetchAll()
    return Response(data.to_json(), status=200, mimetype='application/json')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)
