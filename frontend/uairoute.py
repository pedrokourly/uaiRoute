from flask import Flask
import os
from config import DEBUG, SECRET_KEY, get_template_config

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Disponibilizar configurações para todos os templates
@app.context_processor
def inject_config():
    return {'config': get_template_config()}

from routes import *
from auth_routes import *

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=DEBUG)