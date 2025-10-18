from flask import request, jsonify
import uuid

from config.dbconfig import get_connection
from auth.helper_functions import auth_required
from . import tasks_bp


@tasks_bp.route("/task/<string:task_id>", methods=["DELETE"])
@auth_required
def delete_task(task_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    auth_user = request.user["id"]

    try:
        # check if the task belongs to the auth/logged-in user
        cursor.execute("SELECT * FROM user_tasks WHERE user_id = %s AND task_id = %s", (auth_user, task_id))
        link = cursor.fetchone()

        if not link:
            return jsonify({"success": False, "message": "Task not found or user not authorized"}), 404

        cursor.execute("DELETE FROM tasks WHERE task_id = %s", (task_id,))
        connection.commit()

        return jsonify({"success": True, "message": "Task deleted successfully"}), 200
    
    except Exception as e:
        return (
            jsonify({"success": False, "message": e}),
            500,
        )
    
    finally:
        cursor.close()
        connection.close()
