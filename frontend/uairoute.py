from flask import Flask

app = Flask(__name__)
app.secret_key = 'uairoute-secret-key-2025'  # Necessário para sessões

from routes import *
from auth_routes import *

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug = True)