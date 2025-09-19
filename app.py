from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta

from config.dbconfig import *
from auth import auth_bp
from users import users_bp
from tasks import tasks_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(tasks_bp)


@app.route("/")
def root():
    return jsonify({"message": "Welcome to Tomorrow!"})


@app.route("/tomorrow-date", methods=["GET"])
def fetch_tomorrow_date():
    tomorrow = datetime.now() + timedelta(days=1)

    # extract day and month
    day = tomorrow.day
    month = tomorrow.month
    month_name = tomorrow.strftime("%B")

    return (
        jsonify(
            {
                "success": True,
                "message": "Tomorrow's date fetched successfully",
                "data": {"day": day, "month": month, "month_name": month_name},
            }
        ),
        200,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
