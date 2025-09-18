from flask import Flask, request, jsonify
from flask_cors import CORS

from config.dbconfig import *
from auth import auth_bp
from users import users_bp
from tasks import tasks_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(tasks_bp)

@app.route('/')
def root():
    return jsonify({"message": "Welcome to Tomorrow!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
