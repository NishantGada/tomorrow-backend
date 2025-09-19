from flask import request, jsonify
import uuid

from config.dbconfig import get_connection
from auth.helper_functions import auth_required
from . import tasks_bp

@tasks_bp.route("/tasks", methods=["GET"])
@auth_required
def get_tasks_by_user_id():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    auth_user = request.user["id"]

    cursor.execute("SELECT task_id FROM user_tasks WHERE user_id = %s", (auth_user,))
    task_ids = cursor.fetchall()
    print("task_ids: ", task_ids)

    tasks = []
    
    for task_id in task_ids:
        cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id["task_id"],))
        task = cursor.fetchone()
        tasks.append(task)


    return jsonify({
        "success": True, 
        "message": "Tasks fetched successfully", 
        "data": {
            "tasks": tasks if tasks else [],
            "count": len(tasks)
        }
    }), 200
