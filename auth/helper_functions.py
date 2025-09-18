from flask import jsonify, request
from functools import wraps

from config.dbconfig import get_connection

def is_duplicate_email(email):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
    email = cursor.fetchone()
    if email:
        return True
    return False


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            return (
                jsonify({"error": "Authorization required"}),
                401,
                {"WWW-Authenticate": 'Basic realm="Login Required"'},
            )

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email = %s", (auth.username,))
        user = cursor.fetchone()

        if not user or user["password"] != auth.password:
            return jsonify({"error": "Invalid credentials"}), 401

        # optionally attach user info to the request context
        request.user = user
        return f(*args, **kwargs)

    return decorated