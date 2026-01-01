from flask import Flask, jsonify, request
import logging
from flask_cors import CORS
import uuid

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = app.logger

# In-memory storage for tasks
tasks_db = [
    {'_id': str(uuid.uuid4()), 'title': 'Sample Task 1'},
    {'_id': str(uuid.uuid4()), 'title': 'Sample Task 2'},
    {'_id': str(uuid.uuid4()), 'title': 'Sample Task 3'}
]

CORS(app)

@app.route('/api/tasks', methods=['GET'])
def get_all_tasks():
    """Retrieve all tasks from in-memory storage."""
    try:
        return jsonify(tasks_db)
    except Exception as e:
        logger.error(f"Error in get_all_tasks: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/task', methods=['POST'])
def add_task():
    """Add a new task to in-memory storage."""
    try:
        data = request.get_json()
        if not data or 'title' not in data:
            return jsonify({'error': 'Title is required'}), 400
            
        title = data['title']
        new_task = {'_id': str(uuid.uuid4()), 'title': title}
        tasks_db.append(new_task)
        
        return jsonify({'result': new_task})
    except Exception as e:
        logger.error(f"Error in add_task: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/task/<id>', methods=['PUT'])
def update_task(id):
    """Update an existing task's title."""
    try:
        data = request.get_json()
        if not data or 'title' not in data:
            return jsonify({'error': 'Title is required'}), 400

        title = data['title']
        for task in tasks_db:
            if task['_id'] == id:
                task['title'] = title
                return jsonify({"result": {'title': task['title']}})
        
        return jsonify({'error': 'Task not found'}), 404
    except Exception as e:
        logger.error(f"Error in update_task: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/task/<id>', methods=['DELETE'])
def delete_task(id):
    """Delete a task by ID."""
    try:
        global tasks_db
        initial_length = len(tasks_db)
        tasks_db = [task for task in tasks_db if task['_id'] != id]
        
        if len(tasks_db) < initial_length:
            result = {'message': 'record deleted'}
        else:
            result = {'message': 'no record found'}
        return jsonify({'result': result})
    except Exception as e:
        logger.error(f"Error in delete_task: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
