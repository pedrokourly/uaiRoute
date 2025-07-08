from flask import Flask
import os
from config import DEBUG, SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

from routes import *
from auth_routes import *

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=DEBUG)