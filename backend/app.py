from flask import Flask
import os

app = Flask(__name__)

DEBUG = bool(os.environ.get("DEBUG", False))
app.config["DEBUG"] = DEBUG


@app.route("/")
def hello():
    return "Hello, World!"


if __name__ == "__main__":
    # app.run(host='0.0.0.0')
    app.run(host='0.0.0.0', port=5050)
