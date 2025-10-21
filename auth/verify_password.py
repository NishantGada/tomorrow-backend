from flask import request, jsonify

from config.dbconfig import get_connection
from helper_functions import auth_required, return_400_error_response, return_200_response
from . import auth_bp


@auth_bp.route("/verify-password", methods=["POST"])
@auth_required
def verify_password():
    data = request.get_json()
    auth_user = request.user["id"]

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT password FROM users WHERE id = %s", (auth_user,))
    password = cursor.fetchone()[0]
    print("password: ", password)

    if password != data["password"]:
        return return_400_error_response("Incorrect password entered. ")

    return return_200_response("Password verification successful", {})
