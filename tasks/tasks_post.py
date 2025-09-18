from flask import request, jsonify
import uuid

from config.dbconfig import get_connection
from auth.helper_functions import is_duplicate_email, auth_required
from . import tasks_bp


@tasks_bp.route("/task", methods=["POST"])
@auth_required
def register():
    data = request.get_json()
    connection = get_connection()
    cursor = connection.cursor()
    
    auth_user = request.user["id"]
    print("auth_user: ", auth_user)

    try:
        task_id = str(uuid.uuid4())
        query = """
        	INSERT INTO tasks (task_id, title, description, priority) 
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                task_id, 
				data.get("title"), 
				data.get("description"), 
				data.get("priority")
            ),
        )

        user_task_id = str(uuid.uuid4())
        query = """
        	INSERT INTO user_tasks (id, user_id, task_id) 
            VALUES (%s, %s, %s)
        """
        cursor.execute(
            query,
            (
                user_task_id,
                auth_user,
                task_id,
            ),
        )

        connection.commit()
        cursor.close()
        connection.close()

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Task created successfully",
                    "data": {"id": task_id},
                }
            ),
            201,
        )

    except Exception as e:
        return (
            jsonify({"success": False, "message": e}),
            500,
        )
