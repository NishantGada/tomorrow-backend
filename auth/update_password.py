from flask import request, jsonify

from config.dbconfig import get_connection
from helper_functions import auth_required, return_400_error_response, return_200_response
from . import auth_bp

@auth_bp.route("/update-password", methods=["PUT"])
@auth_required
def update_password():
    try:
        data = request.get_json()
        auth_user = request.user["id"]

        connection = get_connection()
        cursor = connection.cursor()

        if not data["new_password"]:
            return return_400_error_response("Incorrect payload. New password seems absent. Cannot update password. ")


        cursor.execute("UPDATE users SET password = %s, updated_at = NOW() WHERE id = %s", (data["new_password"], auth_user))
        connection.commit()

        return return_200_response("Successfully updated password!", {})

    except Exception as e:
        return jsonify({"success": False, "message": e}), 500

    finally:
        cursor.close()
        connection.close()
