import sys
import os.path
from os import environ
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))   # this is very important stuff
from os import path
import logging
from flask import Flask, Blueprint
app = Flask(__name__)
from flask import render_template
log = logging.getLogger(__name__).setLevel(logging.CRITICAL)
logging.getLogger(__name__).propagate = False
logging.StreamHandler(stream=None)


@app.route("/")
def index():
    return render_template("index.html")


def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
