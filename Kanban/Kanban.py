from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = {
    1: {"id": 1, "title": "Tarefa 1", "description": "Descrição da Tarefa 1", "status": "To Do"},
    2: {"id": 2, "title": "Tarefa 2", "description": "Descrição da Tarefa 2", "status": "In Progress"},
    3: {"id": 3, "title": "Tarefa 3", "description": "Descrição da Tarefa 3", "status": "Done"},
}

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks), 200

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = tasks.get(task_id)
    if task:
        return jsonify(task), 200
    return jsonify({"error": "Tarefa não encontrada"}), 404

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_id = max(tasks.keys()) + 1 if tasks else 1
    new_task = {
        "id": new_id,
        "title": data.get("title"),
        "description": data.get("description"),
        "status": data.get("status", "To Do")
    }
    tasks[new_id] = new_task
    return jsonify(new_task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Tarefa não encontrada"}), 404
    task.update({
        "title": data.get("title", task["title"]),
        "description": data.get("description", task["description"]),
        "status": data.get("status", task["status"])
    })
    return jsonify(task), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_id in tasks:
        del tasks[task_id]
        return jsonify({"message": "Tarefa deletada com sucesso"}), 200
    return jsonify({"error": "Tarefa não encontrada"}), 404

if __name__ == '__main__':
    app.run(debug=True)