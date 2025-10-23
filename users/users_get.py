from flask import request, jsonify

from config.dbconfig import get_connection
from helper_functions import auth_required, return_400_error_response
from . import users_bp

@users_bp.route("/users", methods=["GET"])
def get_all_users():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    return jsonify({
        "success": True, 
        "message": "All users fetched successfully", 
        "data": {
            "users": users,
            "count": len(users)
        }
    }), 200


@users_bp.route("/user", methods=["GET"])
@auth_required
def get_user_by_id():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    auth_user = request.user["id"]

    cursor.execute("SELECT * FROM users WHERE id = %s", (auth_user,))
    user = cursor.fetchone()

    return jsonify({
        "success": True, 
        "message": "User fetched successfully", 
        "data": {
            "user": user,
        }
    }), 200
