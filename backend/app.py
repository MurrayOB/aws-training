from flask import Flask
import os

app = Flask(__name__)

DEBUG = bool(os.environ.get("DEBUG", False))
app.config["DEBUG"] = DEBUG


@app.route("/")
def hello():
    return "Hello, World!!"


if __name__ == "__main__":
    app.run()
