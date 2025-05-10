from flask import Blueprint, request, jsonify

tasks_blueprint = Blueprint('tasks', __name__)

# In-memory task store (would be a database in production)
tasks = []
task_id_counter = 1


@tasks_blueprint.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks), 200


@tasks_blueprint.route('/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400

    new_task = {
        "id": task_id_counter,
        "title": data['title'],
        "description": data.get('description', ''),
        "status": "todo"
    }

    tasks.append(new_task)
    task_id_counter += 1

    return jsonify(new_task), 201


@tasks_blueprint.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()

    for task in tasks:
        if task['id'] == task_id:
            if 'title' in data:
                task['title'] = data['title']
            if 'description' in data:
                task['description'] = data['description']
            if 'status' in data:
                task['status'] = data['status']

            return jsonify(task), 200

    return jsonify({"error": "Task not found"}), 404


@tasks_blueprint.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks

    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            del tasks[i]
            return "", 204

    return jsonify({"error": "Task not found"}), 404