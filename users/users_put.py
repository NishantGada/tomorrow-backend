from flask import request, jsonify

from config.dbconfig import get_connection
from helper_functions import auth_required, return_400_error_response
from . import users_bp


@users_bp.route("/user", methods=["PUT"])
@auth_required
def update_user():
    data = request.get_json()
    auth_user = request.user["id"]

    # Validate empty body
    if not data:
        return return_400_error_response("Request body is empty")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # Prepare dynamic query
    fields = []
    values = []

    allowed_fields = [
        "first_name",
        "last_name",
        "email",
        "password",
        "phone",
    ]  # allowed updatable fields

    for field in allowed_fields:
        if field in data and data[field] is not None:
            fields.append(f"{field} = %s")
            values.append(data[field])

    if not fields:
        return return_400_error_response("No valid fields provided for update")

    values.append(auth_user)  # Add user id for WHERE

    query = f"""
        UPDATE users
        SET {', '.join(fields)}, updated_at = NOW()
        WHERE id = %s
    """

    try:
        cursor.execute(query, tuple(values))
        connection.commit()

        return jsonify({"success": True, "message": "User updated successfully"}), 200

    except Exception as e:
        print("Error in update_user:", e)
        return jsonify({"success": False, "message": "Internal server error"}), 500

    finally:
        cursor.close()
        connection.close()
