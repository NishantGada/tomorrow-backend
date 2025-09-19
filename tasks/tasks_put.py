from flask import request, jsonify
import uuid

from config.dbconfig import get_connection
from auth.helper_functions import is_duplicate_email, auth_required
from . import tasks_bp


@tasks_bp.route("/task/<task_id>", methods=["PUT"])
@auth_required
def update_task(task_id):
    data = request.get_json()
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    auth_user = request.user["id"]

    try:
        # check if the task belongs to the auth/logged-in user
        cursor.execute("SELECT * FROM user_tasks WHERE user_id = %s AND task_id = %s", (auth_user, task_id))
        link = cursor.fetchone()

        if not link:
            return jsonify({"success": False, "message": "Task not found or user not authorized"}), 404

        # update only provided fields
        update_fields = []
        values = []

        if "title" in data:
            update_fields.append("title = %s")
            values.append(data["title"])
        if "description" in data:
            update_fields.append("description = %s")
            values.append(data["description"])
        if "priority" in data:
            update_fields.append("priority = %s")
            values.append(data["priority"])

        if not update_fields:
            return jsonify({"success": False, "message": "No fields to update"}), 400

        query = f"UPDATE tasks SET {', '.join(update_fields)} WHERE task_id = %s"
        values.append(task_id)

        cursor.execute(query, tuple(values))
        connection.commit()

        return jsonify({"success": True, "message": "Task updated successfully"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

    finally:
        cursor.close()
        connection.close()
