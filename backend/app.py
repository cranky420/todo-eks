from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient, errors
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MongoDB connection URL (default to Docker service name)
mongo_url = os.getenv("MONGO_URL", "mongodb://mongodb:27017")

# Connect to MongoDB
try:
    client = MongoClient(mongo_url)
    db = client.todo_db
    tasks_collection = db.tasks
    print("✅ MongoDB connected successfully")
except errors.ConnectionFailure as e:
    print(f"❌ Failed to connect to MongoDB: {e}")
    db = None  # Set db to None if connection fails

@app.route('/')
def home():
    return "Welcome to the Todo App!"

@app.route('/test-db')
def test_db():
    """Check if MongoDB is reachable."""
    if db:
        try:
            db.command("ping")  # MongoDB health check
            return jsonify({"status": "success", "message": "MongoDB is reachable"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        return jsonify({"status": "error", "message": "Database connection failed"}), 500

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Fetch all tasks."""
    if db:
        try:
            tasks = list(tasks_collection.find())  
            for task in tasks:
                task["_id"] = str(task["_id"])  # Convert ObjectId to string for JSON response
            return jsonify(tasks), 200
        except Exception as e:
            return jsonify({"error": f"Failed to fetch tasks: {str(e)}"}), 500
    else:
        return jsonify({"error": "Database connection failed"}), 500

@app.route('/tasks', methods=['POST'])
def add_task():
    """Add a new task."""
    if db:
        try:
            task_data = request.json
            task = {"task": task_data.get("task"), "done": False}
            result = tasks_collection.insert_one(task)
            return jsonify({"_id": str(result.inserted_id), "task": task["task"]}), 201
        except Exception as e:
            return jsonify({"error": f"Failed to add task: {str(e)}"}), 500
    else:
        return jsonify({"error": "Database connection failed"}), 500

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task by ID."""
    if db:
        try:
            from bson.objectid import ObjectId  # Import here to avoid issues if unused
            result = tasks_collection.delete_one({"_id": ObjectId(task_id)})
            if result.deleted_count == 1:
                return jsonify({"message": "Task deleted successfully"}), 200
            else:
                return jsonify({"error": "Task not found"}), 404
        except Exception as e:
            return jsonify({"error": f"Failed to delete task: {str(e)}"}), 500
    else:
        return jsonify({"error": "Database connection failed"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

